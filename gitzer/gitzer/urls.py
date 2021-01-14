from director import views
from django.contrib import admin
from django.urls import path

from gitzer.api.graphql_config import schema

urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql/", views.GitzerGraphQLView.as_view(schema=schema), name="graphql"),
]
