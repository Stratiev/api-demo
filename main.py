import os
import re
import subprocess
from fastapi import FastAPI, HTTPException
from typing import List, Optional

app = FastAPI()

@app.post("/ls")
async def list(folders: Optional[List[str]]=None, parameters: Optional[List[str]]=None):
    if folders is None:
        folders = ['.']
    if parameters is None:
        parameters = []
    parameters = format_parameters(parameters)
    directory = './' + '/'.join(folders)
    command = ['ls'] + parameters + [directory]
    command = [c for c in command if c]
    res = subprocess.run(command, capture_output=True)
    handle_errors(res.stderr)
    return res.stdout

def handle_errors(stderr):
    handle_not_found(stderr)
    handle_permission_denied(stderr)
    handle_invalid_option(stderr)

def handle_not_found(stderr):
    if re.findall('No such file or directory', str(stderr)) == ['No such file or directory']:
        raise HTTPException(status_code=404, detail="No such file or directory.")

def handle_permission_denied(stderr):
    if re.findall('Permission denied', str(stderr)) == ['Permission denied']:
        raise HTTPException(status_code=403, detail="Permission Denied.")

def handle_invalid_option(stderr):
    if re.findall('unrecognized option', str(stderr)) == ['unrecognized option']:
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

