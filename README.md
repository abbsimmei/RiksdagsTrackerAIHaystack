# **RiksdagsTracker AI**

## **Table of Contents**

1. [Overview](#overview)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Examples](#examples)
5. [API Endpoints](#api-endpoints)
6. [Architecture](#architecture)
7. [Previous Attempts](#previous-attempts)
8. [Further Development and vulnerabilities](#further-development-and-vulnerabilities)

---

## **1. Overview**

This is a project which aim is to create an AI Retrieval-Augmented Generation (RAG) model for the UF company RiksdagsTracker UF. The AI-powered chatbot is able to, from user questions, find relevant documents in the [API](https://www.riksdagen.se/sv/dokument-och-lagar/riksdagens-oppna-data/) provided by the Riksdag, shorten the answers and is able to answer further questions about the documents it has provided.

Throughout the project I have tried several different frameworks to build the AI, but in the end I used the OpenAI api.

## **2. Installation**

1. **Prerequisites**:

   - Python version: The program was writen in python version 3.13

2. **Installation steps**:

   ```
   git clone https://github.com/abbsimmei/RiksdagsTrackerAIHaystack.git
   cd FastAPI
   pip install openai
   pip install "fastapi[standard]"
   ```

---

## **3. Usage**

To run the python AI part of the project:

```
cd FastAPI
fastapi dev fastApi_GPT.py
```

To run the website to try out the chat please read the README.md file in /Riksdags-Tracker. (Note: it's in Swedish since it's copied from the RiksdagsTracker repository.)

Alternativly, if you don't want to set up the website you can simply run the GPT_Models/chatGPT_V3.py which is the same as the fastApi_GPT.py script but without the api, and therefor running in the terminal.

## **4. Examples**

You can now ask questions in the chat. Try for example: Ge mig dokument om miljön.
And then: Kan du förklara mer om dokument: "a dokument it provided."

## **5. API Endpoints**

The only relevant endpoint used is:

- /fraga/{userQuestion}

Example:
Request: GET /fraga/Vad%20%C3%A4r%20klimatlagen
Response: { "answer": "Klimatlagen är en lag..." }

This endpoint takes in {user question} and returns the answer.

---

## **6. Architecture**

How does the AI work.

Using the API endpoint a question is given to the python script. This question is then checked using one [openAI request](https://platform.openai.com/docs/quickstart) if it's a follow-up question or not. If it's is the AI returns False, if it isn't the AI returns a url for the riksdagens open API with the relevant search words from the users question.

If it returns a url that url is fetched with it's answer then sent to openAI once again with instructuctions to shorten the text. This shortened answer is then outputed to the user.

If it returns False, a second openAI request will be made where previous questions and documents are provided, this ai will then output the url of the relevant document which the user is asking a follow-up question about. This url is then passed through the same process of shortening as if the first request found a url.

In order to allow the program to find the relevant follow-up documents all answers and questions are stored and provided to the AI once necesarry.

---

## **7. Previous Attempts**

As you can see there are several other python files with everything from working to non-working tests.

I started with trying to use [huggingface](https://huggingface.co/) and [pipelines](https://huggingface.co/docs/transformers/main_classes/pipelines) to run an AI locally as you can see in the virtualFolder/virtualEnvironment.py

Due to the limitations of the computer and struggles with the pytorch library I instead switched to using [LM studio](https://lmstudio.ai/). A program where you also can download LLM models locally on the computer but which automaticly sets up api endpoints simplifying the work.

However due to the models still lacking the accurancy and runtime I seek, I finally decided to switch to the openAI api with a key provided by the school, as this allowed me to use gpt-4o-mini, a far stronger language model compared to the gpt-2 I had run using huggingface and Llama 3.2 1B using lm-studio.

Finally the last version before was the GPT_Models/chatGPT_V3.py which works just like the main version except without the API. So you can try it in the terminal if you don't want to set up the website by simply running the script.

## **8. Further Development and vulnerabilities**

At the moment the process is not significantly optimised, for example it can take up to three requests to openAI before an answer can be given something which is both bad for runtime and for the climate. To improve this instead of one reqest determining if the question is a follow-up question and a second request determining which document it is about, these two could be shortened to a single request.

The answers also don't include any sources, and since this AI is answering regarding important documents it would be necesarry to include a way for it to give it's sources to make the process trustworthy. Especially since I have found questions where it bases it's answer on no documents at all.

Anothere vulnerability is that there is nothing checking if it's riksdagstracker.se that is making the requests. This means other websites would be able to use our openAI api keys without our approval. (Though this is not an issue right now since everything is local host)
