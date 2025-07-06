from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/research")
def research(q: str = Query(...)):
    # Simulated live research from DuckDuckGo (or any search API)
    return {"summary": f"Top search insights for '{q}' from the web."}
