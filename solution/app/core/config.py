import os
from sqlalchemy.engine import make_url
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SQLALCHEMY_DB_URL = make_url(os.environ.get('POSTGRES_CONN').replace('postgres://', 'postgresql://'))