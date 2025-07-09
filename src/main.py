from fastapi import FastAPI
from routes.root import router as root_router
from routes.scrape_recipe import router as scraper_router
from routes.merge_ingredients import router as merger_router
import uvicorn

app = FastAPI()
app.include_router(root_router)
app.include_router(scraper_router)
app.include_router(merger_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
