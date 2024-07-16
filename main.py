from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.route import router

app = FastAPI()

# Define allowed origins
origins = [
    "http://localhost:3000",  # Replace with your frontend origin
]

# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include your router
app.include_router(router)
