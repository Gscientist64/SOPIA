import requests
from config import SERP_API_KEY

def search_web(query):
    # Using SerpApi for web search
    url = f"https://serpapi.com/search?q={query}&api_key={SERP_API_KEY}"
    response = requests.get(url)
    results = response.json()
    
    if 'organic_results' in results:
        # Grab the first result title and snippet
        top_result = results['organic_results'][0]
        return f"Web result: {top_result['title']} - {top_result['snippet']}"
    else:
        return "Sorry, I couldn't find relevant information on the web." 