from fastapi import FastAPI

app = FastAPI(
    title="Farming Chitti",
    description="AI Agricultural Government Schemes Assistant",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "application": "Farming Chitti",
        "message": "Welcome to Farming Chitti!",
        "status": "Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }