##################################
#
# Joakim Tips: Ha en annan AI i början som sammanfattar / Förkortar JSON filen för att minimera antalet Tokens
# Simon Tips: If I do the thing about I can pull the html document insted of .json which will give extra stuff :D
#
##################################



# Example: reuse your existing OpenAI setup
from openai import OpenAI
from bs4 import BeautifulSoup
import requests
import json

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")



##################################
#          (outdated)            #
#           API JSON             #
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

apiAnswer = requestApi(url)
#print(apiAnswer)

##################################
#                                #
#            API HTML            #
#                                #
##################################

def requestApiHtml(url):
    try:
        r = requests.get(url)
        s = r.text
        return s
    except Exception as e:
        print(f"An error occurred: {e}")

urlHtml = "https://data.riksdagen.se/dokument/HC023020.html"
htmlApi = requestApiHtml(urlHtml)
#print (htmlApi)

# Function to remove tags
def remove_tags(html):

    # parse html content
    soup = BeautifulSoup(html, "html.parser")

    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()

    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)

apiHtmlAnswer = remove_tags(htmlApi)
#print(apiHtmlAnswer)

##################################
#                                #
#            Memory              #
#                                #
##################################

def chatMemoryFunc(memory, jsonDocument):
    newMemory = "Du är en hjälpsam och informativ assistent som ska svara på frågor baserat på innehållet i det givna dokumentet och tidigare diskussioner. Ditt främsta mål är att ge tydliga och faktabaserade svar som hämtas direkt från dokumentet och tidigare konversationer. All information som du presenterar ska vara strikt baserad på det som finns i det tillhandahållna dokumentet. Var noga med att ange att din information kommer från dokumentet och specificera vilka som har skrivit och ställt sig bakom dokumentet. Använd relevant kontext från tidigare frågor och svar för att ge djupare och mer precisa svar, när det är lämpligt. Avvik inte från informationen i dokumentet. Spekulativa eller hypotetiska svar ska undvikas. Här är Dokumentet: (" + str(jsonDocument) + "). Här är tidigare frågor och svar som du kan använda som kontext: (" + str(memory) + ")"
    return newMemory

def questAns(previous, question, answer):
    discussion = previous + " Användarens nästa Fråga var: (" + question + "). Och assistentens svar var: (" + answer + ")" 
    return discussion

##################################
#                                #
#             Chat               #
#                                #
##################################

memory = ""
while True:
    print("---------------------------------------")
    question = input("Message to RiksdagsTracker GPT: ")
    print("\n")

    #context = "Du är en hjälpsam assisten som ska svara på frågor angående detta JSON dokument: " + str(apiAnswer)
    context = chatMemoryFunc(memory, apiHtmlAnswer)
    #print("--------------")
    #print(context)
    #print("--------------")

    completion = client.chat.completions.create(
    model="model-identifier",
    messages=[
        {"role": "system", "content": context},
        {"role": "user", "content": question}
    ],
    #max_completion_tokens = 100,
    #max_tokens = 100,
    temperature=0.07,
    )
    answerMessage = completion.choices[0].message
    answerContent = answerMessage.content

    memory = questAns(memory, question, answerContent)
    #print("--------------")
    #print(memory)
    #print("--------------")

    print("#####################")
    print("# RikdagsGPT Svarar #")
    print("#####################")
    print("\n")
    print(answerContent)
    print("\n")
    print("---------------------")




