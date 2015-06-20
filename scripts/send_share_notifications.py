import httplib as http
import datetime
import logging
from furl import furl
from framework import sentry
from framework.auth.core import User
from framework.exceptions import HTTPError
from website import mails
from website.app import init_app
from website.notifications.model import ShareSubscription
from website.search.util import build_query
import website.search.search as search
from website.search.exceptions import IndexNotFoundError
from website.search.exceptions import MalformedQueryError
from website import settings
from framework.tasks import app as celery_app
from scripts import utils as script_utils

logger = logging.getLogger(__name__)
# Silence loud internal mail logger
SILENT_LOGGERS = [
    'website.mails',
    'amqp',
]
if not settings.DEBUG_MODE:
    for logger_name in SILENT_LOGGERS:
        logging.getLogger(logger_name).setLevel(logging.CRITICAL)


def main():
    script_utils.add_file_logger(logger, __file__)
    app = init_app(attach_request_handlers=False)
    celery_app.main = 'scripts.send_digest'
    send_email()


def send_email():
    user_subscriptions = ShareSubscription.find()
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=7)

    for s in user_subscriptions:
        user = User.load(s.user_id)
        if not user:
            sentry.log_exception()
            sentry.log_message("A user with this username does not exist.")
            return
        url = furl(s.url)
        url.args['q'] = url.args['q'] + '+AND+dateUpdated%3A%5B' + start_date.strftime('%Y-%m-%d') + '+TO+' + end_date.strftime('%Y-%m-%d') + '%5D'
        query = build_query(url.args['q'])
        query_url = url.url

        try:
            search_results = search.search_share(query, index='share_v1')
        except MalformedQueryError:
            raise HTTPError(http.BAD_REQUEST)
        except IndexNotFoundError:
            search_results = {
                'count': 0,
                'results': []
            }

        count = search_results.get('count', None)
        if count > 0:
            mails.send_mail(
                to_addr=user.username,
                mail=mails.SHARE_NOTIFICATION,
                name=user.fullname,
                count=count,
                query_url = query_url
            )


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()