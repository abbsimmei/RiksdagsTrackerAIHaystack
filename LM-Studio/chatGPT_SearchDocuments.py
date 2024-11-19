#####################
#
# 1. Lyssna på vad användaren letar efter
# 2. Ta fram en url som hittar dessa
# 3. Fetcha svaret från api'n
# 4. Sammanställ svaret.
# 
# 5. Kunna fetcha ett svar.
# 6. Kunna sammanfatta det.
#
# 6. Leta vidare efter andra förslag, gå tillbaka till 2
#
#
#
#

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


##################################
#            Memory              #
##################################

def chatContextFunc(id):
    if id == 1:
        return ("Du är en hjälpsam assisten som ska söka igenom en databas över Riksdagen. Användaren kommer ställa dig en fråga till dig för att hitta ett dokument"
            " som användaren vill hitta. Det måste inte vara ett specifikt dokument utan användaren kan också bara vilja hitta ett dokument om ett visst ämne."

            " För att hitta dessa dokument har du tillgång till denna URL: https://data.riksdagen.se/dokumentlista/?sok=[Sökord]&doktyp=[dokumenttyp]&from=[Från datum]&tom=[till datum]&sort=rel&utformat=json&a=s#soktraff"
            " [sökord] ska du bytta ut mot huvud ord av det använderan letar efter. Till exemple flyg eller miljön. Du ska bara ha med huvud ord och inga konjuktioner."
            " [dokumenttyp] ska du bytta ut mot en dokumenttyp som användare letar efter. Du har tillgång till betänkande (bet), Motion (mot), Votering (votering), Skriftlig fråga (fr) och Proposition (prop)"
            " [Från datum] och [till datum] ska du bytta ut mot datum som användaren letar efter."
            " Om filtret inte är relevant för användarens fråga ska det lämnas tomt. Det vill säga utan [exemple]"
            " Slutligen vill jag att du ger användaren länken så att den kan söka efter det den vill."
            " Du ska bara svara med länken! Inget annat!"
        )
    elif id == 2:
        return ("Du är en hjälpsam assisten som ska hjälpa en användare att söka igenom Riksdagens databas. Vid detta tillfälle har vi fått ett svar av Riksdagens api"
                "Du kommer få tillgång till svaret och ska sammanställa det på ett snyggt sätt för användaren. Jag vill att all relevant data ska visas. Du ska också efter varje träff hänvisa till dess html url så att användaren kan läsa mer.")



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

    context = chatContextFunc(1)

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

    #memory = questAns(memory, question, answerContent)

    apiAnswer = requestApi(answerContent)

    print("#####################")
    print("#     API answer    #")
    print("#####################")
    print("\n")
    print(apiAnswer)
    print("\n")
    print("---------------------")
    print("\n")

    context2 = chatContextFunc(2)

    context2 = context2 + " Api svaret var: " + str(apiAnswer)

    completion2 = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": context2},
            {"role": "user", "content": "Sammanställ datan"}
        ],
        temperature=0.07
    )

    answerMessage2 = completion2.choices[0].message
    answerContent2 = answerMessage2.content

    print("#####################")
    print("#  Sammanställning  #")
    print("#####################")
    print("\n")
    print(answerContent2)
    print("\n")

