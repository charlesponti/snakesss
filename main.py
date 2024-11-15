import os
from dotenv import load_dotenv

load_dotenv()

from src.server import app  # noqa: E402

PORT: int = int(os.getenv("PORT") or 5555)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PORT)
