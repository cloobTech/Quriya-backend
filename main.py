from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from src.core.pydantic_config import config
from src.api.v1.routes import user, organization, auth, election_project, result, locations
from src.events.bootstrap import bootstrap_events_initializer
from src.storage import db
from src.api.v1.register_exceptions import register_exception_handlers
from src.api.v1.dependencies import validate_organization_route


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize event bus and subscriptions

    bootstrap_events_initializer()
    if config.DEV_ENV == 'development':
        await db.create_tables()
    yield
    # Cleanup actions can be added here if necessary
    await db.cleanup()


app = FastAPI(
    title="Quriya App Backend",
    description="Backend API for Quriya App - Election Monitoring Solution",
    version="1.0.0",
    docs_url="/",
    redoc_url=None,
    lifespan=lifespan,
)


register_exception_handlers(app)


origins = [
    f"https://example.com" if config.DEV_ENV == 'production' else "*",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(auth.router,
                   prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(
    user.router, prefix="/api/v1/organizations/{organization_id}/users", tags=["Users"])
app.include_router(organization.router,
                   prefix="/api/v1/organizations", tags=["Organizations"])
app.include_router(election_project.router,
                   prefix="/api/v1/organizations/{organization_id}/projects", tags=["Election Monitoring Projects"], dependencies=[Depends(validate_organization_route)])
app.include_router(result.router,
                   prefix="/api/v1/organizations/{organization_id}/projects/{project_id}/results", tags=["Election Results"])

app.include_router(locations.router,
                   prefix="/api/v1/locations", tags=["Static Locations"])


@app.get("/api/v1")
async def read_root():
    """Check server status"""
    return {"server_status": "Server is running fine..."}
