from django import forms
from ..models import ServerInformation
from blog.application_config import connection_type_choices


class ServerInformationForm(forms.ModelForm):

    def clean_server_password_confirm(self):
        server_password = self.cleaned_data.get("server_password")
        server_password_confirm = self.cleaned_data.get("server_password_confirm")
        if server_password != server_password_confirm:
            raise forms.ValidationError("サーバーのパスワードが一致しません")
        return server_password_confirm

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

    def clean_server_key_password(self):
        server_key_password = self.cleaned_data.get("server_key_password");
        server_key = self.cleaned_data.get("server_key")
        # print("server_key_password ======>", server_key_password)
        # print("server_key ======>", server_key)
        if server_key_password and not server_key:
            raise forms.ValidationError("秘密鍵のパスフレーズを入力する場合は、秘密鍵をアップロードしてください")
        return server_key_password

    def clean_server_key(self):
        # print("self.cleaned_data.get('server_key') ======>", self.cleaned_data)
        server_key = self.cleaned_data.get("server_key")
        # print("FILE ======>", server_key)
        server_key_password = self.cleaned_data.get("server_key_password")
        # print("server_key_password ======>", server_key_password)
        if server_key_password and not server_key:
            raise forms.ValidationError("秘密鍵のパスフレーズを入力する場合は、秘密鍵をアップロードしてください")
        return server_key

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

    server_key = forms.FileField(
        label="サーバーのSSHキーorFTPの秘密鍵",
        required=False,
        widget=forms.FileInput(),
    )

    # 接続タイプをプルダウンメニューでフォームに表示
    connection_type = forms.ChoiceField(
        label="接続タイプ",
        choices=connection_type_choices,
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
            "connection_type",
            "comment",
        ]
        widgets = {
            # widgetsオブジェクト ～Input()系のオブジェクトを渡す
            "server_port": forms.TextInput(),
            # "server_key": forms.FileInput(),
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
