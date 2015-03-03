# -*- coding: utf-8 -*-

import bson
from modularodm import fields, Q
from modularodm.exceptions import ModularOdmException

from framework.mongo import StoredObject

from website.conferences.exceptions import ConferenceError


class Conference(StoredObject):
    #: Determines the email address for submission and the OSF url
    # Example: If endpoint is spsp2014, then submission email will be
    # spsp2014-talk@osf.io or spsp2014-poster@osf.io and the OSF url will
    # be osf.io/view/spsp2014
    endpoint = fields.StringField(primary=True, required=True, unique=True)
    #: Full name, e.g. "SPSP 2014"
    name = fields.StringField(required=True)
    info_url = fields.StringField(required=False, default=None)
    logo_url = fields.StringField(required=False, default=None)
    active = fields.BooleanField(required=True)
    admins = fields.ForeignField('user', list=True, required=False, default=None)
    #: Whether to make submitted projects public
    public_projects = fields.BooleanField(required=False, default=True)

    @classmethod
    def get_by_endpoint(cls, endpoint, active=True):
        query = Q('endpoint', 'iexact', endpoint)
        if active:
            query &= Q('active', 'eq', True)
        try:
            return Conference.find_one(query)
        except ModularOdmException:
            raise ConferenceError('Endpoint {0} not found'.format(endpoint))


class MailRecord(StoredObject):
    _id = fields.StringField(primary=True, default=lambda: str(bson.ObjectId()))
    data = fields.DictionaryField()
    records = fields.AbstractForeignField(list=True, backref='created')
