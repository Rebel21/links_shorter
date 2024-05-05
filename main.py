from fastapi import FastAPI, HTTPException, Depends
import uvicorn
from fastapi.responses import RedirectResponse

from repository import UrlRepository
from routers.url_router import router as url_router
from routers.short_url_router import router as short_url_router

app = FastAPI()
app.include_router(url_router)
app.include_router(short_url_router)


@app.get("/{short_url}")
async def get_original_url(short_url: str):
    _short_url = await UrlRepository.get_url(short_url)
    if short_url is None:
        raise HTTPException(status_code=404, detail=f"Short {short_url} code not found")
    if not _short_url.is_activ:
        raise HTTPException(status_code=403, detail=f"Url {short_url} was disabled")
    return RedirectResponse(_short_url.url.original_url)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
