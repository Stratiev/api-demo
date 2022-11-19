import time
import os
import re
import subprocess
from logger import get_logger
from pydantic import BaseModel, Extra
from fastapi import FastAPI, HTTPException
from typing import List, Optional

LOGGER = get_logger(__name__)

app = FastAPI()

class ListRequest(BaseModel):
    folders: Optional[List[str]]=None
    parameters: Optional[List[str]]=None

    # This forbids extra parameters
    class Config:
        extra = Extra.forbid

defaults = {'folders': None, 'parameters': None}
default_ls_request = ListRequest(**defaults)

@app.post("/ls")
async def ls(request: ListRequest=default_ls_request):
    LOGGER.info("Processing ls request.")
    command = compile_command(request)
    res = subprocess.run(command, capture_output=True)
    handle_errors(res.stderr)
    return res.stdout


@app.post("/blocking_ls")
async def blocking_ls(request: ListRequest=default_ls_request):
    LOGGER.info("Processing blocking_ls request.")
    command = compile_command(request)
    res = subprocess.run(command, capture_output=True)
    handle_errors(res.stderr)
    time.sleep(5)
    return res.stdout


@app.on_event("shutdown")
def shutdown_event():
    LOGGER.info("Application shutdown")

def compile_command(request: ListRequest):
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

def handle_errors(stderr):
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

