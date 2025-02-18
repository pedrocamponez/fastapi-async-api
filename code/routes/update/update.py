from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from code.database.aqiosqlite import get_session
from code.models.models import Item
from code.schemas.schemas import ItemCreate, ItemRead

router = APIRouter()

@router.put("/items/{item_id}", response_model=ItemRead)
async def update_item(item_id: int, item: ItemCreate, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Item).where(Item.id == item_id))
    existing_item = result.scalars().first()
    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")
    existing_item.name = item.name
    existing_item.description = item.description
    await db.commit()
    await db.refresh(existing_item)
    return existing_item
