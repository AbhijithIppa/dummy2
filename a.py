from fastapi import FastAPI,APIRouter
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from api.routers.createRepo import createRepoRouter
from api.routers.processRepo import processRouter
from api.routers.repoStatus import repoStatus_router
from api.routers.getChunks import get_chunk_router
from api.routers.health import health_check_router
load_dotenv()

app = FastAPI(
    title="AI Services API",
    description="API for AI Services",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health_check_router, tags=["health"])
app.include_router(createRepoRouter, prefix="/repo", tags=["repo"])
app.include_router(processRouter, prefix="/repo", tags=["repo"])
app.include_router(repoStatus_router, prefix="/repo", tags=["repo"])
app.include_router(get_chunk_router, prefix="/repo", tags=["repo"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
