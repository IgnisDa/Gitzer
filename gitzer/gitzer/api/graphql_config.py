import glob

from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    snake_case_fallback_resolvers,
)
from director.api import resolvers as director_resolvers
from django.conf import settings

type_defs = [
    load_schema_from_path(f)
    for f in glob.glob(str(settings.BASE_DIR / "*" / "api" / "schema" / "*.graphql"))
]

schema = make_executable_schema(
    type_defs,
    [director_resolvers.query, director_resolvers.mutation],
    snake_case_fallback_resolvers,
)
