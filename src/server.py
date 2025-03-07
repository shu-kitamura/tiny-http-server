import socket

def run_server(host='127.0.0.1', port=8080):
    # ソケットを作成
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # アドレスの再利用を許可（サーバー再起動時の「Address already in use」回避）
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 指定したホストとポートにバインド
    server_socket.bind((host, port))
    # 接続の待ち受け開始
    server_socket.listen(5)
    print(f'Starting server on {host}:{port}...')

    while True:
        # クライアントからの接続を待機
        client_conn, client_addr = server_socket.accept()
        with client_conn:
            print(f'Connected by {client_addr}')
            # リクエストデータを受信（今回はシンプルに 1024 バイト）
            request = client_conn.recv(1024)
            print("Request received:")
            print(request.decode('utf-8', errors='replace'))
            
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
            client_conn.sendall(response.encode('utf-8'))

if __name__ == '__main__':
    run_server()
