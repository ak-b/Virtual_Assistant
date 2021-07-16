# -*- coding: utf-8 -*-

"""Main module."""
import logging
import os

from wibot.endpoint import SparkEndpoint
from wibot.handler import MessageHandler
from wibot.rbac import rbac_init

logging.getLogger('wibot.endpoint').addHandler(logging.StreamHandler())
logging.getLogger('wibot.endpoint').setLevel(logging.DEBUG)

logging.getLogger('wibot.handler').addHandler(logging.StreamHandler())
logging.getLogger('wibot.handler').setLevel(logging.DEBUG)

logging.getLogger('wibot.rbac').addHandler(logging.StreamHandler())
logging.getLogger('wibot.rbac').setLevel(logging.DEBUG)


if __name__ == "__main__":
    filepath = '/opt/wibot/users.properties'
    rbac_init(filepath)
    spark_endpoint = SparkEndpoint()
    spark_endpoint.setup()
    message_handler = MessageHandler(spark_endpoint.get_websocket_url())
    message_handler.run_forever()
