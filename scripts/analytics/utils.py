# -*- coding: utf-8 -*-

import os
import unicodecsv as csv
from bson import ObjectId

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns  # noqa

import requests

from website.addons.osfstorage import utils as storage_utils


def oid_to_datetime(oid):
    return ObjectId(oid).generation_time


def mkdirp(path):
    try:
        os.makedirs(path)
    except OSError:
        pass


def plot_dates(dates, *args, **kwargs):
    """Plot date histogram."""
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.hist(
        [mdates.date2num(each) for each in dates],
        *args, **kwargs
    )

    fig.autofmt_xdate()
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    return fig


def make_csv(fp, rows, headers=None):
    writer = csv.writer(fp)
    if headers:
        writer.writerow(headers)
    writer.writerows(rows)


def send_file(app, name, content_type, file_like, node, user):
    """Upload file to OSF."""
    file_like.seek(0)
    with app.test_request_context():
        upload_url = storage_utils.get_waterbutler_upload_url(
            user,
            node,
            path=name,
        )
    requests.put(
        upload_url,
        data=file_like,
        headers={'Content-Type': content_type},
    )
