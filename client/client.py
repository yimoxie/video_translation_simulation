# client_library/client_library.py

import asyncio
import logging
import aiohttp
from typing import Optional


class ClientLibrary:
    """A client library to interact with the video translation server."""

    def __init__(self, server_url: str):
        """Initializes the ClientLibrary instance.

        Args:
            server_url: The base URL of the server.
        """
        self.server_url = server_url
        self.session = aiohttp.ClientSession()
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Sets up the logger for the client library.

        Returns:
            Logger: Configured logger instance.
        """
        logger = logging.getLogger("ClientLibrary")
        handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger

    async def wait_for_result(self, timeout: Optional[int] = None) -> str:
        """Waits for the video translation to complete.

        Uses adaptive polling with exponential backoff.

        Args:
            timeout: Optional; Maximum time in seconds to wait for the result.

        Returns:
            str: The final result status ("completed" or raises an exception).

        Raises:
            TimeoutError: If the operation times out.
            Exception: If an error occurs during processing.
        """
        start_time = asyncio.get_event_loop().time()
        delay = 1  # Initial delay in seconds.
        max_delay = 10  # Maximum delay between retries.

        while True:
            try:
                async with self.session.get(f"{self.server_url}/status") as resp:
                    data = await resp.json()
                    result = data.get("result")

                    self.logger.debug("Received status: %s", result)

                    if result == "completed":
                        self.logger.info("Task completed successfully.")
                        return "completed"
                    elif result == "error":
                        self.logger.error("Task failed with an error.")
                        raise Exception("An error occurred during processing.")
                    else:
                        self.logger.debug("Task pending. Retrying in %s seconds...", delay)
            except Exception as e:
                self.logger.error("Error fetching status: %s", e)

            if timeout and (asyncio.get_event_loop().time() - start_time) > timeout:
                self.logger.error("Timeout reached while waiting for the result.")
                raise TimeoutError("Timeout while waiting for the result.")

            await asyncio.sleep(delay)
            delay = min(max_delay, delay * 2)  # Exponential backoff.

    async def close(self):
        """Closes the HTTP session."""
        await self.session.close()