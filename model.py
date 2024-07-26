from pydantic import BaseModel


class CityRequest(BaseModel):
    city: str
    user_id: str


class AutocompleteRequest(BaseModel):
    query: str
