import hmac
import httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTask

ALLOWED = {"api/chat", "api/generate", "v1/chat/completions"}
MAX_BODY = 2_000_000 # 2MB limit

def build_app(api_key: str, upstream: str) -> FastAPI:
    if not api_key:
        raise RuntimeError("API key required to start proxy")
    
    key_b = api_key.encode()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.client = httpx.AsyncClient(
            base_url=upstream, timeout=httpx.Timeout(10, read=600))
        yield
        await app.state.client.aclose()

    # Disable docs to prevent unauthenticated probing
    app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)

    @app.post("/{path:path}")
    async def proxy(path: str, request: Request):
        # 1. Auth Check First
        scheme, _, token = request.headers.get("authorization", "").partition(" ")
        if scheme.lower() != "bearer" or not hmac.compare_digest(token.encode(), key_b):
            raise HTTPException(401, detail="Unauthorized")
        
        # 2. Path Allow-List
        if path not in ALLOWED:
            raise HTTPException(403, detail="Endpoint not allowed")
            
        # 3. Body Size Limit
        if int(request.headers.get("content-length", 0)) > MAX_BODY:
            raise HTTPException(413, detail="Payload too large")
            
        body = await request.body()
        
        # 4. Forward Request (Strip sensitive headers)
        req = app.state.client.build_request(
            "POST", f"/{path}", content=body,
            headers={"content-type": request.headers.get("content-type", "application/json")})
        
        r = await app.state.client.send(req, stream=True)
        return StreamingResponse(
            r.aiter_raw(), status_code=r.status_code,
            media_type=r.headers.get("content-type"),
            background=BackgroundTask(r.aclose))
            
    return app