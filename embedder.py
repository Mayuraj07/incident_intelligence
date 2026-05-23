import openai
import os
import psycopg2
from dotenv import load_dotenv
from generate_narrative import generate_narrative
from incidents_loader import load_incidents

load_dotenv()

client= openai.OpenAI(api_key=os.getenv('OPEN_API_KEY'))

def get_connection():
    return psycopg2.connect(
        dbname='incidents_db', user='mayuri',
        password='password123', host='localhost'
    )


def embed_text(text):
    response = client.embeddings.create(
        model='text-embedding-3-small',
        input=text
    )
    return response.data[0].embedding

def embed_all_incidents():
    incidents = load_incidents('incidents.csv')
    conn = get_connection()
    cur = conn.cursor()

    for inc in incidents:
        narrative = generate_narrative(inc)
        embedding = embed_text(narrative)


        cur.execute('''
            INSERT INTO incidents (
                incident_id, description, source_system,
                category, root_cause, resolution,
                amount_impacted, status, narrative, embedding
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            inc['incident_id'], inc['description'], inc['source_system'],
            inc['category'], inc['root_cause'], inc['resolution'],
            float(inc['amt_impacted']), inc['status'],
            narrative, embedding
        ))
        print(f"Embedded and saved {inc['incident_id']}")

    conn.commit()
    cur.close()
    conn.close()
    print("All incidents embedded successfully.")

if __name__ == '__main__':
    embed_all_incidents()