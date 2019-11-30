import psycopg2
import xlrd
from psycopg2.extras import execute_values

def load(path, run_name):
    loc = (path)

    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)


    list_item = []
    list_conv = []
    # For row x and column y
    # sheet.cell_value(x, y)
    # Iterate through xlsx file and create a list with the key-pairs and scores
    for i in range(1, sheet.nrows):
        list_conv.append(sheet.cell_value(i,0))
        for j in range(1, sheet.ncols):
            #print sheet.cell_value(0,j) + " " + sheet.cell_value(i, 0) + " " + str(sheet.cell_value(i, j))
            list_conv.append(str(sheet.cell_value(i, j)))
        list_item.append((run_name,) + tuple(list_conv))
        list_conv = []
    """
    m = 0
    for k in range(len(list_item)):
         m += len(list_item[k])
         print(str(len(list_item)) + " ::: " + str(m))
    """
    conn = None

    try:
        conn = psycopg2.connect(host="localhost",database="sarcix_test_db",user="postgres", password="2345")
        cur = conn.cursor()
        execute_values(cur, """INSERT INTO naive(
                            run_name,
                            event_name,
                            b,
                            c,
                            d,
                            e,
                            f,
                            g,
                            h,
                            i,
                            j,
                            k,
                            l,
                            m,
                            n,
                            o,
                            p,
                            q,
                            r,
                            s,
                            t,
                            u,
                            v,
                            w,
                            x,
                            y,
                            z,
                            aa,
                            ab,
                            ac,
                            ad,
                            ae,
                            af,
                            ag,
                            ah,
                            ai,
                            aj,
                            ak,
                            al,
                            am,
                            an,
                            ao,
                            ap,
                            aq,
                            ar,
                            ass,
                            att,
                            au,
                            av
                       ) VALUES %s ON CONFLICT DO NOTHING;""", list_item)

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
