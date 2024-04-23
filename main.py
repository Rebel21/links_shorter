from fastapi import FastAPI, HTTPException, Depends
import uvicorn
from fastapi.responses import RedirectResponse

from repository import TokenRepository
from routers.token_router import router as token_router
from schemes import SShortUrl

app = FastAPI()
app.include_router(token_router)


@app.get("/{short_code}")
async def get_original_url(short_code: str):
    url = await TokenRepository.get_url(short_code)
    # if url is None:
    #     raise HTTPException(status_code=404, detail=f"Short {short_code} code not found")
    # if not token.is_activ:
    #     raise HTTPException(status_code=403, detail=f"Url {short_code} was disabled")
    # return RedirectResponse(token.original_url)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
