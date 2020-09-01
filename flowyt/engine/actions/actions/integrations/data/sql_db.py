import sqlalchemy
from engine.actions.action import GenericAction
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


class Database:
    model = None
    result = None
    engine = None
    session_maker = None
    session = None

    def __init__(self, config):
        host = "{0}:{1}".format(config.host, config.port)

        self.engine = sqlalchemy.create_engine(
            "{0}://{1}:{2}@{3}/{4}".format(config.sgbd, config.user, config.password, host, config.database)
        )

        self.session_maker = sessionmaker(bind=self.engine, autoflush=True)
        self.session = scoped_session(self.session_maker)

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
    action_schema: {}

    def handle(self, action_data, execution_context, pipeline_context):
        conn_name = action_data.get("conn_name")

        database = Database(execution_context.private.integrations.sql_database.get(conn_name, {}))

        data = []
        if action_data.get("sql"):
            data = self.execute_raw(database, action_data.get("sql"))

        execution_context.public.response = {"db": database, "data": data}

        return execution_context, pipeline_context

    def execute_raw(self, database, sql):
        result = database.raw(sql)

        # Try get data
        data = None

        try:
            data = database.to_list()
        except:
            pass

        return result
