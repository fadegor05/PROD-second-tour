from typing import List, Annotated
from fastapi import Path, Query
from app.core.exceptions import DetailedHTTPException

from app.api.api_router import api_router
from app.crud.country import get_countries_by_region, get_country_by_alpha2
from app.schemas.country import CountryBase
from app.schemas.error import ErrorSchema

@api_router.get('/countries', responses={200: {'model': List[CountryBase]},})
def get_countries_by_region_handler(region: Annotated[List[str], Query()] = None) -> List[CountryBase]:
    countries = get_countries_by_region(region)
    return countries

@api_router.get('/countries/{alpha2}', responses={200: {'model': CountryBase}, 404: {'model': ErrorSchema},})
def get_country_by_alpha2_handler(alpha2: Annotated[str, Path()]) -> CountryBase | ErrorSchema:
    country = get_country_by_alpha2(alpha2)
    if not country:
        raise DetailedHTTPException(404, 'Страна с указанным кодом не найдена')
    return country