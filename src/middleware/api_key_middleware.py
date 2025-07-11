import os
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class APIKeyMiddleware(BaseHTTPMiddleware):
    """
    Middleware to check the api key
    """

    PROTECTED_ROUTES = ["/scrape-recipe", "/merge-ingredients"]

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        if not any(request.url.path.startswith(path) for path in self.PROTECTED_ROUTES):
            return await call_next(request)

        api_key = request.headers.get("X-API-Key")
        if api_key != os.getenv("ALLOWED_API_KEY"):  # Replace with your actual API key
            raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")

        response = await call_next(request)
        return response
