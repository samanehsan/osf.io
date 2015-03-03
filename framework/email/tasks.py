import smtplib
import logging
from email.mime.text import MIMEText

from framework.tasks import app
from website import settings

logger = logging.getLogger(__name__)


@app.task
def send_email(from_addr, to_addr, subject, message, mimetype='html', ttls=True, login=True,
                username=None, password=None, mail_server=None):
    """Send email to specified destination.
    Email is sent from the email specified in FROM_EMAIL settings in the
    settings module.

    :param from_addr: A string, the sender email
    :param to_addr: A string, the recipient
    :param subject: subject of email
    :param message: body of message

    :return: True if successful
    """
    username = username or settings.MAIL_USERNAME
    password = password or settings.MAIL_PASSWORD
    mail_server = mail_server or settings.MAIL_SERVER

    if not settings.USE_EMAIL:
        return
    if login and (username is None or password is None):
        logger.error('Mail username and password not set; skipping send.')
        return

    msg = MIMEText(message, mimetype, _charset='utf-8')
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr

    s = smtplib.SMTP(mail_server)
    s.ehlo()
    if ttls:
        s.starttls()
        s.ehlo()
    if login:
        s.login(username, password)
    s.sendmail(
        from_addr=from_addr,
        to_addrs=[to_addr],
        msg=msg.as_string()
    )
    s.quit()
    return True
