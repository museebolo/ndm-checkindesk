from __future__ import annotations
import os
from pathlib import Path
import yaml
from fastapi import FastAPI, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.state import State

DATA_PATH = os.getenv("DATA_PATH", "/data/state.json")
PORT = int(os.getenv("PORT", "8080"))
YEAR = os.getenv("YEAR", "2025")

TITLE = f"Nuit des Musées {YEAR}"
OFFSET_X = os.getenv("OFFSET_X", "50%")
OFFSET_Y = os.getenv("OFFSET_Y", "50%")


def reload_config_values():
    global TITLE, OFFSET_X, OFFSET_Y
    cfg_file = Path("/config/config.yaml")
    cfg = {}
    if cfg_file.exists():
        try:
            with cfg_file.open("r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f) or {}
        except Exception as e:
            print(f"[warn] erreur lecture config.yaml: {e}")
    title = cfg.get("title") or f"Nuit des Musées {YEAR}"
    ox = cfg.get("offset_x") or os.getenv("OFFSET_X", "50%")
    oy = cfg.get("offset_y") or os.getenv("OFFSET_Y", "50%")
    TITLE, OFFSET_X, OFFSET_Y = str(title), str(ox), str(oy)
    return {"title": TITLE, "offset_x": OFFSET_X, "offset_y": OFFSET_Y}


# initial load
reload_config_values()

app = FastAPI(title="Compteur Entrées & Billets")
templates = Jinja2Templates(directory="app/templates")
state = State(DATA_PATH)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/healthz")
def healthz():
    return PlainTextResponse("ok")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    snap = state.snapshot()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "entries": snap["entries"],
            "tickets": snap["tickets"],
            "total": snap["total"],
            "title": TITLE,
            "offset_x": OFFSET_X,
            "offset_y": OFFSET_Y,
        },
    )


@app.post("/update")
async def update(key: str = Form(...), delta: str = Form(...)):
    if delta not in ("+1", "-1"):
        raise HTTPException(status_code=400, detail="bad delta")
    d = 1 if delta == "+1" else -1
    try:
        snap = state.update(key, d)
        return JSONResponse(snap)
    except ValueError:
        raise HTTPException(status_code=400, detail="bad key")


@app.post("/reset")
async def reset():
    snap = state.reset()
    return JSONResponse(snap)


@app.post("/reload-config")
async def reload_config_endpoint():
    vals = reload_config_values()
    return JSONResponse({"ok": True, **vals}, status_code=status.HTTP_200_OK)
