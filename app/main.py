from __init__ import app
import uvicorn
from router.api import api_router

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8888, reload=True)