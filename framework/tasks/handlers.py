# -*- coding: utf-8 -*-

import logging
import functools

from flask import g
from celery import chain

from website import settings


logger = logging.getLogger(__name__)


def celery_before_request():
    g._celery_tasks = []


def celery_teardown_request(error=None):
    if error is not None:
        return
    try:
        tasks = g._celery_tasks
        if tasks:
            chain(*tasks)()
    except AttributeError:
        if not settings.DEBUG_MODE:
            logger.error('Task queue not initialized')


def enqueue_task(signature):
    """If working in a request context, push task signature to ``g`` to run
    after request is complete; else run signature immediately.
    :param signature: Celery task signature
    """
    try:
        if signature not in g._celery_tasks:
            g._celery_tasks.append(signature)
    except RuntimeError:
        signature()


def queued_task(task):
    """Decorator that adds the wrapped task to the queue on ``g`` if Celery is
    enabled, else runs the task synchronously. Can only be applied to Celery
    tasks; should be used for all tasks fired within a request context that
    may write to the database to avoid race conditions.
    """
    @functools.wraps(task)
    def wrapped(*args, **kwargs):
        if settings.USE_CELERY:
            signature = task.si(*args, **kwargs)
            enqueue_task(signature)
        else:
            task(*args, **kwargs)
    return wrapped


handlers = {
    'before_request': celery_before_request,
    'teardown_request': celery_teardown_request,
}
