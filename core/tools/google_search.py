# Google Search Tool

from Tools import ToolBase
from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

load_dotenv()

class GoogleSearchTool(ToolBase):
    def use(self, query):
        try:
            search = GoogleSearch({
                "q": query,
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
        except Exception as e:
            return f"An error occurred while performing the search: {str(e)}"

# Example usage
if __name__ == "__main__":
    tool = GoogleSearchTool()
    query = "latest tech in quantum physics"
    result = tool.use(query)
    print(result)
