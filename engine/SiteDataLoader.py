import sqlite3 as lite
import sys
import pandas as pd


class SiteDataLoader(object):
    def __init__(self, db_path):
        self.db_path = db_path
        self.con = None
        self.result_set = None

    def query(self, sql_script):
        try:
            self.con = lite.connect(self.db_path)
            self.result_set = pd.read_sql(sql_script, self.con)
        except lite.Error as e:
            if self.con:
                self.con.rollback()
            print("Error %s:" % e.args[0])
            sys.exit(1)
        finally:
            if self.con:
                self.con.close()

    def insert_data(self, data, dest):
        try:
            self.con = lite.connect(self.db_path)
            data.to_sql(dest, self.con, if_exists='append', index=False)
        except lite.Error as e:
            if self.con:
                self.con.rollback()
            print("Error %s:" % e.args[0])
            sys.exit(1)
        finally:
            if self.con:
                self.con.close()

    def upsert(self, src, dest, pk):
        self.query("SELECT DISTINCT {} as pk FROM {}".format(pk, dest))
        # print(self.result_set)

        src.drop_duplicates('pk', keep='last', inplace=True)
        delta = pd.merge(src, self.result_set, how='left', on='pk', indicator=True)
        delta = delta[delta['_merge'] == 'left_only']
        delta.drop(['_merge', 'pk'], axis=1, inplace=True)
        self.insert_data(delta, dest)
