# server/server.py

import random
import time
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

# Configurable delay in seconds.
CONFIGURABLE_DELAY = 10  # Adjust this value as needed.
START_TIME = time.time()


@app.get("/status")
def get_status():
    """Endpoint to get the current status of the video translation.

    Returns:
        JSONResponse: A JSON response with the result status.
    """
    elapsed_time = time.time() - START_TIME
    if elapsed_time < CONFIGURABLE_DELAY:
        return JSONResponse(content={"result": "pending"})
    else:
        # Simulate random completion or error after the delay.
        result = random.choice(["completed", "error"])
        return JSONResponse(content={"result": result})