import strawberry
from strawberry.types import Info
from typing import List, Optional
from src.inputs.products import ProductInput, ChangeProductDiscountInput, ProductFilter
from src.object_types.products import ProductType
from src.repositories.product import ProductRepository

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_product(self, info: Info, input: ProductInput) -> ProductType:
        product_repo: ProductRepository = info.context['product_repo']
        product_data = input.__dict__
        return await product_repo.create(product_data)

    @strawberry.mutation
    async def update_product(self, info: Info, id: str, input: ProductInput) -> Optional[ProductType]:
        product_repo: ProductRepository = info.context['product_repo']
        update_data = input.__dict__
        return await product_repo.update(id, update_data)

    @strawberry.mutation
    async def change_product_discount(self, info: Info, input: ChangeProductDiscountInput) -> Optional[ProductType]:
        product_repo: ProductRepository = info.context['product_repo']
        product = await product_repo.get(input.id)
        if product:
            product.discount = input.discount
            return await product_repo.update(input.id, product.__dict__)
        return None

@strawberry.type
class Query:
    @strawberry.field
    async def get_product(self, info: Info, id: str) -> Optional[ProductType]:
        product_repo: ProductRepository = info.context['product_repo']
        return await product_repo.get(id)

    @strawberry.field
    async def get_products(self, info: Info, filters: Optional[ProductFilter] = None) -> List[ProductType]:
        product_repo: ProductRepository = info.context['product_repo']
        if filters is None:
            filters = ProductFilter()
        return await product_repo.get_many(filters)

schema = strawberry.Schema(query=Query, mutation=Mutation)
