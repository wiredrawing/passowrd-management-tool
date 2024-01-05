from django.urls import path

from blog.views.webservice import (
    WebServiceView,
    WebServiceCreateView,
    WebServiceDetailView,
    WebServiceUpdateView,
)

urlpatterns = [

    # 登録中のwebサービス一覧を返却する
    path("", WebServiceView.as_view(), name="web_service"),
    # 指定したwebサービスIDの詳細情報を返却
    path(
        "detail/<str:web_service_id>/",
        WebServiceDetailView.as_view(),
        name="web_service_detail"),
    # 新規にwebサービスを登録する
    path(
        "create/",
        WebServiceCreateView.as_view(),
        name="web_service_create"
    ),
    # 指定したwebサービスIDの情報を更新する
    path(
        "update/<str:web_service_id>/",
        WebServiceUpdateView.as_view(),
        name="web_service_update",
    ),
]
