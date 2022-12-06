import re

# Create list of transactions from exerpt from PDF
def transactionList(list, stmtyear):
    stmtyearint = int(stmtyear[:4])
    stmtmo = stmtyear[4:]
    list_of_lines = []
    for line in list:
        if len(line) > 16 and line.find("/") == 2 and re.search("\d[.]\d\d$",line):
            # Prep empty list, to then append Transaction deets
            trxn_line_split = []
            # Initial Transaction split in 2: date, descr_amt
            regexsearch = re.search("[/]\d\d\s{3}",line)
            date, descr_amt = line[:5], line[regexsearch.span()[1]:]
            # Append "Month" to trxn_line_split
            trxn_line_split.append(date[0:2])
            if date[0:2] == "12" and stmtmo == "01":
                # Append "Year"
                trxn_line_split.append(stmtyearint-1)
                # Append "Year-Mo"
                trxn_line_split.append(str(stmtyearint-1) + "-" + date[0:2])
            else:
                # Append "Year"
                trxn_line_split.append(stmtyearint)
                # Append "Year-Mo"
                trxn_line_split.append(str(stmtyearint) + "-" + date[0:2])
            # Append "Date"
            trxn_line_split.append(date)
            # split txn's Description and Amount
            amt_indx = descr_amt.rfind(" ")
            # Find then Append "Description"
            descript = descr_amt[0:amt_indx]
            trxn_line_split.append(descript)
            # Find then Append "Amount"
            print("extracting amount from:\n{}".format(descr_amt))
            print("as part of:\n{}".format(line))
            amount = float(descr_amt[(amt_indx+1):].replace(',',''))
            trxn_line_split.append(amount)
            # Append new transaction line to Trxn Population
            list_of_lines.append(trxn_line_split)
    return list_of_lines

# Input pdf, Obtain pages that contain "$ Amount": 
#   (1) split each pagline, 
#   (2) create raw list of unparsed Transactions (Trxns) lines
#   (3) TransactionList(): parse each raw line into 5 item lines: 
#       [date, year, year-mo, description, amount]
#   (4) append parsed Trxn lines into single list
def whichpages(pdf, stmtyear):
    list_of_txn_pages = []
    list_of_txns=[]
    for x in range(len(pdf.pages)):
        # print("reader_page index number:", x)
        page_text = pdf.pages[x].extract_text()
        if page_text.find("$ Amount") > 0:
            # print("reader_page index number: {} . Extracted page_text:   ".format(x), page_text)
            page_text_pre = page_text[(page_text.find("$ Amount")+ len("$ Amount")):]
            page_text_pre = page_text_pre.splitlines()
            page_inscope = []
            for line in page_text_pre:
                trxn_line = re.findall("\d\d[/]\d\d\s{3}", line)
                if len(trxn_line) > 0:
                    page_inscope.append(line)
            print("page_iscope: {0}, page_inscope contains trxn count of    : {1}".format(x, len(page_inscope)))
            trxnslist = transactionList(page_inscope, stmtyear)
            list_of_txns = list_of_txns + trxnslist
    return list_of_txns