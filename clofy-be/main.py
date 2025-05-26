from fastapi import FastAPI

app = FastAPI(
    swagger_ui_parameters={
        "syntaxHighlight": {"theme": "obsidian"},
        "defaultModelsExpandDepth": -1,
        "docExpansion": "none",
    }
)


# Example route
@app.get("/")
async def read_root():
    return {"message": "Welcome to the API"}
