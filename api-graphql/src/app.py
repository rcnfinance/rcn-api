import os

from fastapi import FastAPI
from starlette.graphql import GraphQLApp
from schema import schema


GRAPHIQL_MODE = os.environ.get("GRAPHIQL_MODE", True)

app = FastAPI()
app.add_route("/", GraphQLApp(schema=schema, graphiql=GRAPHIQL_MODE))
