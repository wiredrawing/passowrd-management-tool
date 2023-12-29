import inspect

from django.views.generic import View

from django.shortcuts import render
from django.http import FileResponse
from blog.forms.ServerInformationForm import ServerInformationForm
from django.shortcuts import redirect
from blog.models import ServerInformation
from django.forms.models import model_to_dict


class ServerInformationView(View):
    """
    現在登録中のサーバー接続情報一覧を返却する
    """

    def get(self, request):
        server_informations = ServerInformation.objects.all()
        for server in server_informations:
            print(server.id)
            print(server.server_name)
        return render(request, "server/index.html", {
            "server_informations": server_informations,
        })

    def post(self, request):
        print(request.POST)
        form = ServerInformationForm(request.POST)
        if form.is_valid():
            # この時点ではまだ未コミット?
            server_information = form.save(commit=False)
            server_information.save()
            return redirect("server")
            # return render(request, "server/detail.html")
        else:
            return redirect("server")


class ServerInformationDetailView(View):

    def get(self, request, server_information_id: str):
        server_information = ServerInformation.objects.get(id=server_information_id)
        print(server_information.server_key)
        members = inspect.getmembers(server_information.server_key)
        # print(server_information.server_key.tolist())
        # print(server_information.server_key.tobytes())
        for member in members:
            print(member[0])
            print(member[1])
        return render(request, "server/server_information/get.html", {
            "server_information": server_information,
        })

    def post(self, request, server_information_id: str):
        return ""


class ServerInformationCreateView(View):

    def get(self, request):
        # サーバー情報登録用フォーム
        form = ServerInformationForm()
        print(form.data)
        return render(request, "server/create.html", {
            "form": form,
        })

    def post(self, request):
        print(request.POST)
        form = ServerInformationForm(request.POST)

        if form.is_valid():
            # 先にアップロードされたファイルを処理する
            uploaded_file = request.FILES.get("server_key")
            # print(uploaded_file)
            # print(type(uploaded_file))
            secret_key_binary = handle_uploaded_file(uploaded_file)
            print("secret_key_binary ===> ", secret_key_binary)
            for uploaded_file_key in dir(uploaded_file):
                print(uploaded_file_key)

            # commit=TrueでDBへの保存を実行(デフォルトはFalse)
            server_information = form.save(commit=False)
            server_information.server_key = secret_key_binary
            server_information.server_key_name = uploaded_file.name
            server_information.save()
            print(type(server_information))


            return redirect("server_information_detail", server_information_id=server_information.id)
        else:
            pure_errors = dict(form.errors.items())
            print("form.errors ===> ", pure_errors)
            # 登録フォームへ戻る
            return render(request, "server/create.html", {"form": form})


class ServerInformationUpdateView(View):

    def get(self, request, server_information_id: str):
        server_information = ServerInformation.objects.get(pk=server_information_id)

        form = ServerInformationForm(None, instance=server_information)
        # print(form)
        # print(form.get_context())
        # print(form.data)
        # Formオブジェクトのメソッド一覧
        members = inspect.getmembers(form)
        for member in members:
            if callable(member[1]):
                print(member[0])
        return render(request, "server/update/get.html", {
            "form": form,
            "server_information": server_information,
        })

    def post(self, request, server_information_id: str):
        current_server_information = ServerInformation.objects.get(pk=server_information_id)
        print(current_server_information.id)
        print(current_server_information.server_name)
        print(current_server_information.server_address)

        # フォーム更新時は,キーワード引数<instance>で更新対象のオブジェクトを渡す
        form = ServerInformationForm(request.POST, instance=current_server_information)
        if form.is_valid():
            # この時点ではまだ未コミット?
            server_information = form.save(commit=False)
            print(type(server_information))
            server_information.save()
            return redirect("server_information_detail", server_information_id=server_information_id)
        else:
            print("form.errors ===> ")
            print(form.errors)
            return render(request, "server/update/get.html", {
                "form": form,
                "server_information": current_server_information,
            })
            # raise Exception("invalid form")


class ServerInformationDownloadServerKeyView(View):

    def get (self, request, server_information_id: str):
        server_information = ServerInformation.objects.get(pk=server_information_id)

        # content_type="application/octet-stream"でダウンロードさせる
        return FileResponse(
            server_information.server_key,
            as_attachment=True,
            filename=server_information.server_key_name,
            content_type="application/octet-stream",
        )


    def post (self, request, server_information_id: str):
        return ""



def handle_uploaded_file(f)->bytes:
    """
    アップロードされた秘密鍵ファイルの中身を取得して
    そのままDBのレコードに登録する
    """
    secret_key_binary = []
    for chunk in f.chunks():
        secret_key_binary.append(chunk)
    return b"".join(secret_key_binary)
