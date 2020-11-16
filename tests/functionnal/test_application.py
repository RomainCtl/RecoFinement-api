import pytest
import json


class TestApplication:
    def test_get_recommended(self, test_client, headers):
        response = test_client.get("/api/application", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True