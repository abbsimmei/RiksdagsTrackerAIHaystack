##################################
#
# Joakim Tips: Ha en annan AI i början som sammanfattar / Förkortar JSON filen för att minimera antalet Tokens
# Simon Tips: If I do the thing about I can pull the html document insted of .json which will give extra stuff :D
#
##################################



# Example: reuse your existing OpenAI setup
from openai import OpenAI
import requests
import json

memory = ""

##################################
#                                #
#          API Request           #
#                                #
##################################

url = "https://data.riksdagen.se/dokument/HC023020.json"

def requestApi(url):
    try:
        r = requests.get(url)
        s = r.text
        j = json.loads(s)
        return j
    except Exception as e:
        print(f"An error occurred: {e}")

##################################
#                                #
#            Memory              #
#                                #
##################################

def chatMemoryFunc(memory, answer):
    newMemory = "Du är en hjälpsam assisten som ska svara på frågor. Du kommer få kontext både på ett dokument och föredetta diskutioner och du ska använda detta för att ge bättre svar."

    newMemory = "Test"

    return newMemory

apiAnswer = requestApi(url)
print(apiAnswer)

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")



while True:
    print("---------------------------------------")
    question = input("Message to RiksdagsTracker GPT: ")
    print("\n")

    context = "Du är en hjälpsam assisten som ska svara på frågor angående detta JSON dokument: " + str(apiAnswer)

    completion = client.chat.completions.create(
    model="model-identifier",
    messages=[
        {"role": "system", "content": context},
        {"role": "user", "content": question}
    ],
    temperature=0.7,
    )
    answerMessage = completion.choices[0].message
    answerContent = answerMessage.content
    print("#####################")
    print("# RikdagsGPT Svarar #")
    print("#####################")
    print("\n")
    print(answerContent)
    print("\n")
    print("---------------------")




