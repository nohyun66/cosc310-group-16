from fastapi import FastAPI

app = FastAPI(
    title="COSC 310 Group 16",
    version="0.1.0"
)


@app.get("/health")
def health():
    return {"status": "ok"}