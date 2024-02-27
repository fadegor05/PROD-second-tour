from pydantic import BaseModel

class CountryBase(BaseModel):
    name: str
    alpha2: str
    alpha3: str
    region: str
