import psycopg2
import xlrd
from psycopg2 import sql
from psycopg2.extras import execute_values
import numpy as np
import seaborn as sb
import matplotlib
matplotlib.use('Agg')      #type of renderer
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def getRunHeatmap(run_name):
    lmany = []
    conn = None

    try:
        conn = psycopg2.connect(host="localhost",database="sarcix_test_db",user="postgres", password="2345")
        cur = conn.cursor()
        cur.execute("""SELECT * INTO TempTable FROM naive WHERE run_name = %s;
                    ALTER TABLE TempTable DROP COLUMN "event_name", DROP "run_name";
                    SELECT * FROM TempTable;""", (run_name,))
        #print("The number of parts: ", cur.rowcount)
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

        #heat_map = sb.heatmap(c_lst, annot=True, linewidths=.5)
        fig, axis = plt.subplots()
        heatmap = axis.pcolor(c_lst) # heatmap contient les valeurs
        plt.colorbar(heatmap)

        #plt.show()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    #get uri
    buf = BytesIO()
    plt.savefig(buf, format='png') # instead of plt.show(), save figure in buffer
    fig_png = base64.b64encode(buf.getvalue()).decode()
    buf.close()
    return fig_png;
