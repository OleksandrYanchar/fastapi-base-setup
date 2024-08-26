from strawberry.fastapi import GraphQLRouter
from src.repositories.product import product_repo
from src.resolvers.products import schema

async def get_context():
    return {
        "product_repo": product_repo
    }

graphql_app = GraphQLRouter(schema, context_getter=get_context)
