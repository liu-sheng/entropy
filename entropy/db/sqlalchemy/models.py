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

from __future__ import absolute_import
import sqlalchemy
import json
import six

from oslo.db.sqlalchemy import migration
from oslo.config import cfg
from oslo.db import exception as dbexc
from oslo.db.sqlalchemy import migration
from oslo.db.sqlalchemy import session as db_session
from oslo.utils import timeutils
from oslo.db.sqlalchemy import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TypeDecorator
from sqlalchemy import Float, Boolean, Text, DateTime
from sqlalchemy.dialects.mysql import DECIMAL
from oslo.utils import timeutils
from entropy import utils


class entropyBase(models.ModelBase):
    __table_args__ = {'mysql_charset': "utf8",
                      'mysql_engine': "InnoDB"}

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def update(self, values):
        """Make the model object behave like a dict."""
        for k, v in six.iteritems(values):
            setattr(self, k, v)

Base = declarative_base()


class JSONEncodedDict(TypeDecorator):
    """Represents an immutable structure as a json-encoded string."""

    impl = sqlalchemy.String

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class PreciseTimestamp(TypeDecorator):
    """Represents a timestamp precise to the microsecond."""

    impl = DateTime

    def load_dialect_impl(self, dialect):
        if dialect.name == 'mysql':
            return dialect.type_descriptor(DECIMAL(precision=20,
                                                   scale=6,
                                                   asdecimal=True))
        return self.impl

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'mysql':
            return utils.dt_to_decimal(value)
        return value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'mysql':
            return utils.decimal_to_dt(value)
        return value


class Resource(Base, entropyBase):
    __tablename__ = 'resource'

    id = sqlalchemy.Column(sqlalchemy.String(255), primary_key=True)
    resource_type = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.String(255))
    project_id = sqlalchemy.Column(sqlalchemy.String(255))
    ha_condition = sqlalchemy.Column(sqlalchemy.String(255))
    created_at = sqlalchemy.Column(PreciseTimestamp,
                                   default=lambda: timeutils.utcnow())
    resource_metadata = sqlalchemy.Column(JSONEncodedDict)


class History(Base, entropyBase):
    __tablename__ = 'history'
    id = sqlalchemy.Column(sqlalchemy.String(255), primary_key=True)
