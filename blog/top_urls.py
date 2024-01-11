from django.urls import path
from blog.views.toppage import TopView




urlpatterns = [
    path("", TopView.as_view(), name="top"),
]
