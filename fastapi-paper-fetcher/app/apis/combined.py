import asyncio
from app.apis import arxiv, semantic_scholar, core_api, unpaywall, pypaperbot
from app.utils import download_paper_text

async def search_all_apis(keyword: str):
    """Search all APIs concurrently and produce a final JSON output."""
    api_names = ["arXiv", "Semantic Scholar", "CORE", "Unpaywall", "PyPaperBot"]
    api_functions = [
        arxiv.fetch_arxiv_results,
        semantic_scholar.fetch_semantic_scholar_results,
        core_api.fetch_core_results,
        unpaywall.fetch_unpaywall_results,
        pypaperbot.fetch_pypaperbot_results,
    ]

    # Gather results from all APIs
    results = await asyncio.gather(
        *(api(keyword) for api in api_functions),
        return_exceptions=True,  # Allow exceptions to be returned
    )

    final_output = []

    for idx, result in enumerate(results):
        api_name = api_names[idx]

        if isinstance(result, Exception):
            print(f"Error in {api_name} API: {result}")
            # Append an empty placeholder for failed API
            final_output.append({
                "API": api_name,
                "Title": "Error fetching results",
                "Authors": [],
                "Text": "",
            })
        else:
            print(f"Successfully fetched results from {api_name}")
            for paper in result:
                text = await download_paper_text(paper.get("link"))
                final_output.append({
                    "API": api_name,
                    "Title": paper.get("title", "Unknown Title"),
                    "Authors": paper.get("authors", []),
                    "Text": text,
                })

    print("Final output prepared:", final_output)
    return final_output
