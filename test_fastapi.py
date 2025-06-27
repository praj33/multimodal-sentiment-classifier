#!/usr/bin/env python3
"""
Simple FastAPI test to check if uvicorn works at all
"""

from fastapi import FastAPI
import time

app = FastAPI(title="Simple Test API")

@app.get("/")
def root():
    return {"message": "Hello World", "timestamp": time.time()}

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting simple test server on port 8002...")
    uvicorn.run(app, host="0.0.0.0", port=8002)
