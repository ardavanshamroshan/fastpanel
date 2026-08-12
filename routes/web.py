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
    """
    security: /health/db returns full database_url, including username/password.
    Never expose secrets in health. Return status only.
    """

    connection = db.execute(text('SELECT 1'))
    database_version = db.execute(text('SELECT version()'))

    return {
        'status': 'OK' if connection else 'ERROR',
        'database': 'connected' if connection else 'disconnected',
        'database_url': get_settings().database.database_url,
        'database_version': database_version.fetchone()[0] if connection else None
    }
