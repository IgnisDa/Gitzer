from datetime import datetime

from ariadne.contrib.django.views import GraphQLView
from django.conf import settings
from django.http import HttpRequest


class GitzerGraphQLView(GraphQLView):
    def post(self, request: HttpRequest, *args, **kwargs):
        data = self.extract_data_from_json_request(request)
        query = data.get("query")
        now = datetime.now()
        if "typename" in query:
            with open(settings.GITZER_LOGGING_FILE, "a") as f:
                if "mutation" in query:
                    write = f"{now}: Performed mutation\n"
                else:
                    write = f"{now}: Performed query\n"
                f.write(write)
        return super(GitzerGraphQLView, self).post(request, *args, **kwargs)
