from typing import List
from sqlalchemy import select

from app.schemas.country import CountryBase
from app.models.country import Country

from app.db.session import Session

def get_countries_by_region(region: str | None) -> List[CountryBase]:
    if region:
        stmt = select(Country).where(Country.region == region)
    else:
        stmt = select(Country)
    with Session() as session:
        result = session.execute(stmt)
        countries = result.scalars().all()
        return countries

def get_country_by_alpha(alpha: str) -> CountryBase:
    stmt = select(Country).where(Country.alpha2 == alpha)
    with Session() as session:
        result = session.execute(stmt)
        country = result.scalar_one_or_none()
        return country