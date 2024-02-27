from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Country(Base):
    __tablename__ = 'countries'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    alpha2: Mapped[str]
    alpha3: Mapped[str]
    region: Mapped[str]