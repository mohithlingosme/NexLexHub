from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import logging
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(title="NexLexHub Admin API")

# Allow your Next.js frontend to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Update with your Next.js domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_scrapers_task():
    """
    This function runs in the background. 
    It executes your existing scraper scripts which will gather news 
    and push them to the Kafka 'raw_articles' topic.
    """
    logging.info("Background Task Started: Triggering Scrapers...")
    try:
        # Example 1: Trigger Supreme Court Scraper
        # Update the path to match where your SC.py is located
        sc_process = subprocess.run(
            ["python", "Pharse_1/Scraper/Live_Law/SC.py"], 
            capture_output=True, 
            text=True
        )
        if sc_process.returncode == 0:
            logging.info("SC Scraper finished successfully.")
        else:
            logging.error(f"SC Scraper failed: {sc_process.stderr}")

        # Example 2: Trigger High Court Scraper
        hc_process = subprocess.run(
            ["python", "Pharse_1/Scraper/Live_Law/High Court/Karnataka_HC.py"], 
            capture_output=True, 
            text=True
        )
        if hc_process.returncode == 0:
            logging.info("HC Scraper finished successfully.")
        else:
            logging.error(f"HC Scraper failed: {hc_process.stderr}")

        logging.info("All scraping tasks completed. Data should now be in the Kafka queue.")

    except Exception as e:
        logging.error(f"Critical error running scrapers: {str(e)}")

@app.post("/api/admin/trigger-update")
async def trigger_news_update(background_tasks: BackgroundTasks):
    """
    Endpoint for the Next.js Admin Panel to trigger a data refresh.
    """
    # 1. Add the heavy scraping task to run in the background
    background_tasks.add_task(run_scrapers_task)
    
    # 2. Return immediately to the frontend so the Admin UI doesn't hang
    return {
        "status": "success",
        "message": "Data update has been triggered. The ML pipeline is processing new articles in the background.",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    # Run the server on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)