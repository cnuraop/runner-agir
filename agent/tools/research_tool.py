import os
from serpapi import GoogleSearch
from tools.google_docs_tool import GoogleDocsTool

class ResearchTool:
    def __init__(self):
        self.serpapi_key = os.getenv("SERPAPI_KEY","xxxxx")
        if not self.serpapi_key:
            raise ValueError("SerpAPI key not found. Set the SERPAPI_KEY environment variable.")
        self.docs = GoogleDocsTool()

    def research_from_task(self, task_desc):
        # Basic cleaning of input
        keywords = ["research", "and", "write", "a", "summary", "on", "about", "topic"]
        for word in keywords:
            task_desc = task_desc.replace(word, "")
        query = task_desc.strip()

        params = {
            "engine": "google",
            "q": query,
            "api_key": self.serpapi_key,
            "num": 5
        }

        try:
            search = GoogleSearch(params)
            results = search.get_dict()
        except Exception as e:
            return f"Error while fetching research: {e}"

        if "organic_results" not in results:
            return "No search results returned."

        summary = f"Research Summary for: {query}\n\n"
        for idx, result in enumerate(results["organic_results"][:5], 1):
            title = result.get("title", "No Title")
            link = result.get("link", "")
            snippet = result.get("snippet", "No description available.")
            summary += f"{idx}. {title}\n{snippet}\n{link}\n\n"

        # Save to Google Doc
        doc_url = self.docs.save_research_to_doc(task_desc, summary)
        return f"Research complete. Saved to Google Doc: {doc_url}"
