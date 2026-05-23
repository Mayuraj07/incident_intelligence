import psycopg2

conn = psycopg2.connect(
    dbpython create_table.pyname ='incidents_db',
    user = 'mayuri',
    password = 'password123',
    host = 'localhost'
)

cur = conn.cursor()

cur.execute('CREATE EXTENSION IF NOT EXISTS vector;')

cur.execute('''
    CREATE TABLE IF NOT EXISTS incidents (
        id SERIAL PRIMARY KEY,
        incident_id TEXT,
        description TEXT,
        source_system TEXT,
        category TEXT,
        root_cause TEXT,
        resolution TEXT,
        amount_impacted NUMERIC,
        status TEXT,
        narrative TEXT,
        embedding vector(1536)
    )
''')

conn.commit()
cur.close()
conn.close()

print('✅ Table created successfully')
