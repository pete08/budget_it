# Obtain full paths of all PDFs in specific Directory
def fulldirpdffiles(list, dirPath):
    filesInScope = []
    for file in list:
        if file.find(".pdf") > 0:
            filesInScope.append(dirPath + "/" + file)
    return filesInScope

# Get stmt year: yyyy-mm, for future manipulation: trxnlist()
def formatstmtyear(filename):
    # show yyyy-mm, split in transactionList() to adjust yyyy per trxn mm
    stmtyear = filename[:6] 
    return stmtyear