from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    snake_case_fallback_resolvers,
)
from director.api import resolvers as director_resolvers

type_defs = [
    load_schema_from_path("./gitzer/api/schema.graphql"),
    load_schema_from_path("./director/api/schema.graphql"),
]
schema = make_executable_schema(
    type_defs,
    [director_resolvers.query],
    snake_case_fallback_resolvers,
)
