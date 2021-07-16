import json
import os
import logging
from concurrent.futures import ThreadPoolExecutor
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import pprint
import websocket
from click.testing import CliRunner
from webexteamssdk import WebexTeamsAPI
from webexteamssdk.exceptions import ApiError
from webexteamssdk.models.immutable import Message
from wibot.rbac import get_role
from wibot.cli.cli import search
from wibot.utils import get_config
from wibot import BOT_AUTH_HEADER
from wibot.cli.cards import handle_doc


BOT_NAME='awsm-o'
BOT_TOKEN='YzhmYzQ3NmMtMGRkNy00MTgxLWI1ZDYtZmZhOWFkMjlhNWU3ZjdkNDQ0OTgtZjgw_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f'

LOGGER = logging.getLogger(__name__)
API_URL = "https://api.ciscospark.com/v1/messages"
ATTACHMENT_URL = "https://webexapis.com/v1/attachment/actions"
MAX_MSG_SIZE = 4096

api: WebexTeamsAPI = None
#changed max#workers to 1 to avoid message swap between concurrent calls
message_processor = ThreadPoolExecutor(max_workers=1)


def send_response(roomId: str, response_text: str):
    markdown = """
    ```\n{response}
    """.format(response=response_text)

    json_data = {
        'roomId': roomId,
        'markdown': markdown,
    }
    response = requests.request('POST', API_URL, json=json_data, headers=BOT_AUTH_HEADER)
    LOGGER.debug(pprint.pprint(response.json()))

def get_card_content(message):
    id = message.get('data').get('id')
    try:
        url = "https://api.ciscospark.com/v1/attachment/actions/%s" % id
        bearer = parameter['bearer']
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": "Bearer " + bearer
        }
        request = requests.get(url, headers=headers).json()
        print('request: ', request)
        if request.get('inputs'):
            return request.get('inputs')
        else:
            return "ERROR: cannot get the inputs, %s" % request.content
    except Exception as e:
        print(e)

def module_create_card(webhook, card):
    content = [
        {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": card()
        }
    ]
    try:
        url = "https://api.ciscospark.com/v1/messages"
        json_data = {
            'roomId': roomId,
            'markdown': markdown,
        }
        response = requests.request('POST', API_URL, json=json_data, headers=BOT_AUTH_HEADER)
        LOGGER.debug(pprint.pprint(response.json()))

        return "create card successfully..."
    except Exception as e:
        return "ERROR: create card failed, %s" % e

def send_card_response(roomId: str, card_response: str):
    json_data = {
        'roomId': roomId,
        'markdown': 'x',
        'attachments': [card_response],
    }
    pprint.pprint(json.dumps(json_data))
    response = requests.request('POST', API_URL, json=json_data, headers=BOT_AUTH_HEADER)
    LOGGER.debug(pprint.pprint(response.json()))

def module_receive_cards(message):
    print('message:', message)
    card_content = get_card_content(message)
    roomId = message['data']['roomId']
    print('#####card content ', card_content)
    if 'ERROR:' in card_content:
        print('ERROR: %s' % card_content)
        return card_content
    else:
        function = list(card_content.keys())[-1]
        for item in card_content.keys():
            if item != 'subscribe':
                function = item
                break
        print('#####function: ', function)
        send_response(message, 'processing...')
        if 'show_port' in function:
            in_message = process_show_port_input(card_content)
            msg = show_port(in_message, message)
            send_response(message, msg)


def handled_using_card(message, args) -> bool:
    if args and args[0] == 'Awesom-o':
        args = args[1:]

    if args[0] != 'demo' or args[1:] is None:
        return False

    card_response = handle_doc('demo')

    if not card_response:
        return False

    send_card_response(message.roomId, card_response)
    return True

def attachment_post(roomId : str, logtype: str):
    log_file_dir = os.getcwd()
    print(log_file_dir)
    if logtype == 'embaudit':
        log_file_name = "EmbConScan_log.txt"
    elif logtype == 'pwrscan':
        log_file_name = "PwrScan_log.txt"
    elif logtype == 'codescan':
        log_file_name = 'CodeVersion_log.txt'
    log_filepath = os.path.join(log_file_dir,log_file_name)
    print(log_filepath)
    m = MultipartEncoder({'roomId': roomId,
                          'text': 'Scan Results Attached',
                          'files': (log_filepath, open(log_filepath,'rb'),
                          'image/png')})

    headers={'Authorization': 'Bearer {}'.format(BOT_TOKEN),
    'Content-Type': m.content_type}

    response = requests.request('POST', API_URL, data=m, headers=headers)
    print(response)

    LOGGER.debug(pprint.pprint(response.json()))


def html_message_post(roomid: str, html: str):
    """Post a message to a spark room"""
    try:
        json_data = {"roomId": roomid,
                     "html": html}
        response = requests.request("POST", API_URL, json=json_data, headers=BOT_AUTH_HEADER).json()
        return response
    except Exception as e:
        LOGGER.error(str({'title': 'spark_message_post', 'exception': str(e)}))


def process_message(message):
    json_data = json.loads(message)
    if 'data' in json_data and \
        'activity' in json_data['data'] and \
        'id' in json_data['data']['activity']:
        message_id = json_data['data']['activity']['id']
        try:
            message: Message = api.messages.get(message_id)
            LOGGER.debug(message)
            if message.personId == api.people.me().id:
                return

            email = message.personEmail
            roles = get_role(email)
            if not roles:
                send_response(message.roomId, "Sorry {} , it seems you don't have access to use Awesom-o,Please send an email with justification to iaas-fw@cisco.com to request access ".format(email))
                return
            for role in roles:
                LOGGER.debug("Using role: {}".format(role))
                LOGGER.debug(message.text)
                runner = CliRunner()
                args = message.text.split()
                result = "Acess Denied {}".format(email)
                if role == "search":
                    if args[0] == 'Awesom-o' and args[1] == 'demo':
                        if handled_using_card(message, args):
                            print("Card Created Successfully")
                            return
                        else:
                            help_msg = "Please enter hi or @Aweso-o help in a team space to get started "
                            send_response(message.roomId, help_msg) 
                    if args[0] =='demo':
                        if handled_using_card(message, args):
                            print("Card Created Successfully")
                            return
                        else:
                            help_msg = "Please enter hi or @Aweso-o help in a team space to get started "
                            send_response(message.roomId, help_msg) 

                    elif args[0] == 'Awesom-o' and args[1] == 'search':
                        result = runner.invoke(search, args[1:] if not args[0] == 'Awesom-o' else args[2:])
                        LOGGER.debug("{} {}".format(result.output, result.exit_code))
                         #
                         # Webex Teams has a limit on message size, so we need to chunk the output
                         #                 
                        split_output = result.output.split('\n')
                        buf = ''
                        for line in split_output:
                            buf = buf + '\n' + line
                            if len(buf) > MAX_MSG_SIZE:
                                send_response(message.roomId, buf)
                                buf = ''

                        if buf.strip():
                            send_response(message.roomId, buf)

                    else:
                        result = runner.invoke(search, args[1:] if not args[0] == 'Awesom-o'else args[2:])
                        LOGGER.debug("{} {}".format(result.output, result.exit_code))
                         #
                         # Webex Teams has a limit on message size, so we need to chunk the output
                         #                 
                        split_output = result.output.split('\n')
                        buf = ''
                        for line in split_output:
                            buf = buf + '\n' + line
                            if len(buf) > MAX_MSG_SIZE:
                                send_response(message.roomId, buf)
                                buf = ''

                        if buf.strip():
                            send_response(message.roomId, buf)

        except ApiError:
            LOGGER.error("Unable to fetch message {}".format(message_id, json_data))


def on_message(ws, message):
    message_processor.submit(process_message, message)


def on_open(ws):
    LOGGER.debug('Opened received on ws')


def on_error(ws, err):
    LOGGER.error('Got a websocket error {}'.format(err))


def on_close(ws):
    LOGGER.info('Websocket closed')


class MessageHandler:

    def __init__(self, wss_url):
        websocket.enableTrace(True)
        header = {'Authorization:Bearer {}'.format(BOT_TOKEN)}
        self.ws = websocket.WebSocketApp(wss_url, on_open=on_open, on_message=on_message,
                                         on_close=on_close, on_error=on_error, header=header)

    def run_forever(self):
        LOGGER.info("Running websocket listener forever")
        global api
        api = WebexTeamsAPI(access_token=BOT_TOKEN)

        self.ws.run_forever()
