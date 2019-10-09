from django.db import models
import sqlite3
from .dom_mod.domain2 import *

# Create your models here.

class Domain_c():
    def __init__(self):
        self.db_table = "domainlist"
        self.db_column1 = "domains"
        self.db_column2 = "status"
        self.db_column3 = "lastcheck"
        self.db_column4 = "forcecheck"
        self.db_conn = sqlite3.connect('dom_mod/domain.db')
        self.cursor = self.db_conn.cursor()
    def querydomain(self):
        self.cursor.execute("SELECT {} FROM {}".format(self.db_column1,self.db_table))
        output = self.cursor.fetchall()
        d_list = []
        for i in output:
            d_list.append(i[0])
        return d_list
    def querystatus(self, domain):
        self.cursor.execute("SELECT {} FROM {} WHERE {}=?".format(self.db_column2, self.db_table, self.db_column1), (str(domain),))
        output = self.cursor.fetchall()
        return output[0][0]
    def querydate(self, domain):
        self.cursor.execute("SELECT {} FROM {} WHERE {}=?".format(self.db_column3, self.db_table, self.db_column1), (str(domain),))
        output = self.cursor.fetchall()
        return output[0][0]
    def queryfc(self, domain):
        self.cursor.execute("SELECT {} FROM {} WHERE {}=?".format(self.db_column4, self.db_table, self.db_column1), (str(domain),))
        output = self.cursor.fetchall()
        return output[0][0]
    def updatefc(self):
        print(domain_forcecheck("d13579.com"))







test = Domain_c()
print(test.updatefc())