from django.views.generic import View
from django.shortcuts import render, redirect



class TopView(View):

    def get(self, request):
        print("TopView.get()")
        # Topページを表示
        return render(request, "top/index.html")
