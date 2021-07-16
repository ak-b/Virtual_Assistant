from wibot.cli.cards.demo import get_demo
from wibot.cli.cards.feature import *


def handle_doc(args):
    if 'demo' == args:
        return get_demo()