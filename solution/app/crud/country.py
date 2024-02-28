from typing import List
from sqlalchemy import select

from app.schemas.country import CountryBase
from app.models.country import Country

from app.db.session import Session

def get_countries_by_region(region: List[str] | None) -> List[CountryBase]:
    if region:
        stmt = select(Country).where(Country.region.in_(region)).order_by(Country.alpha2)
    else:
        stmt = select(Country)
    with Session() as session:
        result = session.execute(stmt)
        countries = result.scalars().all()
        return countries

def get_country_by_alpha2(alpha2: str) -> CountryBase | None:
    stmt = select(Country).where(Country.alpha2 == alpha2)
    with Session() as session:
        result = session.execute(stmt)
        country = result.scalar_one_or_none()
        return country