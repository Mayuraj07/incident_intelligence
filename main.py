import openai
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from generator import investigate
from search import find_similar_incidents

load_dotenv()

app = FastAPI()

def get_connection():
    return psycopg2.connect(
        dbname ='incidents_db',user ='mayuri',
        password ='password123', host ='loaclhost'
    )
class IncidentQuery(BaseModel):
    description: str

@app.post('/investigate')
def investigate_incident(query: IncidentQuery):
    result = investigate(query.description)
    similar = find_similar_incidents(query.description)
    return {
        'investigation': result,
        'similar_incidents' : [dict(r) for r in similar]
    }

@app.get('/incidents')
def list_incidents():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT incident_id, description, category, status FROM incidents')
    results = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(r) for r in results]

@app.get('/health')
def health():
    return {'status':'ok'}
