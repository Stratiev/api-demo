import subprocess
import time

from fastapi import FastAPI

from app.ls_helpers import ListRequest, compile_ls_command, handle_ls_errors
from app.probability_helpers import SoccerTeamsRequest, handle_invalid_team_name
from logger import get_logger
from utils import get_latest_soccer_data

LOGGER = get_logger(__name__)

app = FastAPI()


@app.post("/ls")
async def ls(request: ListRequest):
    LOGGER.info("Processing ls request.")
    command = compile_ls_command(request)
    res = subprocess.run(command, capture_output=True)
    handle_ls_errors(res.stderr)
    return {'text': res.stdout}

@app.post("/blocking_ls")
async def blocking_ls(request: ListRequest):
    LOGGER.info("Processing blocking_ls request.")
    command = compile_ls_command(request)
    res = subprocess.run(command, capture_output=True)
    handle_ls_errors(res.stderr)
    time.sleep(5)
    return {'text': res.stdout}

@app.post("/probability")
async def probability(request: SoccerTeamsRequest):
    LOGGER.info("Processing probability request.")
    command = ['./external_executable'] + [request.team_1] + [request.team_2]
    res = subprocess.run(command, capture_output=True)
    handle_invalid_team_name(res.stderr)
    return {'text': res.stdout}

@app.post("/blocking_probability")
async def blocking_probability(request: SoccerTeamsRequest):
    LOGGER.info("Processing probability request.")
    command = ['./external_executable'] + [request.team_1] + [request.team_2]
    res = subprocess.run(command, capture_output=True)
    handle_invalid_team_name(res.stderr)
    time.sleep(5)
    return {'text': res.stdout}

@app.get("/soccer_teams")
async def soccer_teams():
    LOGGER.info("Processing soccer teams get request.")
    df = get_latest_soccer_data()
    clubs = df['Club'].unique().tolist()
    return {'clubs': clubs}

@app.on_event("shutdown")
def shutdown_event():
    LOGGER.info("Application shutdown")



