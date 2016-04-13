"""Get number of users who have created a comment."""
import logging
import sys
from bson.code import Code
from framework.mongo import database as db
from framework.transactions.context import TokuTransaction

from website.app import init_app
from scripts import utils as script_utils

logger = logging.getLogger(__name__)


def main():
    users = group_comments_by_user()
    logger.info("{} users have created comments.".format(len(users)))
    for user in users:
        logger.info(user)


def group_comments_by_user():
    """ Group comments by user.
        :return: [{
                    'user': User._id,
                    'comments': [Comment._id, Comment._id...]
                  },
                  {
                    'user': ...
                  }]
    """
    return db['comment'].group(
        key={'user': 1},
        condition={},
        initial={'comments': 0},
        reduce=Code("""function(curr, result) {
                        result.comments += 1;
                    };""")
    )


if __name__ == '__main__':
    dry = '--dry' in sys.argv
    if not dry:
        script_utils.add_file_logger(logger, __file__)
    init_app(routes=False, set_backends=True)
    with TokuTransaction():
        main()
        if dry:
            raise Exception('Dry Run -- Aborting Transaction')
