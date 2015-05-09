# -*- encoding: utf-8 -*-
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import functools

from oslo.utils import strutils
from oslo.utils import timeutils
import pecan
from pecan import rest
from wsme import types as wtypes
import wsmeext.pecan as wsme_pecan


class Instance(wtypes.Base):
    resource_id = wtypes.text
    resource_type = wtypes.text
    resource_meta = wtypes.DictType(wtypes.text, wtypes.text)

    @classmethod
    def from_db_model(cls, m):
        return cls(**(m.as_dict()))


class ResourcesController(rest.RestController):
    _custom_actions = {
        'history': ['GET'],
    }

    @wsme_pecan.wsexpose(Instance, body=Instance, status_code=201)
    def post(self, data):
        try:
            resource = pecan.request.db_conn.record_resources(
                data.resource_id, 'instance', {})
        except Exception:
            raise
        pecan.response.status = 201
        return Instance.from_db_model(resource)

    @pecan.expose('json')
    def get_all(self):
        return [r.as_dict() for r in pecan.request.db_conn.get_resources()]

    @pecan.expose('json')
    def history(self):
        return {}


class V1Controller(object):
    resource = ResourcesController()


class RootController(object):
    v1 = V1Controller()

    @staticmethod
    @pecan.expose(content_type="text/plain")
    def index():
        return "Nom nom nom."
