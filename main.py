from fastapi import FastAPI
from code.database.aqiosqlite import engine, Base
from code.routes.create.create import router as create_router
from code.routes.delete.delete import router as delete_router
from code.routes.get.get import router as get_router
from code.routes.update.update import router as update_router

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Include routers from different modules
app.include_router(create_router)
app.include_router(delete_router)
app.include_router(get_router)
app.include_router(update_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
