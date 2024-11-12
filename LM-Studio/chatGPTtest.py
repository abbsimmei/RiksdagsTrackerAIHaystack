from openai import OpenAI
import os
import requests
import json
from bs4 import BeautifulSoup

# Set your OpenAI API key (replace 'your-openai-api-key' with your actual key)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "sk-svcacct-hTXxZcWjaiaIrud_c7PeF0X5VhcKRhtFTDIWu-cTNmwwdFtuT9KPNSxMbZauzT3BlbkFJdotkr21ZFKr5fk9q8w8V4UAiQnFp1wHKZdqXEYnwJwlCE_doYA0Gf4S1whhoAA"))

##################################
#          API JSON              #
##################################

def requestApi(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure we get a valid response
        return response.json()
    except Exception as e:
        print(f"An error occurred: {e}")

url = "https://data.riksdagen.se/dokument/HC023020.json"
apiAnswer = requestApi(url)

##################################
#            API HTML            #
##################################

def requestApiHtml(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure we get a valid response
        return response.text
    except Exception as e:
        print(f"An error occurred: {e}")

urlHtml = "https://data.riksdagen.se/dokument/HC023020.html"
htmlApi = requestApiHtml(urlHtml)

# Function to remove tags from HTML
def remove_tags(html):
    soup = BeautifulSoup(html, "html.parser")
    for data in soup(['style', 'script']):
        data.decompose()
    return ' '.join(soup.stripped_strings)

apiHtmlAnswer = remove_tags(htmlApi)

##################################
#            Memory              #
##################################

def chatMemoryFunc(memory, jsonDocument):
    return (
        "Du är en hjälpsam och informativ assistent som ska svara på frågor baserat på innehållet i det givna dokumentet och tidigare diskussioner. "
        "Ditt främsta mål är att ge tydliga och faktabaserade svar som hämtas direkt från dokumentet och tidigare konversationer. All information som du presenterar "
        "ska vara strikt baserad på det som finns i det tillhandahållna dokumentet. Här är Dokumentet: ("
        + str(jsonDocument)
        + "). Här är tidigare frågor och svar som du kan använda som kontext: ("
        + str(memory)
        + ")"
    )

def questAns(previous, question, answer):
    return previous + f" Användarens nästa Fråga var: ({question}). Och assistentens svar var: ({answer})"

##################################
#             Chat               #
##################################

memory = ""
while True:
    print("---------------------------------------")
    question = input("Message to RiksdagsTracker GPT: ")
    print("\n")

    context = chatMemoryFunc(memory, apiHtmlAnswer)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": question}
        ],
        temperature=0.07
    )

    answerMessage = completion.choices[0].message
    answerContent = answerMessage.content

    memory = questAns(memory, question, answerContent)

    print("#####################")
    print("# RikdagsGPT Svarar #")
    print("#####################")
    print("\n")
    print(answerContent)
    print("\n")
    print("---------------------")
