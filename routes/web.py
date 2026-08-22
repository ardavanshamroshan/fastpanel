from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from config.settings import get_settings
from database.connection import get_db

router = APIRouter(tags=['health'])


@router.get('/health')
def health():
    return {'status': 'OK'}


@router.get('/health/db')
def health_db(db: Session = Depends(get_db)):
    db.execute(text('SELECT 1'))

    return {
        'status': 'OK',
        'database': 'connected',
    }
