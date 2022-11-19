import time
import os
import re
import subprocess
from logger import get_logger
from pydantic import BaseModel, Extra
from fastapi import FastAPI, HTTPException
from typing import List, Optional
from utils import get_latest_soccer_data

LOGGER = get_logger(__name__)

app = FastAPI()

class ListRequest(BaseModel):
    folders: Optional[List[str]]=None
    parameters: Optional[List[str]]=None

    # This forbids extra parameters
    class Config:
        extra = Extra.forbid


class SoccerTeamsRequest(BaseModel):
    team_1: str
    team_2: str

    # This forbids extra parameters
    class Config:
        extra = Extra.forbid

ls_defaults = {'folders': ["."],
               'parameters': [""]}
default_ls_request = ListRequest(**ls_defaults)
probability_defaults = {'team_1': 'Djurgarden',
                        'team_2': 'Hammarby'}
default_probability_request = SoccerTeamsRequest(**probability_defaults)



@app.post("/ls")
async def ls(request: ListRequest=default_ls_request):
    LOGGER.info("Processing ls request.")
    command = compile_ls_command(request)
    res = subprocess.run(command, capture_output=True)
    handle_ls_errors(res.stderr)
    return res.stdout


@app.post("/blocking_ls")
async def blocking_ls(request: ListRequest=default_ls_request):
    LOGGER.info("Processing blocking_ls request.")
    command = compile_ls_command(request)
    res = subprocess.run(command, capture_output=True)
    handle_ls_errors(res.stderr)
    time.sleep(5)
    return res.stdout


@app.post("/probability")
async def probability(request: SoccerTeamsRequest=default_probability_request):
    LOGGER.info("Processing probability request.")
    command = ['./external_executable'] + [request.team_1] + [request.team_2]
    res = subprocess.run(command, capture_output=True)
    return res.stdout


@app.get("/soccer_teams")
async def soccer_teams():
    LOGGER.info("Processing soccer teams get request.")
    df = get_latest_soccer_data()
    clubs = df['Club'].unique().tolist()
    return {'clubs': clubs}


@app.on_event("shutdown")
def shutdown_event():
    LOGGER.info("Application shutdown")


def compile_ls_command(request: ListRequest):
    folders = request.folders
    parameters = request.parameters
    if folders is None:
        folders = ['.']
    if parameters is None:
        parameters = []
    parameters = format_parameters(parameters)
    directory = './' + '/'.join(folders)
    if folders[0] != '.':
        directory = '/' + '/'.join(folders)
    else:
        directory = '/'.join(folders)
    command = ['ls'] + parameters + [directory]
    command = [c for c in command if c]
    return command


def handle_ls_errors(stderr):
    handle_not_found(stderr)
    handle_permission_denied(stderr)
    handle_invalid_option(stderr)


def handle_not_found(stderr):
    error_message = 'No such file or directory'
    if re.findall(error_message, str(stderr)) == [error_message]:
        LOGGER.error(f"{error_message}.")
        raise HTTPException(status_code=404, detail=f"{error_message}.")


def handle_permission_denied(stderr):
    error_message = 'Permission denied'
    if re.findall(error_message, str(stderr)) == [error_message]:
        LOGGER.error(f"{error_message}.")
        raise HTTPException(status_code=403, detail=f"{error_message}.")


def handle_invalid_option(stderr):
    error_message = 'unrecognized option'
    if re.findall(error_message, str(stderr)) == [error_message]:
        LOGGER.error(f"{error_message}.")
        raise HTTPException(status_code=400, detail="Bad request. Unrecognized option for parameter value.")


def format_parameter(p):
    if p == '':
        return p
    if len(p) == 1:
        return f"-{p}"
    else:
        return f"--{p}"


def format_parameters(parameters):
    return [format_parameter(p) for p in parameters]

