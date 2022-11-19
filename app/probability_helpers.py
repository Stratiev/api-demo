from logger import get_logger
import re
from pydantic import BaseModel, Extra
from fastapi import HTTPException

LOGGER = get_logger(__name__)
class SoccerTeamsRequest(BaseModel):
    team_1: str='Djurgarden'
    team_2: str='Hammarby'

    # This forbids extra parameters
    class Config:
        extra = Extra.forbid

def handle_invalid_team_name(stderr):
    error_pattern = "(?<=ValueError: ).* not in the list of available club names."
    matches = re.findall(error_pattern, str(stderr))
    if matches:
        error_message = f"Bad request. Invalid team name. {matches[0]}"
        LOGGER.error(error_message)
        raise HTTPException(status_code=400, detail=error_message)


