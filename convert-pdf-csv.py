# Import the required Module
from PyPDF2 import PdfReader
import pandas as pd
import re
import os
 

pd.set_option('display.max_columns', None)


# Get the list of all files and directories
path = "/Users/peter/Desktop/Programming/budgeting_01"


# Obtain full paths of all PDFs in specific Directory
def fullpaths(list, dirPath):
    filesInScope = []
    for file in list:
        if file.find(".pdf") > 0:
            filesInScope.append(dirPath + "/" + file)
    return filesInScope

# Create list of transactions from exerpt from PDF of
def transactionList(list):
    list_of_lines = []
    for line in list:
        if len(line) > 16 and line.find("/") == 2:
            line_split = []
            split_Date_DescrAmt = re.split("\s{5}", line)
            # Append "Month"
            line_split.append(split_Date_DescrAmt[0][0:2])
            # Append "Date"
            line_split.append(split_Date_DescrAmt[0])
            # split txn's Description and Amount
            amt_indx = split_Date_DescrAmt[1].rfind(" ")
            # Find then Append "Description"
            descript = split_Date_DescrAmt[1][0:amt_indx]
            line_split.append(descript)
            # Find then Append "Amount"
            amount = float(split_Date_DescrAmt[1][(amt_indx+1):].replace(',',''))
            line_split.append(amount)
            # Append new transaction line to population
            list_of_lines.append(line_split)
    return list_of_lines

# Obtain pages that contain "$ Amount", 
# Gather all Transactions into single list
def whichpages(reader_pages, list_of_txns=[]):
    list_of_txn_pages = []
    for x, i in enumerate(reader_pages):
        i = i.extract_text()
        amt_indctr = i.find("$ Amount")
        if amt_indctr > 0:
            list_of_txn_pages.append(x)
            page_inscope = i[amt_indctr:]
            page_inscope = page_inscope.splitlines()
            trxnslist = transactionList(page_inscope)
            list_of_txns = list_of_txns + trxnslist
    return list_of_txns




# # Read a PDF File
# def txnsindir(dir_list):
#     list_full_pop = []    
#     for file in dir_list:
#         try:
#             reader = PdfReader(file)
#             reader_pages = reader.pages
#             pagelength = len(reader.pages)
#         except Exception as e:
#             print('The Error is', e)
#         list_of_transactions = whichpages(reader_pages)
#         list_full_pop.append(list_of_transactions)
#         print("lenght of current pdf: len(list_of_transactions):", len(list_of_transactions))
#         print("length of current pop: len(list_full_pop): ", len(list_full_pop))
#     return list_full_pop

dir_list = os.listdir(path)
files = fullpaths(dir_list,path)


list_full_pop = []  
for filepath in files:
    print("############## new file: #################")
    print("Current file extracting trxns from:", filepath)
    try:
        reader = PdfReader(dir_list[0])
        reader_pages = reader.pages
        pagelength = len(reader.pages)
    except Exception as e:
        print('The Error is', e)
    list_of_transactions = whichpages(reader_pages)
    list_full_pop = list_full_pop + list_of_transactions
    print("Length of list for current file", list_of_transactions)
    print("Length of population:", len(list_full_pop))


# add_stmts = txnsindir(dir_list)

txnsdf = pd.DataFrame(list_full_pop, columns=(["Month", "Date", "Description", "Amount"]))
print("txnsdf.shape == (rows, columns): ", txnsdf.shape)

# Remove pmts from DF
df = txnsdf[txnsdf["Amount"] > 0]
print(df)


# [ ] - DNLD ALL STMTS 
# [ ] - Re-Run to create 12 month statement trxn Graph
# [ ] - Group by month 
# [ ] - Create Graph of spend per Month --- matplotlab
# [ ] - Add to github
# OPTIONAL [ ] - Add Year: get yr as arg in:
#                   whichpages(reader_pages, list_of_txns=[]
#                   transactionList(list, +yr) 
#                   add "year" to each row
#                   add "Year" in df columns b/n Month, Date
# 
# OPTIONAL [ ] - Make DF For each month
