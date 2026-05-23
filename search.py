import psycopg2
from psycopg2.extras import RealDictCursor
from embedder import embed_text

def get_connection():
    return psycopg2.connect(
        dbname='incidents_db', user='mayuri',
        password='password123', host='localhost'
    )

def find_similar_incidents(query_text, top_n=5):
    query_embedding = embed_text(query_text)

    conn = get_connection()
    cur = conn.cursor(cursor_factory = RealDictCursor)
    
    cur.execute('''
        SELECT incident_id, description, root_cause, resolution,
               1 - (embedding <=> %s::vector) AS similarity
        FROM incidents
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    ''', (query_embedding, query_embedding, top_n))
    
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

if __name__ == '__main__':
    results = find_similar_incidents('SWIFT feed late, nostro mismatch 2M')
    for r in results:
        print(r['incident_id'], '-', r['description'])
        print('Similarity:', round(r['similarity'], 4))
        print('Root cause:', r['root_cause'])
        print('Resolution:', r['resolution'])
        print()