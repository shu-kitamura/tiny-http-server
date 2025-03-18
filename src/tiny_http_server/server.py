import pprint
import socket


def run_server(host="127.0.0.1", port=8080):
    # ソケットを作成
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # アドレスの再利用を許可（サーバー再起動時の「Address already in use」回避）
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 指定したホストとポートにバインド
    server_socket.bind((host, port))
    # 接続の待ち受け開始
    server_socket.listen(5)
    print(f"Starting server on {host}:{port}...")

    while True:
        # クライアントからの接続を待機
        client_conn, client_addr = server_socket.accept()
        with client_conn:
            print(f"Connected by {client_addr}")
            # リクエストデータを受信（今回はシンプルに 1024 バイト）
            request = client_conn.recv(1024)
            parse_request(request)

            # HTTP レスポンスの組み立て
            body = "Hello World"
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                f"Content-Length: {len(body)}\r\n"
                "\r\n"
                f"{body}"
            )
            # レスポンスを送信
            client_conn.sendall(response.encode("utf-8"))

def parse_request(request: str) -> dict:
    """
    生の HTTP リクエスト文字列をパースし、以下のキーを持つ辞書を返します:
      - method: HTTP メソッド
      - path: リクエストのパス
      - version: HTTP バージョン
      - headers: ヘッダーの辞書（各ヘッダーは "Key: Value" 形式でパース）
      - body: ボディ文字列
    """
    # 行ごとに分割 (このテストでは "\n" 区切り)
    lines = request.splitlines()
    if not lines:
        raise ValueError("Empty request")

    # 1行目はリクエストライン
    request_line = lines[0]
    parts = request_line.split()
    if len(parts) < 3:
        raise ValueError("Invalid request line")
    method, path, version = parts[0], parts[1], parts[2]

    # ヘッダー部分のパース (空行に到達するまで)
    headers = {}
    i = 1
    while i < len(lines) and lines[i].strip() != "":
        line = lines[i]
        # ヘッダー行は "Key: Value" 形式であることを期待
        if ":" not in line:
            raise ValueError(f"Invalid header line: {line}")
        key, value = line.split(":", 1)
        headers[key.strip()] = value.strip()
        i += 1

    # 空行以降はボディ (存在する場合)
    i += 1  # 空行をスキップ
    body = "\n".join(lines[i:]) if i < len(lines) else ""

    return {
        "method": method,
        "path": path,
        "version": version,
        "headers": headers,
        "body": body,
    }

if __name__ == "__main__":
    run_server()
