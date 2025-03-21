import os

from fastapi import Depends, HTTPException, Request, security
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware

security = HTTPBearer() # noqa

class BearerTokenMiddleware(BaseHTTPMiddleware):
    """
    Middlerware de autenticaçao via API, sei que JWT  é melhor, mas é só para testar.
    Em ambiente de produção, use JWT e Lambda Authoraizer com API Gateway.
    """
    WITHELISTT = [
        "/docs",
        "/openapi.json",
        "/api/healthcheck/"
    ]

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.WITHELISTT:
            return await call_next(request)

        if os.getenv("PYTHON_ENV") == "test":
            return await call_next(request)

        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={
                    "message": "Unauthorized - Bearer token is missing or inválid"
                },
            )

        token = auth_header.split(" ")[1]
        if token != os.getenv("API_KEY"):
            return JSONResponse(
                status_code=403,
                content={"message": "Forbidden - Invalid Bearer token or expired"},
            )

        return await call_next(request)

async def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Verifica se o token está no formato "Bearer <token>"
    if credentials.scheme != "Bearer":
        raise HTTPException(
            status_code=401,
            detail="Formato de token inválido. Use 'Bearer <token>'.",
        )

    token = credentials.credentials
    if token != os.getenv("API_KEY"):
        raise HTTPException(
            status_code=403,
            detail="Token inválido ou expirado.",
        )

    return token
