from django.db import models

# 各種テーブルのID(primaryKey)をUUIDにするためのライブラリ
import uuid
from blog.validators.server_name_validator import server_name_validator


# Create your models here.
"""
テーブルのマイグレーションをロールバックする

python manage.py migrate <application name> zero
例)python manage.py migrate blog zero

テーブルのマイグレーションファイルを作成する
python manage.py makemigrations <application name>
例)python manage.py makemigrations blog

テーブルのマイグレーションを実行する
python manage.py migrate <application name>
例)python manage.py migrate blog
"""

class User(models.Model):
    # テーブル名を任意の名前で変更したい場合
    class Meta():
        db_table = "users"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=255, unique=True)
    family_name = models.CharField(max_length=255)
    given_name = models.CharField(max_length=255)
    address = models.TextField()
    zipcode = models.CharField(max_length=255)
    email = models.EmailField()
    # set the hashed password
    password = models.CharField(max_length=255)


class ServerInformation(models.Model):
    class Meta():
        db_table = "server_informations"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    server_name = models.CharField(
        validators=[
            server_name_validator,
        ],
        max_length=255,
        db_comment="サーバーの名前 同一名不可",
        # null と blankキーワード引数がともにFalseの場合は,バリデーションで必須項目となる
        # そのため基本は null=False と blank=False とする
        null=False,
        blank=False,
        unique=True,
        # required=True,
        # フォームのラベル名を変更する
        verbose_name="サーバー名",
    )
    server_description = models.TextField(
        db_comment="説明付与",
        null=False,
        blank=False,
        error_messages={"required": "説明を入力してください"},
        verbose_name="サーバーの説明",
    )
    server_address = models.CharField(
        max_length=255,
        db_comment="サーバーのIPアドレス",
        null=False,
        blank=False,
        verbose_name="サーバーのIPアドレス",
    )
    server_port = models.IntegerField(
        db_comment="サーバーのポート番号",
        null=False,
        blank=False,
        verbose_name="サーバーのポート番号",
    )
    server_user = models.CharField(
        max_length=255, db_comment="サーバーのユーザー名", null=False, blank=False,
        verbose_name="サーバーのユーザー名",
    )
    server_password = models.CharField(
        max_length=255,
        db_comment="サーバーのパスワード",
        null=False,
        blank=False,
        verbose_name="サーバーパスワード",
    )

    server_key = models.BinaryField(
        db_comment="サーバーのSSHキーorFTPの秘密鍵", null=True, blank=True, editable=True,
        verbose_name="サーバーのSSHキーorFTPの秘密鍵",
    )
    server_key_name = models.CharField(
        max_length=255,
        db_comment="サーバーのSSHキーorFTPの秘密鍵の名前",
        null=True,
        blank=True,
        verbose_name="サーバーのSSHキーorFTPの秘密鍵の名前",
    )
    server_key_password = models.CharField(max_length=255, db_comment="サーバーのSSHキーorFTPの秘密鍵のパスワード", null=False, blank=False, verbose_name="サーバーのSSHキーorFTPの秘密鍵のパスワード")
    comment = models.TextField(
        db_comment="サーバーのコメント(任意)", null=True, blank=True, db_column="comment",
        verbose_name="サーバーのコメント(任意)",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


class Post(models.Model):
    class Meta():
        db_table = "posts"

    # タイトル
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    intro = models.TextField()
    body = models.TextField()
    # 投稿日時
    posted_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    class Meta(object):
        db_table = "comments"

    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)


class WebService(models.Model):

    class Meta (object):
        db_table = "web_services"

    """
    Webサービスのモデルクラス
    利用中のウェブサービスのアカウントを管理する
    """

    # サービス名(社内も含めて)
    service_name = models.CharField(
        max_length=255,
        verbose_name="サービス名",
        null=False,
        blank=False,
        unique=True,
        error_messages={"unique": "<カスタムメッセージ>:既に登録されているサービス名です"},
    )
    # サービスへログインするためのURL
    login_url = models.URLField(
        verbose_name="ログインURL",
        null=False,
        blank=False,
    )
    # サービスへログインするためのURL
    login_id = models.CharField(
        max_length=255,
        verbose_name="ログインID",
        null=False,
        blank=False,
    )
    # サービスへログインするためのパスワード
    login_password = models.CharField(
        max_length=255,
        verbose_name="ログインパスワード",
        null=False,
        blank=False,
    )

    # memo
    comment = models.TextField(
        verbose_name="メモ",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
