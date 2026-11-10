from embeddings import model
import sqlite3
import numpy as np
from google import genai
import os
from groq import Groq

while True:
    
    prompt = input("Ask retrival : ")
    if prompt == ".quit":
        break
    ans = model(prompt) # right now it should be less 2200 words

    # now cosine similarity, we will use for loop
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    rows = cur.execute("SELECT embedding, id FROM notes")
    list = []
    for row in rows:
        vector = np.frombuffer(row[0], dtype=np.float32)
        id = row[1]
        simi = np.dot(ans, vector)/(np.linalg.norm(ans)*np.linalg.norm(vector))
        if(simi > 0.3):
            list.append((simi, id))
    list.sort(reverse = True)
    list = list[:5]
    strings = []
    for priority, i_d in list:
        rows = cur.execute("SELECT body FROM notes WHERE id = ?",(i_d,) )
        for row in rows:
            Text = row[0]
            strings.append(Text)
            print(f"priority value {priority} and String is {Text}")
    User_question = prompt
    Instruction = "Use the context if it’s relevant. If it isn’t, answer from your general knowledge, and say which one you used."
    string = ", ".join(strings)
    

    Augmented_query = User_question + "\n" + "\n" + Instruction + "\n" + string

    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def genrate(augmented_query):
        response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
           {"role": "user", "content": augmented_query}
        ], temperature=0.4, max_tokens=250
    )
        return response.choices[0].message.content

    print(genrate(Augmented_query))
    
