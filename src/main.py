from fastapi import FastAPI
from routes.root import router as root_router
from routes.scrape_recipe import router as scraper_router
from routes.merge_ingredients import router as merger_router

app = FastAPI()
app.include_router(root_router)
app.include_router(scraper_router)
app.include_router(merger_router)
