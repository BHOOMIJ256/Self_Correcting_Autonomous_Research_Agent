import requests
from langchain_core.tools import tool
import xml.etree.ElementTree as ET

@tool
def arxiv_search_tool(query: str):
    """
    Useful for searching academic papers on ArXiv. 
    Use this when the user asks for 'papers', 'research', 'scientific studies', or 'PDFs'.
    """
    print(f"--- [ArXiv Tool] Searching for: {query} ---")
    
    # ArXiv API Endpoint
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": 3
    }
    
    try:
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            return "Error connecting to ArXiv."
            
        # Parse XML
        root = ET.fromstring(response.content)
        namespace = {'atom': 'http://www.w3.org/2005/Atom'}
        
        results = []
        for entry in root.findall('atom:entry', namespace):
            title = entry.find('atom:title', namespace).text.strip().replace('\n', ' ')
            summary = entry.find('atom:summary', namespace).text.strip().replace('\n', ' ')
            link = entry.find('atom:id', namespace).text.strip()
            published = entry.find('atom:published', namespace).text.strip()[:10]
            
            results.append(f"Title: {title}\nDate: {published}\nLink: {link}\nAbstract: {summary[:500]}...")
            
        return "\n\n".join(results) if results else "No papers found."
        
    except Exception as e:
        return f"ArXiv Search Error: {e}"