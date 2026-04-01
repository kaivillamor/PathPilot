from unittest.mock import patch, MagicMock
import requests
from services.usajobs import get_usajobs
from services.theirstack import get_theirstack

# usajobs tests

def test_usajobs_timeout():
    with patch("services.usajobs.requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.Timeout
        result = get_usajobs("1550")
        assert "error" in result

def test_usajobs_bad_status():
    with patch("services.usajobs.requests.get") as mock_get:
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError
        result = get_usajobs("1550")
        assert "error" in result

def test_usajobs_empty_results():
    with patch("services.usajobs.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "SearchResult": {
                "SearchResultItems": []
            }
        }
        mock_get.return_value = mock_response
        result = get_usajobs("1550")
        assert result == []
                    

def test_usajobs_missing_fields():
    with patch("services.usajobs.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "SearchResult": {
                "SearchResultItems": [
                    {"MatchedObjectDescriptor": {}}
                ]
            }
        }
        mock_get.return_value = mock_response
        result = get_usajobs("1550")
        assert result[0]["title"]
        assert result[0]["salary_min"] is None
        assert result[0]["remote"] is None
        assert result[0]["url"] is None

# ----------------------------------------------
# theirstack tests

def test_theirstack_timeout():
    with patch("services.theirstack.requests.post") as mock_post:
        mock_post.side_effect = requests.exceptions.Timeout
        result = get_theirstack(["Software Engineer"])
        assert "error" in result

def test_theirstack_bad_status():
    with patch("services.theirstack.requests.post") as mock_post:
        mock_post.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError
        result = get_theirstack(["Software Engineer"])
        assert "error" in result

def test_theirstack_empty_results():
    with patch("services.theirstack.requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": []}
        mock_post.return_value = mock_response
        result = get_theirstack(["Software Engineer"])
        assert result == []
        
def test_theirstack_missing_fields():
    with patch("services.theirstack.requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": [{}]}
        mock_post.return_value = mock_response
        result = get_theirstack(["Software Engineer"])
        assert result[0]["title"] is None
        assert result[0]["salary_min"] is None
        assert result[0]["location"] is None
        