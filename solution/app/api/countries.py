from typing import List, Annotated
from fastapi import Path, Query

from app.api.api_router import api_router
from app.crud.country import get_countries_by_region, get_country_by_alpha
from app.schemas.country import CountryBase

@api_router.get('/countries')
def get_countries_by_region_handler(region: Annotated[str, Query()] = None) -> List[CountryBase]:
    return get_countries_by_region(region)

@api_router.get('/countries/{alpha}')
def get_country_by_alpha_handler(alpha: Annotated[str, Path()]) -> CountryBase:
    return get_country_by_alpha(alpha)