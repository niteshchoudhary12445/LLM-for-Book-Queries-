import os
from langchain.tools import Tool
from langchain_community.utilities import SerpAPIWrapper, GoogleSearchAPIWrapper, PubMedAPIWrapper, ArxivAPIWrapper

# Load API keys from environment variables
serp_api_key = os.getenv("SERPAPI_API_KEY")
google_api_key = os.getenv("API_KEY")
google_cse_id = os.getenv("CSE_ID")
pubmed_api_key = os.getenv("PUBMED_API_KEY")

class Tools:
    def __init__(self):
        """Initialize the various API Wrappers and tools."""
        self.serp_api_wrapper = SerpAPIWrapper(serpapi_api_key=serp_api_key)
        self.google_search_wrapper = GoogleSearchAPIWrapper(google_api_key=google_api_key, google_cse_id=google_cse_id)
        self.pubmed_wrapper = PubMedAPIWrapper(pubmed_api_key=pubmed_api_key)
        self.arxiv_wrapper = ArxivAPIWrapper()

    def search_real_time_query(self, query: str):
        """Search for real-time results using SerpAPI."""
        try:
            return self.serp_api_wrapper.run(query)
        except Exception as e:
            return {"error": f"Failed to fetch real-time results: {str(e)}"}

    def customize_search_query(self, query: str):
        """Perform a custom search using Google Search API."""
        try:
            return self.google_search_wrapper.run(query)
        except Exception as e:
            return {"error": f"Google Custom Search API failed: {str(e)}"}

    def pubmed_search_query(self, query: str):
        """Search for medical papers on PubMed."""
        try:
            return self.pubmed_wrapper.run(query)
        except Exception as e:
            return {"error": f"PubMed API search failed: {str(e)}"}

    def arxiv_search_query(self, query: str):
        """Search for scientific papers on Arxiv."""
        try:
            return self.arxiv_wrapper.run(query)
        except Exception as e:
            return {"error": f"Arxiv API search failed: {str(e)}"}

    def create_tools(self):
        """Create and return a list of tools for handling various types of searches and document reading."""
        return [
            Tool(
                name="Search Real-Time Query",
                func=self.search_real_time_query,
                description="Use this tool to search for real-time results using SerpAPI."
            ),
            Tool(
                name="Customize Search",
                func=self.customize_search_query,
                description="Use this tool for customizable search if you don't get results using real-time search."
            ),
            Tool(
                name="PubMed Search",
                func=self.pubmed_search_query,
                description="Use this tool to search for medical papers, research articles, and clinical studies on PubMed."
            ),
            Tool(
                name="Arxiv Search",
                func=self.arxiv_search_query,
                description="Use this tool to search for research papers on computer science, physics, mathematics, and other scientific fields on Arxiv."
            )
        ]
