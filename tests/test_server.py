from src.server import parse_request

def test_parse():
    request = (
        "GET / HTTP/1.1\n"
        "Host: 127.0.0.1:8080\n"
        "Connection: keep-alive\n"
        "sec-ch-ua: \"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Microsoft Edge\";v=\"134\"\n"
        "sec-ch-ua-mobile: ?0\n"
        "sec-ch-ua-platform: \"Windows\"\n"
        "Upgrade-Insecure-Requests: 1\n"
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0\n"
        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\n"
        "Sec-Fetch-Site: none\n"
        "Sec-Fetch-Mode: navigate\n"
        "Sec-Fetch-User: ?1\n"
        "Sec-Fetch-Dest: document\n"
        "Accept-Encoding: gzip, deflate, br, zstd\n"
        "Accept-Language: ja,en;q=0.9,en-GB;q=0.8,en-US;q=0.7\n"
        "\n"
        "request-body-data"
    )

    expect = {
        "method": "GET",
        "path": "/",
        "version": "HTTP/1.1",
        "body": "request-body-data",
        "headers": {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "ja,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
                "Connection": "keep-alive",
                "Host": "127.0.0.1:8080",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
                "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Microsoft Edge\";v=\"134\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\""
            }
    }

    assert parse_request(request) == expect
    
