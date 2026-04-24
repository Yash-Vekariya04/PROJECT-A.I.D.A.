from duckduckgo_search import DDGS

class AidaTools:
    def __init__(self):
        self.registry = {
            "web_search": self.search_web
        }

    def execute(self, tool_name: str, parameters: dict):
        """The master execution hub."""
        if tool_name in self.registry:
            print(f"\n[SYSTEM] Executing Physical Tool: {tool_name}")
            return self.registry[tool_name](**parameters)
        return f"Error: Tool '{tool_name}' not found."
    
    def search_web(self, query: str):
        """Fetches live search results from DuckDuckGo."""
        print(f"[SYSTEM] Scraping the web for: '{query}'")

        try:
            # Fetching top 3 results
            results = DDGS().text(query, max_results=3)

            # Format the JSON into a clean text string for F.R.I.D.A.Y.'s brain
            knowledge_block = f"Live Web Results for '{query}':\n\n"
            for index, result in enumerate(results):
                knowledge_block += f"- {result['title']}: {result['body']}\n"

            return knowledge_block
        
        except Exception as e:
            return f"System Error: Web search failed due to {e}"