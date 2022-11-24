import re
from typing import List, Optional

from fastapi import HTTPException
from pydantic import BaseModel, Extra

from logger import get_logger

LOGGER = get_logger(__name__)

class ListRequest(BaseModel):
    folders: Optional[List[str]]=["."]
    parameters: Optional[List[str]]=[""]

    # This forbids extra parameters
    class Config:
        extra = Extra.forbid

def compile_ls_command(request: ListRequest):
    folders = request.folders
    parameters = request.parameters
    if folders is None:
        folders = ["."]
    if parameters is None:
        parameters = [""]
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
    handle_directory_not_found(stderr)
    handle_ls_permission_denied(stderr)
    handle_ls_invalid_option(stderr)

def handle_directory_not_found(stderr):
    error_message = 'No such file or directory'
    if re.findall(error_message, str(stderr)) == [error_message]:
        LOGGER.error(f"{error_message}.")
        raise HTTPException(status_code=404, detail=f"{error_message}.")

def handle_ls_permission_denied(stderr):
    error_message = 'Permission denied'
    if re.findall(error_message, str(stderr)) == [error_message]:
        LOGGER.error(f"{error_message}.")
        raise HTTPException(status_code=403, detail=f"{error_message}.")

def handle_ls_invalid_option(stderr):
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
