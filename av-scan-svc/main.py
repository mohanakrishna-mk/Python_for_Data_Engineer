from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, you are connected to port 7000!"}

if __name__ == "__main__":
    import uvicorn
    # This keeps the server listening on port 7000
    uvicorn.run(app, host="0.0.0.0", port=7000)
