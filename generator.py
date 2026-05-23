import openai
import os
from dotenv import load_dotenv
from search import find_similar_incidents

load_dotenv()

client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def investigate(query_text):
    similar = find_similar_incidents(query_text)

    context = ''
    for inc in similar:
        context += f"Past case: {inc['description']}\n"
        context += f"Root cause: {inc['root_cause']}\n"
        context += f"Resolution: {inc['resolution']}\n\n"
    
    prompt = f'''
    You are a banking operations expert.
    A new incident has been reported: {query_text}
    
    Here are 5 similar past incidents:
    {context}
    Based on these, suggest:
    1. Most likely root cause
    2. First 3 investigation steps
    3. Likely resolution
    '''
    
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': prompt}]
    )
    
    return response.choices[0].message.content


if __name__ == '__main__':
    query = 'SWIFT feed not received, nostro balance off by 1.8M'
    print('Query:', query)
    print()
    result = investigate(query)
    print(result)