from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import plot
from app.config import settings


app = FastAPI(
    title="Land Mapping API", 
    version="1.0.0",
    debug=settings.DEBUG,
    )

# CORS Configuration, To add more origings, we can direcctly add them in config.py file in ALLOWED_ORIGINS variable
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"]
)


# The main router code can be found in app/routers/plot.py and the main "GeneratePlot" can be found in app/services/plot_mechanism.py
# registering the routers.

app.include_router(plot.router)

@app.get("/") # Home entry
def index():
    helth_resp = {
        "title": app.title,
        "version": app.version,
        "routes": "<local URL> /landmap/generate",
        "status": "healthy",
    }
    return helth_resp