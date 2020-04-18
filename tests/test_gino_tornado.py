import pytest
import tornado.httpclient


@pytest.mark.gen_test
def test_hello_world(http_client, base_url):
    response = yield http_client.fetch(base_url)
    assert response.code == 200

    with pytest.raises(tornado.httpclient.HTTPClientError, match="404"):
        yield http_client.fetch(base_url + "/user/1")

    response = yield http_client.fetch(
        base_url + "/user", method="POST", body="name=fantix"
    )
    assert response.code == 200
    assert b"fantix" in response.body

    response = yield http_client.fetch(base_url + "/user/1")
    assert response.code == 200
    assert b"fantix" in response.body

    response = yield http_client.fetch(base_url)
    assert response.code == 200
    assert b"fantix" in response.body
