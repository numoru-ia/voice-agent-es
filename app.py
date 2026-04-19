"""FastAPI websocket that drives a Pipecat pipeline per call."""
from __future__ import annotations

import os
from fastapi import FastAPI, WebSocket

from agent import run_agent

app = FastAPI()


@app.websocket("/ws/{tenant_id}")
async def voice_ws(websocket: WebSocket, tenant_id: str):
    await websocket.accept()
    await run_agent(websocket, tenant_id)


@app.get("/healthz")
async def healthz():
    return {"ok": True}
