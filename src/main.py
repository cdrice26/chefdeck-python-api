from fastapi import FastAPI
from routes.root import router as root_router
from routes.scrape_recipe import router as scraper_router
from routes.merge_ingredients import router as merger_router
from middleware.api_key_middleware import APIKeyMiddleware
from dotenv import load_dotenv
import uvicorn

load_dotenv()

app = FastAPI()
app.include_router(root_router)
app.include_router(scraper_router)
app.include_router(merger_router)

app.add_middleware(APIKeyMiddleware)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
