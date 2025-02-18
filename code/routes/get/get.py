from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from code.database.aqiosqlite import get_session
from code.models.models import Item
from code.schemas.schemas import ItemRead

router = APIRouter()

@router.get("/items/", response_model=list[ItemRead])
async def read_items(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Item))
    items = result.scalars().all()
    return items

@router.get("/items/{item_id}", response_model=ItemRead)
async def read_item(item_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
