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
from oslo.config import cfg

from foobar.indexer import sqlalchemy as sql_db
from foobar.rest import app
from foobar import service
from foobar import manager
from foobar.openstack.common import service as os_service


def agent():
    service.prepare_service()
    os_service.launch(manager.AgentManager('foobar')).wait()


def storage_dbsync():
    service.prepare_service()
    indexer = sql_db.SQLAlchemyIndexer(cfg.CONF)
    indexer.upgrade()


def api():
    service.prepare_service()
    app.build_server()

#TODO server