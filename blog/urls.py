from django.urls import path

from blog.views.server import (
    ServerInformationView,
    ServerInformationDetailView,
    ServerInformationCreateView,
    ServerInformationUpdateView,
    ServerInformationDownloadServerKeyView,
)

# server_information独自のルーティング
urlpatterns = [
    path("", ServerInformationView.as_view(), name="server_information"),
    path(
        "create/",
        ServerInformationCreateView.as_view(),
        name="server_information_create"
    ),
    # 指定したサーバーIDの詳細情報を返却
    path(
        "<str:server_information_id>/detail/",
        ServerInformationDetailView.as_view(),
        name="server_information_detail"
    ),
    # 指定したサーバーIDの秘密鍵をDownload
    path(
        "<str:server_information_id>/download/",
        ServerInformationDownloadServerKeyView.as_view(),
        name="server_information_download_server_key"
    ),
    path(
        "<str:server_information_id>/update/",
        ServerInformationUpdateView.as_view(),
        name="server_information_update"
    ),
]
