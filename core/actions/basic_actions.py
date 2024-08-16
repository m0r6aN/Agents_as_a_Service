import httpx
import re
from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

load_dotenv()

def google_search(q):
    search = GoogleSearch({
        "q": q,
        "api_key": os.getenv("SERPAPI_API_KEY")
    })
    results = search.get_dict()
    
    # Extract and format the search results
    formatted_results = []
    if "organic_results" in results:
        for result in results["organic_results"][:3]:  # Limit to top 3 results
            title = result.get("title", "No title")
            snippet = result.get("snippet", "No snippet available")
            formatted_results.append(f"{title}\n{snippet}\n")
    
    return "\n".join(formatted_results) if formatted_results else "No results found."

def wikipedia(q):
    response = httpx.get("https://en.wikipedia.org/w/api.php", params={
        "action": "query",
        "list": "search",
        "srsearch": q,
        "format": "json"
    })
    return response.json()["query"]["search"][0]["snippet"]

def calculate(what):
    return eval(what)

# Define known_actions dictionary
known_actions = {
    "wikipedia": wikipedia,
    "calculate": calculate,
    "google_search": google_search
}

action_re = re.compile('^Action: (\w+): (.*)$')