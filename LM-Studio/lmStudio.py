# Example: reuse your existing OpenAI setup
from openai import OpenAI
import requests
import json

url = "https://data.riksdagen.se/dokument/HC023020.json"

def requestApi(url):
    try:
        r = requests.get(url)
        s = r.text
        j = json.loads(s)
        return j
    except Exception as e:
        print(f"An error occurred: {e}")

apiAnswer = requestApi(url)
print(apiAnswer)

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")



while True:
    question = input("Message to RiksdagsTracker GPT: ")

    completion = client.chat.completions.create(
    model="model-identifier",
    messages=[
        {"role": "system", "content": "Du är en hjälpsam assisten som ska svara på frågor angående detta JSON dokument: " + str(apiAnswer)},
        {"role": "user", "content": question}
    ],
    temperature=0.7,
    )

    print(completion.choices[0].message)



