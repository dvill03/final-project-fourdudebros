# This script inserts the entire run from an xlsx file. 
# The speed is very fast. From several minutes to a few seconds using by using execute_values.

import xlrd
from App.models import Run
from django.conf import settings

loc = (settings.BASE_DIR + "/Runs/analysis_530_firstpage.xlsx")

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)


#list_item = []

# For row x and column y
# sheet.cell_value(x, y)
# Iterate through xlsx file and create a list with the key-pairs and scores 
for i in range(1, sheet.nrows):
    for j in range(1, sheet.ncols):
        #print sheet.cell_value(0,j) + " " + sheet.cell_value(i, 0) + " " + str(sheet.cell_value(i, j))
        r = Run(sheet.cell_value(i,0), sheet.cell_value(0,j), sheet.cell_value(i, j))
        r.save()


#conn = None

#try:
#    conn = psycopg2.connect(host="localhost",dbname="sarcix_test_db",user="postgres", password="2345")
#    cur = conn.cursor()
#    execute_values(cur, "INSERT INTO run1(event_name, coverage_name, score) VALUES %s ON CONFLICT DO NOTHING;",list_item)
#
#   conn.commit()
#    cur.close()
#except (Exception, psycopg2.DatabaseError) as error:
#    print(error)
#finally:
#    if conn is not None:
#        conn.close()
            
