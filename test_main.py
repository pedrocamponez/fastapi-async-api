import pytest
from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_create_and_get_item():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Test creating an item
        create_payload = {"name": "Test Item", "description": "Test description"}
        create_response = await client.post("/items/", json=create_payload)
        assert create_response.status_code == 200
        created_item = create_response.json()
        assert created_item["name"] == "Test Item"
        item_id = created_item["id"]

        # Test reading the created item
        get_response = await client.get(f"/items/{item_id}")
        assert get_response.status_code == 200
        fetched_item = get_response.json()
        assert fetched_item["id"] == item_id
        assert fetched_item["name"] == "Test Item"


@pytest.mark.asyncio
async def test_update_item():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create an item to update
        create_payload = {"name": "Old Name", "description": "Old description"}
        create_response = await client.post("/items/", json=create_payload)
        item_id = create_response.json()["id"]

        # Update the item
        update_payload = {"name": "New Name", "description": "New description"}
        update_response = await client.put(f"/items/{item_id}", json=update_payload)
        assert update_response.status_code == 200
        updated_item = update_response.json()
        assert updated_item["name"] == "New Name"


@pytest.mark.asyncio
async def test_delete_item():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create an item to delete
        create_payload = {"name": "To Delete", "description": "Delete me"}
        create_response = await client.post("/items/", json=create_payload)
        item_id = create_response.json()["id"]

        # Delete the item
        delete_response = await client.delete(f"/items/{item_id}")
        assert delete_response.status_code == 200
        assert delete_response.json()["detail"] == "Item deleted"

        # Confirm that the item no longer exists
        get_response = await client.get(f"/items/{item_id}")
        assert get_response.status_code == 404
