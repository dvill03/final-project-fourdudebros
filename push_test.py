# This is a simple test script to load a fixed item into the PostgreSQL database
# TODO generalize this so it will load any data passed in. 
# This will probably turn into a Python function

import psycopg2

sql = """INSERT INTO run1(event_name, coverage_name, cover_score) VALUES(%s, %s, %s) ;"""
conn = None

try:
    conn = psycopg2.connect(host="localhost",database="sarcix_test_db",user="postgres")
    cur = conn.cursor()

    value1 = "\"test_event_python0\""
    value2 =  "\"test_coverage_python0\""
    value3 = 0.75
    #print('PostgreSQL database version:')
    #cur.execute('SELECT version()')
    #db_version = cur.fetchone()
    #print(db_version)
    cur.execute(sql, (value1, value2, value3));
    conn.commit()
    cur.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
            
