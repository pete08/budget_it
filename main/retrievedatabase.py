import mysql.connector
import pandas as pd

# Populate MySql
# Output to MySql table 'cred_spend_practice': Part 1of2

class RetrievDB:
    def __init__(self, user="root", password="", host="127.0.0.1", database="sampledb"):
        self.user  = user
        self.password = password
        self.host = host
        self.database  = database
        try:
            self.cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
            self.cursor = self.cnx.cursor()
        except mysql.connector.Error as err:
            print("Eror-code:", err.errno)
            print("Eror-message: {}".format(err.msg))

    def popccspendtable(self, df, ccspendtable="cred_spend_practice"):
        # test idea: 
        #   1. confirm df contains 6 column names: Month, Year, YearMonth, Date, Description, Amount
        query_add_cred_spend = ("""INSERT INTO {} (Month, Year, YearMonth, Date, Description, Amount) VALUES (%s, %s, %s, %s, %s, %s)""").format(ccspendtable)
        # delete current pop table
        self.cursor.execute("""delete from {};""".format(ccspendtable))
        #Output to MySql table 'cred_spend': Part 2of2 - Insert trxns list row by row
        for index, row in df.iterrows():
            self.cursor.execute(query_add_cred_spend, [row.Month, row.Year, row.YearMonth, row.Date, row.Description, row.Amount])    
        self.cnx.commit()
        self.cursor.close()
        self.cnx.close()

    def df_with_pd(self, table="cred_spend_practice"):
        df = pd.read_sql("""SELECT * FROM {}""".format(table), con=self.cnx)
        self.cursor.close()
        self.cnx.close()
        return df


cc_spend = RetrievDB()
df_cc_spend = cc_spend.df_with_pd()
print("This here's shape of the table:", df_cc_spend.shape)
print("This here's the table:!:!:\n", df_cc_spend)

