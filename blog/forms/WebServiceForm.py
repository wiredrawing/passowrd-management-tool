from django import forms
from ..models import WebService



class WebServiceForm(forms.ModelForm):


    def clean_login_password_confirm(self):
        """ウェブサービスへのログインパスワードが
        マッチしているかどうかを確認する"""
        login_password = self.cleaned_data.get("login_password")
        login_password_confirm = self.cleaned_data.get("login_password_confirm")
        if login_password != login_password_confirm:
            raise forms.ValidationError("パスワードが一致しません")
        return login_password_confirm

    # ログインパスワード確認用フォームを追加
    login_password_confirm = forms.CharField(
        label="ログインパスワード確認",
        widget=forms.PasswordInput(),
    )

    class Meta(object):
        model = WebService

        fields = [
            "service_name",
            "login_url",
            "login_id",
            "login_password",
            "login_password_confirm",
            "comment",
        ]
