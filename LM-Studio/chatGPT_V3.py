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
#           "Memory"             #
##################################

def chatContextFunc(id, apiAnswer, fdFragor):
    if id == 1:
        return ("Du är en hjälpsam assisten som ska söka igenom en databas över Riksdagen. Användaren kommer ställa dig en fråga till dig för att hitta ett dokument"
        " som användaren vill hitta. Det måste inte vara ett specifikt dokument utan användaren kan också bara vilja hitta ett dokument om ett visst ämne."

        " För att hitta dessa dokument har du tillgång till denna URL: https://data.riksdagen.se/dokumentlista/?sok=[Sökord]&doktyp=[dokumenttyp]&from=[Från datum]&tom=[till datum]&sort=rel&utformat=json&p=1&a=s#soktraff"
        " [sökord] ska du bytta ut mot huvud ord av det använderan letar efter. Till exemple flyg eller miljön. Du ska bara ha med huvud ord och inga konjuktioner."
        " [dokumenttyp] ska du bytta ut mot en dokumenttyp som användare letar efter. Du har tillgång till betänkande (bet), Motion (mot), Votering (votering), Skriftlig fråga (fr) och Proposition (prop)"
        " [Från datum] och [till datum] ska du bytta ut mot datum som användaren letar efter."
        " Om filtret inte är relevant för användarens fråga ska det lämnas tomt. Det vill säga utan [exempel]"

        " När du har tagit fram en url vill jag att du svara med: [url:lägg url'n här.]"
        "Till exempel [url:https://exempel.url.se/exempel]")
    elif id == 2:
        return (" Du är en hjälpsam assisten som ska hjälpa en användare att söka igenom Riksdagens databas. Vid detta tillfälle har vi fått ett svar av Riksdagens api "
        " Du kommer få tillgång till svaret och ska sammanställa det på ett snyggt sätt för användaren. Jag vill att all relevant data utifrån användarens fråga ska visas. Du ska inte visa url'ens utan istället ska du erbjuda dig att berätta mer om varje sak. "
        " Här är svaret från api'n som du ska förkorta " + str(apiAnswer)) 
    elif id == 3:
        return ("Du är en hjälpsam assisten som ska söka igenom en databas över Riksdagen, samt bestämma vad nästa steg kommer vara för detta program. Användaren kommer ställa dig en fråga till dig som du ska utgå ifrån."
        " Om användarens fråga kräver ett api call för mer information ska du förja steg 1, men om användarens fråga är en följdfråga på en tidigare fråga ska du följa steg 2"

        " Steg 1: "
        " För att skapa ett api call har du tillgång till denna URL: https://data.riksdagen.se/dokumentlista/?sok=[Sökord]&doktyp=[dokumenttyp]&from=[Från datum]&tom=[till datum]&sort=rel&utformat=json&p=1&a=s#soktraff"
        " [sökord] ska du bytta ut mot huvud ord av det använderan letar efter. Till exemple flyg eller miljön. Du ska bara ha med huvud ord och inga konjuktioner."
        " [dokumenttyp] ska du bytta ut mot en dokumenttyp som användare letar efter. Du har tillgång till betänkande (bet), Motion (mot), Votering (votering), Skriftlig fråga (fr) och Proposition (prop)"
        " [Från datum] och [till datum] ska du bytta ut mot datum som användaren letar efter."
        " Om filtret inte är relevant för användarens fråga ska det lämnas tomt. Det vill säga utan [exempel]"
        " När du har tagit fram en url vill jag att du svara med: [url:lägg url'n här.]"
        " Till exempel [url:https://exempel.url.se/exempel]"
        
        " Steg 2:"
        " returnera bara False"
        
        " För att hjälpa med att bestämma vilket fall du ska utgå ifrån kommer du här få alla frågor användaren har ställt:" + str(fdFragor))
    elif id == 4:
        return(" Du ska med hjälp av föredetta frågor och svar ge ut ett api url. Användaren kommer stäla dig en fråga och du ska hitta dokument användaren syftar på"
               " Här kommer före detta frågor:" + str(fdFragor) +
               " Här kommer före detta svar på frågorna:")     
    
def questAns(previous, question, answer, apiAnswer):
    return previous + f"Användarens nästa Fråga var: ({question}). Och assistentens svar var: ({answer}). Api svar som du nu har tillgång till: ({apiAnswer})"

##################################
#           Chat Func            #
##################################

def createURLsearch(question, questions, num):
    context = chatContextFunc(num,"", questions)

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

    print(answerContent)
    print("######################")
    
    if answerContent == "False":
        return False

    url = extract_text_between(answerContent, "[url:", "]")

    if url != "":
        apiAnswer = requestApi(url)

    return apiAnswer

def normalChatCall(thingToShorten, question2, num):
    context = chatContextFunc(num,thingToShorten,"")
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": question2}
        ],
        temperature=0.07
    )
    answerMessage = completion.choices[0].message
    answerContent = answerMessage.content

    return answerContent

##################################
#            Storage             #
##################################

apiAnswers = []
questions = []
chatAnswers = []

#storage = {"questions": {"Ge mig ett dokument om miljön":{"svar": "ergnergnerogn", "api": "api fetch"}}}

##################################
#         Loop functions         #
##################################

def loopShortenText(apiAnswer ,question):
    shortenedAnswer = normalChatCall(str(apiAnswer), question, 2)

    print(shortenedAnswer)

    chatAnswers.append(shortenedAnswer)

def loopFetchApi():
    question = input("Message to RiksdagsTracker GPT: ")
    questions.append(question)

    answerContent = createURLsearch(question, questions, 3)
    apiAnswers.append(answerContent)

    #Delar svaret i två delar samt sparar.
    #answerLen = len(answerContent["dokumentlista"]["dokument"])
    #for i in range(answerLen):
    #    if len(questions) not in apiAnswers:
    #        apiAnswers[len(questions)] = [[],[]]  

    #    if i < (answerLen / 2):
    #        apiAnswers[len(questions)][0].append(answerContent["dokumentlista"]["dokument"][i])
    #    else:
    #        apiAnswers[len(questions)][1].append(answerContent["dokumentlista"]["dokument"][i])

    return answerContent, question



##################################
#             Chat               #
##################################
val = ["fetch api", "förkorta api svar", "följdfråga"]
valt = "fetch api"

while True:
    if valt == "fetch api":
        answer, question = loopFetchApi()
        if answer == False:
            valt = val[2]
        else:
            valt = val[1]
    elif valt == "förkorta api svar":
        loopShortenText(answer, question)
        valt = val[0]
    elif valt == "följdfråga":
        print("följdfråga")
        valt = val[0]





