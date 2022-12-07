# # LIST of Interest:
    # # [ ] 1 - Cateogrical spend: Machine learning 
    # # [ ] 2 - Cateogrical spend: categorical spend pie graph 

import pdfplumber
import pandas as pd
import re
import os
import datetime
import matplotlib.pyplot as plt
import mysql.connector
import fullfilelistpdf
import pullpagestrxns
import retrievedatabase

# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)

# Get date
today = datetime.datetime.today().strftime("%Y-%m-%d %H:%M")
mm = datetime.datetime.today().strftime("%m")
current_yr_mm = datetime.datetime.today().strftime("%Y-%m")
# Get the list of all stmts and directories
stmtpath = "/Users/peter/Desktop/Programming/budget_it/stmts"
outputpath = "/Users/peter/Desktop/Programming/budget_it"
outputfilename = "spendcsv_{}.csv".format(today)
dir_list = os.listdir(stmtpath)
# Database variables:
db_inscope = {"user": "root", "password": "", "host": "127.0.0.1", "database": "sampledb", "table": "cred_spend_practice"}

stmts = fullfilelistpdf.fulldirpdffiles(dir_list,stmtpath)

list_full_pop = []  
for filepath in stmts:
    with pdfplumber.open(filepath) as pdf:
        print("### newfile: ### extracting trxns from:", filepath)
        filename = filepath.split("/")[-1]
        # Get stmt year
        stmtyear = fullfilelistpdf.formatstmtyear(filename) # import fullfilelistpdf.py > formatstmtyear(filename)
        list_of_transactions = pullpagestrxns.whichpages(pdf, stmtyear) # import pullpagestrxns.py > whichpages(pdf, stmtyear)
        list_full_pop = list_full_pop + list_of_transactions

txnsdf = pd.DataFrame(list_full_pop, columns=(["Month", "Year", "YearMonth", "Date", "Description", "Amount"]))
print("txnsdf.shape == (rows, columns): ", txnsdf.shape)

# Remove pmts from DF
df = txnsdf[txnsdf["Amount"] > 0]
# scrap current mm's transactions: spend NOT complete
df = df[df['YearMonth'] != current_yr_mm]

#Output df to csv
df.to_csv((outputpath + "/" + outputfilename))

# # Populate MySql
# # Output to MySql table 'cred_spend_practice': Part 1of2
# try:
#     cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='sampledb')
#     cursor = cnx.cursor()
#     query_add_cred_spend_practice = ("""INSERT INTO cred_spend_practice (Month, Year, YearMonth, Date, Description, Amount)
#     VALUES (%s, %s, %s, %s, %s, %s)""")
#     #Output to MySql table 'cred_spend_practice': Part 2of2 - Insert the rows
#     for index, row in df.iterrows():
#         cursor.execute(query_add_cred_spend_practice, [row.Month, row.Year, row.YearMonth, row.Date, row.Description, row.Amount])    
#     cnx.commit()
# except mysql.connector.Error as err:
#     print("Eror-code:", err.errno)
#     print("Eror-message: {}".format(err.msg))
# finally:
#     cursor.close()
#     cnx.close()

dbtable = retrievedatabase.RetrievDB(user = db_inscope["user"], password = db_inscope["password"], host = db_inscope["host"], database = db_inscope["database"])
dbtable.popccspendtable(df, ccspendtable=db_inscope["table"])



# # group by Month, Year, Date
# df_group_mo_yr = df.groupby(["YearMonth"])["Amount"].sum()
# # convert columns to df
# df_group_mo_yr = pd.DataFrame({'YearMonth':df_group_mo_yr.index, 'Amount':df_group_mo_yr.values})

# print(df_group_mo_yr)
# df_group_mo_yr.plot.bar("YearMonth",'Amount', rot=0)
# plt.xlabel('Month')
# plt.ylabel('Amount Spent')
# plt.title('CC Spend past Year')
# plt.yticks(range(500,int(max(df_group_mo_yr['Amount'])+500), 500))
# plt.show()
