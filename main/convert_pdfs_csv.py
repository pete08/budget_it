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

# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)

# Get date
today = datetime.datetime.today().strftime("%Y-%m-%d %H:%M")
mm = datetime.datetime.today().strftime("%m")
current_yr_mm = datetime.datetime.today().strftime("%Y-%m")
# Get the list of all files and directories
stmtpath = "/Users/peter/Desktop/Programming/budget_it/stmts"
outputpath = "/Users/peter/Desktop/Programming/budget_it"
outputfilename = "spendcsv_{}.csv".format(today)

# # Obtain full paths of all PDFs in specific Directory
# def fulldirpdffiles(list, dirPath):
#     filesInScope = []
#     for file in list:
#         if file.find(".pdf") > 0:
#             filesInScope.append(dirPath + "/" + file)
#     return filesInScope

# # Create list of transactions from exerpt from PDF of
# def transactionList(list, stmtyear):
#     stmtyearint = int(stmtyear[:4])
#     stmtmo = stmtyear[4:]
#     list_of_lines = []
#     for line in list:
#         if len(line) > 16 and line.find("/") == 2 and re.search("\d[.]\d\d$",line):
#             # Prep empty list, to then append Transaction deets
#             trxn_line_split = []
#             # Initial Transaction split in 2: date, descr_amt
#             regexsearch = re.search("[/]\d\d\s{3}",line)
#             date, descr_amt = line[:5], line[regexsearch.span()[1]:]
#             # Append "Month" to trxn_line_split
#             trxn_line_split.append(date[0:2])
#             if date[0:2] == "12" and stmtmo == "01":
#                 # Append "Year"
#                 trxn_line_split.append(stmtyearint-1)
#                 # Append "Year-Mo"
#                 trxn_line_split.append(str(stmtyearint-1) + "-" + date[0:2])
#             else:
#                 # Append "Year"
#                 trxn_line_split.append(stmtyearint)
#                 # Append "Year-Mo"
#                 trxn_line_split.append(str(stmtyearint) + "-" + date[0:2])
#             # Append "Date"
#             trxn_line_split.append(date)
#             # split txn's Description and Amount
#             amt_indx = descr_amt.rfind(" ")
#             # Find then Append "Description"
#             descript = descr_amt[0:amt_indx]
#             trxn_line_split.append(descript)
#             # Find then Append "Amount"
#             print("extracting amount from:\n{}".format(descr_amt))
#             print("as part of:\n{}".format(line))
#             amount = float(descr_amt[(amt_indx+1):].replace(',',''))
#             trxn_line_split.append(amount)
#             # Append new transaction line to Trxn Population
#             list_of_lines.append(trxn_line_split)
#     return list_of_lines

# # Obtain pages that contain "$ Amount",
# # Gather all Transactions into single list
# def whichpages(pdf, stmtyear):
#     list_of_txn_pages = []
#     list_of_txns=[]
#     for x in range(len(pdf.pages)):
#         # print("reader_page index number:", x)
#         page_text = pdf.pages[x].extract_text()
#         if page_text.find("$ Amount") > 0:
#             # print("reader_page index number: {} . Extracted page_text:   ".format(x), page_text)
#             page_text_pre = page_text[(page_text.find("$ Amount")+ len("$ Amount")):]
#             page_text_pre = page_text_pre.splitlines()
#             page_inscope = []
#             for line in page_text_pre:
#                 trxn_line = re.findall("\d\d[/]\d\d\s{3}", line)
#                 if len(trxn_line) > 0:
#                     page_inscope.append(line)
#             print("page_iscope: {0}, page_inscope contains trxn count of    : {1}".format(x, len(page_inscope)))
#             trxnslist = transactionList(page_inscope, stmtyear)
#             list_of_txns = list_of_txns + trxnslist
#     return list_of_txns

# # Get stmt year: yyyy-mm, for future manipulation: trxnlist()
# def formatstmtyear(filename):
#     # show yyyy-mm, split in transactionList() to adjust yyyy per trxn mm
#     stmtyear = filename[:6]
#     return stmtyear

dir_list = os.listdir(stmtpath)
files = fullfilelistpdf.fulldirpdffiles(dir_list,stmtpath) # import fullfilelistpdf.py > fulldirpdffiles(list, path)

# [ ] - 6am 2022-12-06: Start importing dependency functions

list_full_pop = []  
for filepath in files:
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

#Output df to csv
df.to_csv((outputpath + "/" + outputfilename))

# group by Month, Year, Date
df_group_mo_yr = df.groupby(["YearMonth"])["Amount"].sum()
# convert columns to df
df_group_mo_yr = pd.DataFrame({'YearMonth':df_group_mo_yr.index, 'Amount':df_group_mo_yr.values})

print(df_group_mo_yr)
df_group_mo_yr.plot.bar("YearMonth",'Amount', rot=0)
plt.xlabel('Month')
plt.ylabel('Amount Spent')
plt.title('CC Spend past Year')
plt.yticks(range(500,int(max(df_group_mo_yr['Amount'])+500), 500))
plt.show()
