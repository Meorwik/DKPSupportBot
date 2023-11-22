from psycopg2 import connect
from psycopg2.extras import RealDictCursor


config = "postgres://postgres:FE4gfEBc52E54D55BE3gb63bFCFC3bGF@monorail.proxy.rlwy.net:40830/railway"

connection = connect(config)
cursor = connection.cursor(cursor_factory=RealDictCursor)

sql = """
ALTER SEQUENCE medication_schedule_id_seq RESTART WITH 1;
"""

cursor.execute(sql)
connection.commit()
connection.close()
