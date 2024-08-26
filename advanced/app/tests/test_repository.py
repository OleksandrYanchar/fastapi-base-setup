import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from src.repositories.product import ProductRepository
from src.configs.db import MONGO_URL
from src.inputs.products import ProductFilter

@pytest.fixture
def mock_client():
    client = AsyncIOMotorClient(MONGO_URL)
    return client

@pytest.fixture
async def product_repo(mock_client):
    repo = ProductRepository(mock_client)
    # Clear collection before running tests
    await repo.collection.delete_many({})
    # Create a test product
    await repo.create({"title": "Test Product", "price": 100, "description": "A test product", "photos": []})
    return repo

@pytest.mark.asyncio
async def test_find_by_id(product_repo):
    repo = await product_repo
    product = await repo.create({"title": "Product1", "price": 50, "description": "Description1", "photos": []})
    print(f"Created product: {product}")
    found_product = await repo.find_by_id(str(product._id))
    print(f"Found product by id: {found_product}")
    assert found_product is not None, "Product not found"
    assert str(found_product.id) == str(product.id)

@pytest.mark.asyncio
async def test_get(product_repo):
    repo = await product_repo
    product = await repo.create({"title": "Product2", "price": 75, "description": "Description2", "photos": []})
    print(f"Created product: {product}")
    found_product = await repo.get(title="Product2")
    print(f"Found product by get: {found_product}")
    assert found_product is not None, "Product not found"
    assert found_product.title == "Product2"

@pytest.mark.asyncio
async def test_get_many(product_repo):
    repo = await product_repo
    await repo.create({"title": "Product3", "price": 25, "description": "Description3", "photos": []})
    filters = ProductFilter(title="Product3", min_price=20, max_price=30)
    products = await repo.get_many(filters)
    print(f"Found products by get_many: {products}")
    assert len(products) == 1, f"Expected 1 product, found {len(products)}"
    assert products[0].title == "Product3"

@pytest.mark.asyncio
async def test_create(product_repo):
    repo = await product_repo
    new_product = {"title": "Product4", "price": 125, "description": "Description4", "photos": []}
    created_product = await repo.create(new_product)
    print(f"Created product: {created_product}")
    assert created_product.title == "Product4"
    assert created_product.price == 125

@pytest.mark.asyncio
async def test_delete(product_repo):
    repo = await product_repo
    product = await repo.create({"title": "Product5", "price": 200, "description": "Description5", "photos": []})
    print(f"Created product: {product}")
    delete_status = await repo.delete(str(product._id))
    print(f"Delete status: {delete_status}")
    assert delete_status is True, "Product not deleted"
    found_product = await repo.find_by_id(str(product._id))
    print(f"Found product after delete: {found_product}")
    assert found_product is None, "Product still exists after deletion"

@pytest.mark.asyncio
async def test_update(product_repo):
    repo = await product_repo
    product = await repo.create({"title": "Product6", "price": 150, "description": "Description6", "photos": []})
    print(f"Created product: {product}")
    updated_data = {"price": 175}
    updated_product = await repo.update(str(product._id), updated_data)
    print(f"Updated product: {updated_product}")
    assert updated_product is not None, "Product not found after update"
    assert updated_product.price == 175
