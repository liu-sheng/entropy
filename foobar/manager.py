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

from foobar.openstack.common import service as os_service
from foobar.openstack.common import log
from stevedore import extension
import time

LOG = log.getLogger(__name__)


class AgentManager(os_service.Service):

    def __init__(self, namespace, default_discovery=None, group_prefix=None):
        super(AgentManager, self).__init__()

    @staticmethod
    def _extensions(category, agent_ns=None):
        namespace = ('foobar.%s.%s' % (category, agent_ns) if agent_ns
                     else 'foobar.%s' % category)
        return extension.ExtensionManager(
            namespace=namespace,
            invoke_on_load=True,
        )

    def _test_db(self):
        from foobar import db
        from oslo.config import cfg
        conn = db.get_connection_from_config(cfg.CONF)
        conn.record_resources('12345', 'test', 'test_meta')

    def start(self):
        self._test_db()
        while True:
            LOG.error('just test!!!')
            time.sleep(5)





