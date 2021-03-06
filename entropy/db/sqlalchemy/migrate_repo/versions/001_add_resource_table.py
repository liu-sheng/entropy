#
# Author: John Tran <jhtran@att.com>
#
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

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import UniqueConstraint
from entropy.db.sqlalchemy import models as db_models


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    resource = Table(
        'resource', meta,
        Column('resource_id', String(255), primary_key=True, index=True),
        Column('resource_type', String(255)),
        Column('ha_condition', String(255)),
        Column('resource_metadata', String(5000)),
        Column('project_id', String(255), index=True),
        Column('user_id', String(255), index=True),
        Column('created_at', db_models.PreciseTimestamp(), index=True),
        mysql_engine='InnoDB',
        mysql_charset='utf8',
    )

    tables = [resource]
    for i in sorted(tables):
        i.create()


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    for name in ['resource']:
        t = Table(name, meta, autoload=True)
        t.drop()
