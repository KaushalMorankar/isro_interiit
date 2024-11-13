from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import matrix, visualization, plot  # Import the plot router correctly

app = FastAPI(title="ISRO PROJECT", version="1.1.0")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    plot.router, prefix="/api/v1/plot", tags=["plot"]
)  # Include the plot router with the correct prefix


@app.get("/")
async def root():
    return {"message": "Welcome to ISRO PROJECT"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
