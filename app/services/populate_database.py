from app import *

class PopulateDatabase:
    def __init__(self):
        self.engine = engine


    def populate_table(self, table_name, df):
        meta = MetaData()
        meta.reflect(bind=self.engine)
        table = meta.tables[table_name]
        conn = self.engine.connect()
        conn.execute(table.delete())
        df.to_sql(table_name, self.engine, if_exists='append', index=False)
        conn.close()