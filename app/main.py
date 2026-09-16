from __future__ import annotations

import os
from pathlib import Path

import yaml
from fastapi import FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.state import State

DATA_PATH = os.getenv("DATA_PATH", "/data/state.json")
PORT = int(os.getenv("PORT", "8080"))
YEAR = os.getenv("YEAR", "2025")

TITLE = f"Nuit des Musées {YEAR}"
OFFSET_X = os.getenv("OFFSET_X", "50%")
OFFSET_Y = os.getenv("OFFSET_Y", "50%")
TICKET_SALES_ENABLED = False


def reload_config_values() -> dict[str, str | bool]:
    global TITLE, OFFSET_X, OFFSET_Y, TICKET_SALES_ENABLED

    cfg_file = Path("/config/config.yaml")
    cfg = {}

    if cfg_file.exists():
        try:
            with cfg_file.open("r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f) or {}
        except (OSError, yaml.YAMLError) as e:
            print(f"[warn] erreur lecture config.yaml: {e}")

    title = cfg.get("title") or f"Nuit des Musées {YEAR}"
    ox = cfg.get("offset_x") or os.getenv("OFFSET_X", "50%")
    oy = cfg.get("offset_y") or os.getenv("OFFSET_Y", "50%")

    counters_cfg = cfg.get("counters", {})
    TICKET_SALES_ENABLED = bool(counters_cfg.get("ticket_sales_enabled", False))

    TITLE = str(title)
    OFFSET_X = str(ox)
    OFFSET_Y = str(oy)

    return {
        "title": TITLE,
        "offset_x": OFFSET_X,
        "offset_y": OFFSET_Y,
        "ticket_sales_enabled": TICKET_SALES_ENABLED,
    }


# Initial configuration load.
reload_config_values()

app = FastAPI(title="Compteur des entrées")
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
        request=request,
        name="index.html",
        context={
            "request": request,
            "children_entries": snap["children_entries"],
            "adult_entries": snap["adult_entries"],
            "adult_tickets_sold": snap["adult_tickets_sold"],
            "total_entries": snap["total_entries"],
            "title": TITLE,
            "offset_x": OFFSET_X,
            "offset_y": OFFSET_Y,
            "ticket_sales_enabled": TICKET_SALES_ENABLED,
        },
    )


@app.post("/update")
async def update(
    key: str = Form(...),
    delta: str = Form(...),
):
    if delta not in ("+1", "-1"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="bad delta")

    d = 1 if delta == "+1" else -1

    try:
        snap = state.update(key, d)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="bad key"
        ) from e

    return JSONResponse(snap)


@app.post("/sell-adult-ticket")
async def sell_adult_ticket(
    delta: str = Form(...),
):
    if not TICKET_SALES_ENABLED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="ticket sales disabled"
        )

    if delta not in ("+1", "-1"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="bad delta")

    d = 1 if delta == "+1" else -1

    snap = state.sell_adult_ticket(d)

    return JSONResponse(snap)


@app.post("/reset")
async def reset():
    snap = state.reset()
    return JSONResponse(snap)


@app.post("/reload-config")
async def reload_config_endpoint():
    vals = reload_config_values()

    return JSONResponse(
        {
            "ok": True,
            **vals,
        },
        status_code=status.HTTP_200_OK,
    )
