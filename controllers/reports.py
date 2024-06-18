# routes/my_route.py
from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import FileResponse
from databases import Database
from config.db.database import get_database
from services.print_settings_service import get_item_service

router = APIRouter()

@router.get("/reports/{item_id}")
async def read_item(item_id: int, db: Database = Depends(get_database)):
    item = await get_item_service(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item