import requests

PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
DETAILS_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"  # ✅ Use efetch for XML

def fetch_pubmed_data(query: str, debug: bool = False):
    """Fetch PubMed articles based on a query and return raw XML data."""
    
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",  # ✅ Search still uses JSON
        "retmax": 10  # ✅ Limit to 10 results
    }
    
    response = requests.get(PUBMED_API_URL, params=params)
    
    if debug:
        print(f"🔍 Debug: Fetching data for query: {query}")
        print(f"🌍 API URL: {response.url}")

    if response.status_code != 200:
        raise Exception("❌ Failed to fetch data from PubMed API")

    # ✅ Extract article IDs from JSON response
    article_ids = response.json().get("esearchresult", {}).get("idlist", [])

    articles = []
    for article_id in article_ids:
        article_details = fetch_article_details(article_id, debug)
        if article_details:
            articles.append(article_details)

    return articles

def fetch_article_details(article_id: str, debug: bool = False):
    """Fetches full details of a PubMed article using its ID in XML format (for affiliations & emails)."""
    params = {
        "db": "pubmed",
        "id": article_id,
        "retmode": "xml"  # ✅ Request XML format instead of JSON
    }
    
    response = requests.get(DETAILS_API_URL, params=params)
    
    if response.status_code != 200:
        print(f"❌ Failed to fetch details for article {article_id}")
        return None
    
    if debug:
        print(f"✅ Successfully fetched article {article_id}")

    return response.text  # ✅ Return XML instead of JSON
