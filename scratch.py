import os

# Get the list of all files and directories
path = "/Users/peter/Desktop/Programming/budgeting_01"
dir_list = os.listdir(path)
print("dir_list:", dir_list)
stmts_pdf_list = []





files = fullpaths(dir_list, path)
print(files)

