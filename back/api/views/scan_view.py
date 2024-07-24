from fastapi import APIRouter
from typing import List
from core.controllers.scan_controller import ScanController
from core.schema import Manga

router = APIRouter()


@router.get("/scans", response_model=List[Manga])
def get_scans():
    return ScanController.get_scans()
