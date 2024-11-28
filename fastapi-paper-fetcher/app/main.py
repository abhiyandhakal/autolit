from fastapi import FastAPI, HTTPException, BackgroundTasks
from app.apis import combined
from app.models import SearchRequest, SearchResults
import os
import json

app = FastAPI()

# Create an output directory if it doesn't exist
OUTPUT_DIR = "app/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"message": "Welcome to the Paper Fetcher API"}

@app.post("/search")
async def search_papers(request: SearchRequest):
    """Search papers and save the results to a JSON file."""
    try:
        results = await combined.search_all_apis(request.keyword)
        
        # Create the output directory if it doesn't exist
        os.makedirs("output", exist_ok=True)
        output_path = os.path.join("output", f"{request.keyword.replace(' ', '_')}_results.json")

        # Write results to JSON
        with open(output_path, "w") as f:
            json.dump(results, f, indent=4)

        return {
            "message": "Results saved successfully",
            "file": output_path,
            "data": results  # Return results in the response
        }
    except Exception as e:
        return {"error": f"An error occurred: {e}"}


@app.post("/download")
def download_papers(selected_apis: list[str], background_tasks: BackgroundTasks):
    """Download papers from selected APIs."""
    background_tasks.add_task(combined.download_papers, selected_apis, OUTPUT_DIR)
    return {"message": "Download started in the background."}
