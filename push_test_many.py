# This script will read the xlsx file and push to the database.
# For now it is using a naive solution. Performance enhancements to come.  

import psycopg2
import xlrd

loc = ("[insert path to this file]t/analysis_530_firstpage.xlsx")

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

# For row 0 and column 0
# sheet.cell_value(0, 0)
list_item = []
value1 = ""
value2 = ""
value3 = ""
#for i in range(1, sheet.nrows):
#    for j in range(1, sheet.ncols):
#        #print sheet.cell_value(0,j) + " " + sheet.cell_value(i, 0) + " " + str(sheet.cell_value(i, j))
#        list_item.append((str(sheet.cell_value(0,j)), str(sheet.cell_value(i, 0)), str(sheet.cell_value(i, j))))


sql = """INSERT INTO run1(event_name, coverage_name, cover_score) VALUES(%s, %s, %s) ;"""
conn = None

try:
    conn = psycopg2.connect(host="localhost",database="sarcix_test_db",user="postgres")
    cur = conn.cursor()
    for i in range(1, sheet.nrows):
        for j in range(1, sheet.ncols):
            #print sheet.cell_value(0,j) + " " + sheet.cell_value(i, 0) + " " + str(sheet.cell_value(i, j))
            value1 = str(sheet.cell_value(0,j))
            value2 = str(sheet.cell_value(i, 0))
            value3 = str(sheet.cell_value(i, j))
    #print('PostgreSQL database version:')
    #cur.execute('SELECT version()')
    #db_version = cur.fetchone()
    #print(db_version)
            cur.execute(sql,(value2, value1, value3));
            conn.commit()
    cur.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
            
