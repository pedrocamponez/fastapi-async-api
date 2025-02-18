from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from code.database.aqiosqlite import get_session
from code.schemas.schemas import ItemCreate, ItemRead
from code.models.models import Item

router = APIRouter()

@router.post("/items/", response_model=ItemRead)
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_session)):
    new_item = Item(name=item.name, description=item.description)
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item
