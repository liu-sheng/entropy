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
import os
import socket
from wsgiref import simple_server
import threading

import netaddr
from oslo.config import cfg
import pecan
from pecan import hooks

from entropy.openstack.common import log
from entropy import db
from entropy.api import middleware


LOG = log.getLogger(__name__)

API_SERVICE_OPTS = [
    cfg.IntOpt('port',
               default=8099,
               help='The port for the entropy API server.',
               ),
    cfg.StrOpt('host',
               default='0.0.0.0',
               help='The listen IP for the entropy API server.',
               ),
]

opt_group = cfg.OptGroup(name='api',
                         title='Options for the entropy-api service')
cfg.CONF.register_group(opt_group)
cfg.CONF.register_opts(API_SERVICE_OPTS, opt_group)

CONF = cfg.CONF


class DBHook(pecan.hooks.PecanHook):

    def __init__(self, db_conn):
        self.db_conn = db_conn

    def on_route(self, state):
        state.request.db_conn = self.db_conn

PECAN_CONFIG = {
    'app': {
        'root': 'entropy.api.v1.RootController',
        'modules': ['entropy.api.v1'],
    },
    'conf': cfg.CONF,
}


def setup_app(pecan_config=PECAN_CONFIG):
    app_hooks = [DBHook(db.get_connection_from_config(cfg.CONF))]
    pecan.configuration.set_config(dict(pecan_config), overwrite=True)
    app = pecan.make_app(
        pecan_config['app']['root'],
        debug=CONF.debug,
        hooks=app_hooks,
        guess_content_type_from_ext=False
    )
    return app


def get_server_cls(host):
    """Return an appropriate WSGI server class base on provided host

    :param host: The listen host for the entropy API server.
    """
    server_cls = simple_server.WSGIServer
    if netaddr.valid_ipv6(host):
        if getattr(server_cls, 'address_family') == socket.AF_INET:
            class server_cls(server_cls):
                address_family = socket.AF_INET6
    return server_cls


def build_server():

    host, port = cfg.CONF.api.host, cfg.CONF.api.port
    srv = simple_server.make_server(host,
                                    port,
                                    setup_app(),
                                    get_server_cls(cfg.CONF.api.host))
    LOG.info(_('Starting server in PID %s') % os.getpid())
    if host == '0.0.0.0':
        LOG.info(_(
            'serving on 0.0.0.0:%(sport)s, view at http://127.0.0.1:%(vport)s')
            % ({'sport': port, 'vport': port}))
    else:
        LOG.info(_("serving on http://%(host)s:%(port)s") % (
                 {'host': host, 'port': port}))

    srv.serve_forever()
