from django import forms
from ..models import ServerInformation


class ServerInformationForm(forms.ModelForm):

    def clean_server_port(self):
        server_port = self.cleaned_data.get("server_port")
        if server_port == 22:
            raise forms.ValidationError("22番ポートは使用できません")
        return server_port

    def clean_server_name(self):
        server_name = self.cleaned_data.get("server_name")
        if server_name == "NG":
            raise forms.ValidationError("NG word is not allowed")
        return server_name

    def clean_server_key_password_confirm(self):
        server_key_password = self.cleaned_data.get("server_key_password")
        server_key_password_confirm = self.cleaned_data.get("server_key_password_confirm")
        if server_key_password != server_key_password_confirm:
            raise forms.ValidationError("サーバーのパスワードが一致しません")
        return server_key_password_confirm

    def clean(self):
        cleaned_data = super().clean()

        """入力した値でバリデーションを変更する"""
        server_key_password = self.data["server_key_password"]
        server_key_password_confirm = self.data["server_key_password_confirm"]

        if server_key_password_confirm != server_key_password:
            raise forms.ValidationError("パスワード ミスマッチ")

        return cleaned_data


    """サーバーのパスフレーズの確認用フォームを追加
    ※参考URL
    https://medium.com/@kjmczk/django-custom-validators-529d3d6cba82
    """
    server_key_password_confirm = forms.CharField(
        label="(確認用)サーバーのSSHキーorFTPの秘密鍵のパスワード",
        widget=forms.TextInput(),
        required=False,
    )
    # server_password_confirmはFieldクラスのオブジェクト
    server_password_confirm = forms.CharField(
        label="(確認用)サーバーパスワード",
        # widgetsはInputクラスのオブエジェクト
        widget=forms.TextInput(),
        required=False,
    )

    class Meta(object):
        model = ServerInformation
        fields = [
            "server_name",
            "server_address",
            "server_port",
            "server_user",
            "server_password",
            "server_password_confirm",
            # 秘密鍵(フォームはファイルアップロード)
            "server_key",
            "server_key_password",
            "server_key_password_confirm",
            "comment",
        ]
        widgets = {
            # widgetsオブジェクト ～Input()系のオブジェクトを渡す
            "server_port": forms.TextInput(),
            "server_key": forms.FileInput(),
        }

        error_messages = {
            "server_name": {
                "required": "サーバー名を入力してください",
                "any_invalid": "サーバー名に使用できない文字が含まれています",
            },
            "server_address": {
                "required": "サーバーの正しいIPアドレスを入力してください",
            },
        }
