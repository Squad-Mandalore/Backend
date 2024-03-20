import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import FileResponse
from src.database.database_utils import get_db
from src.services.csv_service import entity_config, create_csv


router = APIRouter(
    # routing prefix
    prefix="/csv",
    # documentation tag
    tags=["csv"],
    # default response
    #responses={404: {"route": "Not found"}}
)

@router.get("/trainer.csv", response_class=FileResponse, status_code=status.HTTP_200_OK)
async def read_trainer_csv(db: Session = Depends(get_db)) -> FileResponse:
    create_csv(db)
    if not os.path.exists(f"{entity_config['Trainer']['filename']}"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Csv file not found")

    return FileResponse(f"{entity_config['Trainer']['filename']}")

@router.get("/athlete.csv", response_class=FileResponse, status_code=status.HTTP_200_OK)
async def read_athlete_csv(db: Session = Depends(get_db)) -> FileResponse:
    create_csv(db)
    if not os.path.exists(f"{entity_config['Athlete']['filename']}"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Csv file not found")

    return FileResponse(f"{entity_config['Athlete']['filename']}")

@router.get("/completes.csv", response_class=FileResponse, status_code=status.HTTP_200_OK)
async def read_completes_csv(db: Session = Depends(get_db)) -> FileResponse:
    create_csv(db)
    if not os.path.exists(f"{entity_config['Completes']['filename']}"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Csv file not found")

    return FileResponse(f"{entity_config['Completes']['filename']}")
