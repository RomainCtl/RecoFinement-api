import pytest
import json


class TestAuth:
    def test_login(self, test_client):
        response = test_client.post("/api/auth/login", json=dict(email="", password=""))
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['user']['email'] == ""
