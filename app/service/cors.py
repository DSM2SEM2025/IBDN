from fastapi.middleware.cors import CORSMiddleware
import os

origins = os.getenv("ALLOWED_ORIGINS", "").split(",")


def add_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
