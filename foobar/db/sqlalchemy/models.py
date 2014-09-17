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
import uuid

from oslo.db.sqlalchemy import migration
from oslo.config import cfg
from oslo.db import exception as dbexc
from oslo.db.sqlalchemy import migration
from oslo.db.sqlalchemy import session as db_session
from oslo.utils import timeutils
from oslo.db.sqlalchemy import models
from sqlalchemy.ext.declarative import declarative_base


class FoobarBase(models.ModelBase):
    __table_args__ = {'mysql_charset': "utf8",
                      'mysql_engine': "InnoDB"}

Base = declarative_base()


class Resource(Base, FoobarBase):
    __tablename__ = 'resource'

    id = sqlalchemy.Column(uuid, primary_key=True)
    resource_type = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    resource_metadata = sqlalchemy.Column(sqlalchemy.String(5000),
                                          nullable=False)


class History(Base, FoobarBase):
    __tablename__ = 'history'
    id = sqlalchemy.Column(uuid, primary_key=True)

