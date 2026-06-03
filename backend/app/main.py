from fastapi import FastAPI

app = FastAPI(
    title="Enterprise AI Compliance Copilot",
    version="0.1.0"
)

@app.get("/")
def root():
    return {
        "message": "Enterprise AI Compliance Copilot API"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }