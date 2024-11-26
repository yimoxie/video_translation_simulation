# tests/integration_test.py

import asyncio
import uvicorn
from multiprocessing import Process
from client import ClientLibrary
from server.server import app


def start_server():
    """Starts the FastAPI server."""
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")


async def main():
    """Main function to run the client library."""
    client = ClientLibrary("http://127.0.0.1:8000")
    try:
        result = await client.wait_for_result(timeout=30)
        print(f"Final result: {result}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await client.close()


if __name__ == "__main__":
    server_process = Process(target=start_server)
    server_process.start()

    try:
        asyncio.run(main())
    finally:
        server_process.terminate()