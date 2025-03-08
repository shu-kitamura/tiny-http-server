import socket
import pprint

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
            client_conn.sendall(response.encode('utf-8'))

def parse_request(request: bytes):
    # parse HTTP request
    result = {
        "request_line": {
            "method": "",
            "path": "",
            "protocol": ""},
        "headers": {},
        "body": ""
    }
    decoded_request = request.decode('utf-8')
    splited_request = decoded_request.split('\r\n')
    request_line = splited_request[0].split(" ")
    if len(request_line) == 3:
        result["request_line"]["method"] = request_line[0]
        result["request_line"]["path"] = request_line[1]
        result["request_line"]["protocol"] = request_line[2]
    else:
        print("Invalid Request")

    for header in splited_request[1:]:
        if header == "":
            break
        key, value = header.split(": ")
        result["headers"][key] = value

    pprint.pprint(result)    
    

if __name__ == '__main__':
    run_server()
