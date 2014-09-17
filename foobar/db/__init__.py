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
from oslo.db import options as db_options
import six
import six.moves.urllib.parse as urlparse
from stevedore import driver

from foobar.openstack.common.gettextutils import _
from foobar.openstack.common import log
from foobar import utils


LOG = log.getLogger(__name__)

OLD_STORAGE_OPTS = [
    cfg.StrOpt('database_connection',
               secret=True,
               help='DEPRECATED - Database connection string.',
               ),
]

cfg.CONF.register_opts(OLD_STORAGE_OPTS)


STORAGE_OPTS = [
    cfg.IntOpt('time_to_live',
               default=-1,
               help="Number of seconds that samples are kept "
               "in the database for (<= 0 means forever)."),
]

cfg.CONF.register_opts(STORAGE_OPTS, group='database')

db_options.set_defaults(cfg.CONF)
cfg.CONF.import_opt('connection', 'oslo.db.options', group='database')


class StorageBadVersion(Exception):
    """Error raised when the storage backend version is not good enough."""


class StorageBadAggregate(Exception):
    """Error raised when an aggregate is unacceptable to storage backend."""
    code = 400


def get_connection_from_config(conf):
    if conf.database_connection:
        conf.set_override('connection', conf.database_connection,
                          group='database')
    namespace = 'foobar.db'
    url = conf.database.connection
    connection_scheme = urlparse.urlparse(url).scheme
    engine_name = connection_scheme.split('+')[0]
    LOG.debug(_('looking for %(name)r driver in %(namespace)r') % (
              {'name': engine_name, 'namespace': namespace}))
    mgr = driver.DriverManager(namespace, engine_name)
    return mgr.driver(url)
