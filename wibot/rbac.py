import configparser
import logging
from collections import defaultdict

LOGGER = logging.getLogger(__name__)

users = defaultdict(set)


def rbac_init(users_db: str):
    global users
    with open(users_db) as f:
        config = configparser.ConfigParser()
        config.read_file(f)
        all_users = config['users']
        for role in all_users:
            users_in_role = all_users[role]
            for user in users_in_role.split(','):
                users[user].add(role)
    LOGGER.info("RBAC init complete {}".format(users))
    return users


def get_role(user_email):
    user = user_email.split('@')[0]

    LOGGER.debug('Getting cli for {}'.format(user))
    if user not in users:
        return None

    roles = users[user]
    LOGGER.debug('Got roles {}'.format(roles))
    return roles
