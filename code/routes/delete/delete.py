from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from code.database.aqiosqlite import get_session
from code.models.models import Item

router = APIRouter()

@router.delete("/items/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    await db.delete(item)
    await db.commit()
    return {"detail": "Item deleted"}
