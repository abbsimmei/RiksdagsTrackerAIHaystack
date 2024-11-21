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
#          Functions             #
##################################

def extract_text_between(text: str, start: str, end: str) -> str:
    try:
        start_index = text.index(start) + len(start)
        end_index = text.index(end, start_index)
        return text[start_index:end_index]
    except ValueError:
        # Return an empty string if 'start' or 'end' is not found, or if they are in the wrong order.
        return ""



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

def chatContextFunc(id, apiAnswer):
    if id == 1:
        return ("Du är en hjälpsam assisten som ska söka igenom en databas över Riksdagen. Användaren kommer ställa dig en fråga till dig för att hitta ett dokument"
        " som användaren vill hitta. Det måste inte vara ett specifikt dokument utan användaren kan också bara vilja hitta ett dokument om ett visst ämne."

        " För att hitta dessa dokument har du tillgång till denna URL: https://data.riksdagen.se/dokumentlista/?sok=[Sökord]&doktyp=[dokumenttyp]&from=[Från datum]&tom=[till datum]&sort=rel&utformat=json&a=s#soktraff"
        " [sökord] ska du bytta ut mot huvud ord av det använderan letar efter. Till exemple flyg eller miljön. Du ska bara ha med huvud ord och inga konjuktioner."
        " [dokumenttyp] ska du bytta ut mot en dokumenttyp som användare letar efter. Du har tillgång till betänkande (bet), Motion (mot), Votering (votering), Skriftlig fråga (fr) och Proposition (prop)"
        " [Från datum] och [till datum] ska du bytta ut mot datum som användaren letar efter."
        " Om filtret inte är relevant för användarens fråga ska det lämnas tomt. Det vill säga utan [exempel]"

        " När du har tagit fram en url vill jag att du svara med: [url:lägg url'n här.:url]")
    elif id == 2:
        return ("Du är en hjälpsam assisten som ska hjälpa en användare att söka igenom Riksdagens databas. Vid detta tillfälle har vi fått ett svar av Riksdagens api"
        "Du kommer få tillgång till svaret och ska sammanställa det på ett snyggt sätt för användaren. Jag vill att all relevant data ska visas. Du ska inte visa url'ens utan istället ska du erbjuda dig att berätta mer om varje sak."
        "Här är svaret från api'n som du ska förkorta " + str(apiAnswer))
        
    
def questAns(previous, question, answer, apiAnswer):
    return previous + f"Användarens nästa Fråga var: ({question}). Och assistentens svar var: ({answer}). Api svar som du nu har tillgång till: ({apiAnswer})"

##################################
#           Chat Func            #
##################################

async def createURLsearch(question):
    context = chatContextFunc(1,"")

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

    url = extract_text_between(answerContent, "url:", ":url")

    if url != "":
        apiAnswer = await requestApi(url)

    return apiAnswer

def shortenAnswer(thingToShorten):
    context = chatContextFunc(2,thingToShorten)
    question = "Snälla sammanställ svaret från API'n"
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

    return answerContent


##################################
#             Chat               #
##################################

while True:

    question = input("Message to RiksdagsTracker GPT: ")

    answerContent = createURLsearch(question)
    print(answerContent)
    shortenedAnswer = shortenAnswer(answerContent)

    print(shortenedAnswer)



