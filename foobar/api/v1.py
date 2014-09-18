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

from oslo.utils import strutils
from oslo.utils import timeutils
import pecan
from pecan import rest


class InstancesController(rest.RestController):

    @pecan.expose('json')
    def post(self):
        try:
            resource = pecan.request.db_conn.record_resources(
                '12345', 'test', 'test_meta')
        except Exception:
            raise
        pecan.response.status = 201
        return resource

    @pecan.expose('json')
    def get_all(self, **kwargs):
        return [r for r in pecan.request.db_conn.get_resources()]


class ResourcesController(rest.RestController):
    instance = InstancesController()


class V1Controller(object):
    resource = ResourcesController()


class RootController(object):
    v1 = V1Controller()

    @staticmethod
    @pecan.expose(content_type="text/plain")
    def index():
        return "Nom nom nom."