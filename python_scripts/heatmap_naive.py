import psycopg2
import xlrd
from psycopg2.extras import execute_values
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

data = np.random.rand(4, 6)

#heat_map = sb.heatmap(data)

#plt.show()

lmany = []

conn = None

try:
    conn = psycopg2.connect(host="localhost",database="sarcix_test_db",user="test_user0")
    cur = conn.cursor()
    cur.execute("""SELECT * INTO TempTable FROM naive;
                ALTER TABLE TempTable DROP COLUMN "event_name";
                SELECT * FROM TempTable;""")
    #cur.execute("SELECT * FROM naive;")
    print("The number of parts: ", cur.rowcount)
    str_lst= cur.fetchall()
    #print(str_lst[0])
    #print(type(str_lst[0])) 
    c_lst = []
    d_lst = []
    for i in range(len(str_lst)):
        for j in range(len(str_lst[i])):
            d_lst.append(float(str_lst[i][j]))
        c_lst.append(tuple(d_lst))
        d_lst.clear()
    
    print(type(c_lst[0][46]))
    
    heat_map = sb.heatmap(c_lst)
    plt.show()

    #conn.commit()
    cur.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
