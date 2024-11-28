async def download_paper_text(url: str) -> str:
    """Download and return the full text of a paper."""
    if not url:
        return "No URL provided."

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        elif response.status_code == 202:
            return "The paper content is not immediately available (HTTP 202)."
        else:
            return f"Failed to download paper (HTTP {response.status_code})."
    except Exception as e:
        return f"Error downloading paper: {e}"
