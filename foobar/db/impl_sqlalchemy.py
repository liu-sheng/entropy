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

"""SQLAlchemy storage backend."""

from __future__ import absolute_import
import os

from oslo.db.sqlalchemy import migration
from oslo.config import cfg
from oslo.db import exception as dbexc
from oslo.db.sqlalchemy import migration
from oslo.db.sqlalchemy import session as db_session
from oslo.utils import timeutils
from oslo.db.sqlalchemy import models
from sqlalchemy.ext import declarative
from oslo.db.sqlalchemy import session
from foobar.db.sqlalchemy import models
from oslo.db import exception as db_exception

from foobar import exception
from foobar.db import api_models


Base = declarative.declarative_base()


class Connection(object):
    def __init__(self, url):
        self._engine_facade = db_session.EngineFacade(
            url,
            **dict(cfg.CONF.database.items())
        )

    def upgrade(self):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            'sqlalchemy', 'migrate_repo')
        migration.db_sync(self._engine_facade.get_engine(), path)

    def clear(self):
        engine = self._engine_facade.get_engine()
        for table in reversed(models.Base.metadata.sorted_tables):
            engine.execute(table.delete())
        self._engine_facade._session_maker.close_all()
        engine.dispose()

    def record_resources(self, resource_id, resource_type, resource_meta):
        session = self._engine_facade.get_session()
        with session.begin(subtransactions=True):
            event = models.Resource(id=resource_id,
                                    resource_type=resource_type,
                                    resource_metadata=resource_meta)
            session.add(event)
            try:
                session.flush()
            except db_exception.DBDuplicateEntry:
                raise exception.ResourceAlreadyExists(resource_id)

    def get_resources(self, **kwargs):
        session = self._engine_facade.get_session()
        query = session.query()
        for row in query.all():
            yield api_models.Resource(resource_id=row.id,
                                      resource_type=row.resource_type,
                                      resource_meta=row.resource_metadata)
