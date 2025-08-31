import os, requests

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")

def web_search(query: str, k: int = 3) -> list[dict]:
    # prefer SerpAPI
    results = []
    try:
        if SERPAPI_KEY:
            url = "https://serpapi.com/search.json"
            resp = requests.get(url, params={"q": query, "api_key": SERPAPI_KEY})
            data = resp.json()
            for item in (data.get("organic_results") or [])[:k]:
                results.append({"title": item.get("title"), "snippet": item.get("snippet")})
            return results
        if BRAVE_API_KEY:
            url = "https://api.search.brave.com/res/v1/web/search"
            headers = {"X-Subscription-Token": BRAVE_API_KEY}
            resp = requests.get(url, headers=headers, params={"q": query})
            data = resp.json()
            for item in (data.get("web", {}).get("results") or [])[:k]:
                results.append({"title": item.get("title"), "snippet": item.get("description")})
            return results
    except Exception as e:
        results.append({"title": "search-error", "snippet": str(e)})
    return results
