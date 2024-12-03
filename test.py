import requests

url = "//data.riksdagen.se/dokument/H5023024.html"

def requestHtmlApi(url):
    try:   
        print("Fetching html url")
        response = requests.get(url)
        #response.raise_for_status()  # Ensure we get a valid response
        return response
    except Exception as e:
        pass
        #print(f"An error occurred: {e}")   

repsonse = requestHtmlApi(url)
print(repsonse.content)