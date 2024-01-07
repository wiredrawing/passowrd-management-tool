from django import forms
from ..models import WebService


class WebServiceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # レコード更新時にはパスワード確認用フォームの必須は外す
        if kwargs.get("instance") != None:
            print("UPDATE MODE: ")
        else:
            print("CREATE MODE: ")

        for field_key in  self.fields.keys():
            if self.instance != None and field_key == "login_password_confirm":
                self.fields.get(field_key).required = False

    def clean_login_password_confirm(self):
        """ウェブサービスへのログインパスワードが
        マッチしているかどうかを確認する"""

        if self.instance == None:
            login_password = self.cleaned_data.get("login_password")
            login_password_confirm = self.cleaned_data.get("login_password_confirm")
            if login_password != login_password_confirm:
                raise forms.ValidationError("パスワードが一致しません")
            return login_password_confirm
        else:
            # self.instanceがNoneでない場合は既存のウェブサービス情報の更新処理のため
            # パスワードの変更があったかどうかを確認する
            login_password = self.cleaned_data.get("login_password")
            login_password_confirm = self.cleaned_data.get("login_password_confirm")
            if len(login_password_confirm) == 0:
                # パスワードの変更がない場合は既存のパスワードを返却する
                return self.instance.login_password
            else:
                # パスワードの変更がある場合は変更後のパスワードを返却する
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

        labels = {
            "login_id": "ログインIDあるいはメールアドレス",
        }

        fields = [
            "service_name",
            "login_url",
            "login_id",
            "login_password",
            "login_password_confirm",
            "comment",
        ]
