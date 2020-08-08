import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session

from engine.actions.action import GenericAction


class Database:
    result = None
    engine = None
    session = None

    def __init__(self, config):
        host = "{0}:{1}".format(config.host, config.port)

        self.engine = sqlalchemy.create_engine(
            "{0}://{1}:{2}@{3}/{4}".format(config.sgbd, config.user, config.password, host, config.database)
        )

        self.session = scoped_session(sessionmaker(bind=self.engine))

    def raw(self, sql):
        sql = sqlalchemy.text(sql)
        self.result = self.engine.execute(sql)
        return self

    def to_list(self):
        data = []
        info = self.result.keys()
        for row in self.result:
            line = {}
            for i, col in enumerate(row):
                line[info[i]] = col
            data.append(line)
        return data


class SqlDatabase(GenericAction):
    def handle(self, action_data, execution_context, pipeline_context):
        conn_name = action_data.get("conn_name")

        database = Database(execution_context.private.integrations.sql_database.get(conn_name, {}))
        execution_context.public.response = database

        if not action_data.get("sql"):
            return execution_context, None

        result = database.raw(action_data.get("sql"))

        execution_context.public.response = {"db": database}

        return execution_context, pipeline_context

    def to_list(self, rows):
        data = []
        info = rows.keys()
        for row in rows:
            line = {}
            for i, col in enumerate(row):
                line[info[i]] = col
            data.append(line)
        return data
