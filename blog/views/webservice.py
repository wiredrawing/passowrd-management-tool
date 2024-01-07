from django.views.generic import View
from django.shortcuts import render, redirect
from blog.models import WebService
from blog.forms import WebServiceForm
from blog.forms.WebServiceForm import WebServiceForm


class WebServiceView(View):

    # 現在登録中のwebサービス一覧を返却する
    def get(self, request):
        web_services = WebService.objects.all()

        for web_service in web_services:
            print("web_service ======>", web_service)
            print("web_service.service_name ======>", web_service.service_name)


        return render(request, "web_service/index.html", {
            "web_services": web_services,
        })


class WebServiceDetailView(View):
    """指定したwebサービスIDの詳細情報を返却"""

    def get(self, request, web_service_id: str):
        web_service = WebService.objects.get(id=web_service_id)
        print("web_service ======>", web_service)
        print("web_service.service_name ======>", web_service.service_name)
        return render(request, "web_service/detail.html", {
            "web_service": web_service,
        })


class WebServiceCreateView(View):
    """
    新規にwebサービスを登録する
    """

    def get(self, request):
        form = WebServiceForm()
        return render(request, "web_service/create.html", {
            "form": form
        })

    def post(self, request):
        form = WebServiceForm(request.POST)

        # execute validation.
        if form.is_valid():
            web_service = form.save(commit=False)
            web_service.save()
            latest_web_service_id = web_service.id
            return redirect("web_service_detail", web_service_id=latest_web_service_id)

        # validation error.
        return render(request, "web_service/create.html", {
            "form": form
        })


class WebServiceUpdateView(View):

    def get(self, request, web_service_id: str):
        web_service = WebService.objects.get(id=web_service_id)
        form = WebServiceForm(instance=web_service)
        return render(request, "web_service/update.html",
        {
            "web_service": web_service,
            "form": form
        })

    def post(self, request, web_service_id: str):
        web_service = WebService.objects.get(pk=web_service_id)
        form = WebServiceForm(request.POST, instance=web_service)

        if form.is_valid():
            web_service = form.save(commit=False)
            web_service.save()
            updated_web_service_id = web_service.id
            return redirect("web_service_detail", web_service_id=updated_web_service_id)

        return render(request, "web_service/update.html", {
            "web_service": web_service,
            "form": form
        })
