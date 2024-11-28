import os
import subprocess

PYPAPERBOT_EXECUTABLE = "pypaperbot"  # Ensure PyPaperBot is installed and accessible globally

async def fetch_pypaperbot_results(keyword: str):
    """Fetch results using PyPaperBot."""
    # Output will be stored in a file named after the keyword
    output_file = f"pypaperbot_output_{keyword.replace(' ', '_')}.json"
    
    try:
        # Run PyPaperBot as a subprocess
        subprocess.run(
            [PYPAPERBOT_EXECUTABLE, "--query", keyword, "--output", output_file],
            check=True
        )
        # Load and parse the output file
        if os.path.exists(output_file):
            import json
            with open(output_file, "r") as f:
                data = json.load(f)
            return [{
                "title": paper.get("title"),
                "authors": paper.get("authors"),
                "link": paper.get("pdf_url"),
            } for paper in data]
    except Exception as e:
        print(f"Error running PyPaperBot: {e}")
    return []
