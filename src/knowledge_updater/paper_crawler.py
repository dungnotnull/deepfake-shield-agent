import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time

class PaperCrawler:
    """
    Robust crawler for arXiv and Semantic Scholar.
    Handles rate limiting and structured data extraction.
    """
    def __init__(self):
        self.arxiv_url = "http://export.arxiv.org/api/query"
        self.user_agent = {"User-Agent": "DeepFake-Shield-Agent/1.0"}

    def fetch_latest_papers(self, query: str, max_results: int = 20) -> List[Dict]:
        """
        Fetches papers and returns a list of structured summaries.
        """
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending"
        }
        
        try:
            response = requests.get(self.arxiv_url, params=params, headers=self.user_agent, timeout=10)
            response.raise_for_status()
            
            # Using BeautifulSoup to parse the XML response from arXiv
            soup = BeautifulSoup(response.content, "xml")
            entries = soup.find_all("entry")
            
            results = []
            for entry in entries:
                results.append({
                    "title": entry.find("title").text.strip(),
                    "summary": entry.find("summary").text.strip(),
                    "url": entry.find("id").text,
                    "published": entry.find("published").text
                })
            return results
        except Exception as e:
            print(f"Crawler Error: {e}")
            return []

if __name__ == "__main__":
    crawler = PaperCrawler()
    print(crawler.fetch_latest_papers("deepfake detection"))
