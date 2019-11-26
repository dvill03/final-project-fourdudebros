# Program extracting all columns, row names and scores in Python script.
# All this does is read each row/column pair and the related score. 
# This will be integrated into loading the database.

import xlrd

loc = ("[insert path to this file]/analysis_530_firstpage.xlsx")

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

# For row 0 and column 0
# sheet.cell_value(0, 0)

for i in range(1, sheet.nrows):
    for j in range(1, sheet.ncols):
        print sheet.cell_value(0,j) + " " + sheet.cell_value(i, 0) + " " + str(sheet.cell_value(i, j))

