import csv
import inspect
import tempfile
from django.views import View
from django.http import FileResponse, HttpResponse
from blog.models import ServerInformation


class ServerInformationListDownloadView(View):

    def get(self, request):
        # インメモリファイルを作成
        fp = tempfile.TemporaryFile(mode='w+b')
        # 現在登録済みの全サーバー接続情報を取得
        server_informations = ServerInformation.objects.all()
        # またモデルで定義されているDBカラム名をすべて取得する
        columns = ServerInformation._meta.get_fields()
        headers = []
        for column in columns:
            # fpにヘッダーを書き込む
            header = column.name
            headers.append(header)
            fp.write(header.encode("sjis") + ",".encode("sjis"))
        # ヘッダー名を書き込んだ後に改行する
        fp.write("\n".encode("sjis"))

        for server_information in server_informations:
            body = [];
            for header in headers:
                if header == "server_key":
                    # 秘密鍵ファイルの中身を文字列として取得する
                    server_key_bytes = server_information.server_key.tobytes()
                    server_key_str = server_key_bytes.decode('utf-8')
                    body.append(server_key_str)
                else:
                    # ヘッダー名と同じ属性名を持つ値を取得する
                    body.append(getattr(server_information, header))
            fp.write(",".join(map(str, body)).encode("sjis"))
            fp.write("\n".encode("sjis"))

        # ファイルポインタの位置を先頭に戻してやる必要がある
        fp.seek(0)
        file_response = FileResponse(
            fp,
            as_attachment=True,
            filename="server_information_list.csv",
            content_type="application/octet-stream",
        )
        # 以下を記述しないと、ダウンロード時のファイル名が文字化けする
        file_response.set_headers({
            "Content-Disposition": "attachment; filename={}".format("server_information_list.csv"),
        })
        print(vars(file_response))
        return file_response

    def unused_get(self, request):
        # インメモリファイルを作成
        fp = tempfile.TemporaryFile(mode='w+b')
        fp.write("id,server_name,server_description,server_address,server_port,server_user,server_password,server_key,server_key_password,comment,connection_type\n".encode("sjis"))
        # 現在登録済みの全サーバー接続情報を取得
        server_informations = ServerInformation.objects.all()

        # CSVレスポンスを作成
        response = HttpResponse(content_type='text/csv; charset=Shift-JIS')
        response["Content-Disposition"] = "attachment; filename=server_information_list.csv"
        writer = csv.writer(response)
        csv_bodies = [];

        # UTF-8でかかれたCSVもエクセルで開けるようにするためにBOMをつける
        # writer.writerow((0xEF, 0xBB, 0xBF))

        for server_information in server_informations:
            body = [];
            body.append(str(server_information.id))
            body.append(server_information.server_name)
            body.append(server_information.server_description)
            body.append(server_information.server_address)
            body.append(server_information.server_port)
            body.append(server_information.server_user)
            body.append(server_information.server_password)
            # 秘密鍵ファイルの中身を文字列として取得する
            # server_key_bytes = server_information.server_key.tobytes()
            # server_key_str  = server_key_bytes.decode('utf-8')
            # body.append(server_key_str)
            # print(server_key_str)
            body.append(server_information.server_key_password)
            body.append(server_information.comment)
            body.append(server_information.connection_type_name)
            writer.writerow(body)
        print(fp)
        fp.seek(0)
        # print(fp.read())
        # print(fp.readlines())
        # return response
        # connected_csv = ""
        # for csv in csv_bodies:
        #     print(csv)
        #     connected_csv += ",".join(map(str, csv)) + "\n"
        # print(connected_csv)
        # print(connected_csv.encode("utf-8"))
        # data = bytearray(connected_csv.encode("utf-8"))
        # v = memoryview(data)
        # print(v)

        print(dir(fp))
        print(fp.file)
        print(11)
        file_response = FileResponse(
            fp,
            as_attachment=True,
            filename="server_information_list.csv",
            content_type="application/octet-stream",
        )
        # 以下を記述しないと、ダウンロード時のファイル名が文字化けする
        file_response.set_headers({
            "Content-Disposition": "attachment; filename={}".format("server_information_list.csv"),
        })
        print(vars(file_response))
        return file_response
