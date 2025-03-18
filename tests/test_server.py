from src.tiny_http_server import server


def test_init_server():
    hserver = server.HttpServer("192.168.0.1", 8080)
    assert hserver.ip_address == "192.168.0.1"
    assert hserver.port == 8080
