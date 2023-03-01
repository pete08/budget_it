# # LIST of Interest:
    # # [ ] 1 - Cateogrical spend: Machine learning 
    # # [ ] 2 - Cateogrical spend: categorical spend pie graph 

import pdfplumber
import pandas as pd
import re
import os
import datetime
import matplotlib.pyplot as plt
import fullfilelistpdf
import pullpagestrxns
import retrievedatabase
import plot_spend_graph

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

# Input to mysql db.table
dbtable = retrievedatabase.RetrievDB(user = db_inscope["user"], password = db_inscope["password"], host = db_inscope["host"], database = db_inscope["database"])
dbtable.popccspendtable(df, ccspendtable=db_inscope["table"])

# display new df's graph using "plot_spend_graph.py" or call in terminal with newly created pop csv
plot_spend_graph.plotspend(df)