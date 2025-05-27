from fastapi import FastAPI

from app.core.docs import setup_docs

app = FastAPI(docs_url=None, redoc_url=None)

setup_docs(app)


# Example route
@app.get("/")
async def read_root():
    return {"message": "Welcome to the API"}
