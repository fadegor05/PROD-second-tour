from typing import List
from sqlalchemy import select, distinct

from app.schemas.country import CountryBase
from app.models.country import Country

from app.db.session import Session

def get_regions() -> List[str]:
    stmt = select(distinct(Country.region))
    with Session() as session:
        result = session.execute(stmt)
        regions = result.scalars().all()
        return regions

def get_countries_by_region(regions: List[str] | None) -> List[CountryBase]:
    stmt = select(Country)
    if regions:
        existing_regions = get_regions()
        for region in regions:
            if region not in existing_regions:
                return None
        stmt = stmt.where(Country.region.in_(regions))     
    stmt = stmt.order_by(Country.alpha2)
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