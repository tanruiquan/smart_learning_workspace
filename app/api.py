# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import logging

from fastapi import FastAPI
from starlette.responses import RedirectResponse

from app.attempts.router import router as attempt_router
from app.feedback.router import router as feedback_router
from app.tasks.router import router as task_router

logging.basicConfig(level=logging.DEBUG, filename="app/app.log", filemode="w")

app = FastAPI(
    title="Smart learning workspace",
    version="1.0",
    description="The backend repository for the smart learning workspace",
)

app.include_router(task_router)
app.include_router(attempt_router)
app.include_router(feedback_router)


@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse("/docs")
