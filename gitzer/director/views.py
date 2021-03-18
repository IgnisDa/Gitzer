from ariadne.contrib.django.views import GraphQLView
from django.conf import settings
from django.http import HttpRequest


class GitzerGraphQLView(GraphQLView):
    def post(self, request: HttpRequest, *args, **kwargs):
        data = self.extract_data_from_json_request(request)
        query = data.get("query")
        if "typename" in query:
            with open(settings.GITZER_LOGGING_FILE, "a") as f:
                if "mutation" in query:
                    f.write("Performed mutation\n")
                else:
                    f.write("Performed query\n")
        return super(GitzerGraphQLView, self).post(request, *args, **kwargs)
