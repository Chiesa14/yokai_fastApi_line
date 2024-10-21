import functools
from fastapi import HTTPException, Header
from datetime import datetime,timedelta
import jwt


SECRET_KEY = "2ec26ad9-e039-445e-915e-a482dc6f5e3b"
ALGORITHM = "HS256"