import os
import sys

import pytest

from unittest.mock import Mock

sys.path.append(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))
)

import tmdb_client
from main import app


def get_poster_url_uses_default_size():
    poster_api_path = "some-poster_path"
    expected_default_size = "w342"
    poster_url = tmdb_client.get_poster_url(poster_api_path=poster_api_path)
    assert expected_default_size in poster_url


def test_get_movies_list_type_popular():
    movies_list = tmdb_client.get_movies_list(list_type="popular")
    assert movies_list is not None


def test_api_call(monkeypatch):
    mock_return = 1
    mock_endpoint = "https://api.themoviedb.org/3/movie"

    requests_mock = Mock()
    response = requests_mock.return_value
    response.json.return_value = mock_return
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

    api_call = tmdb_client.api_call(mock_endpoint)
    assert api_call == mock_return


def test_get_movies_list(monkeypatch):
    mock_movies_list = ["Movie 1", "Movie 2"]

    requests_mock = Mock()
    requests_mock.return_value = mock_movies_list
    monkeypatch.setattr("tmdb_client.api_call", requests_mock)

    movies_list = tmdb_client.get_movies_list(list_type="popular")
    assert movies_list == mock_movies_list


def test_get_single_movie(monkeypatch):
    mock_movie = "Movie"

    requests_mock = Mock()
    requests_mock.return_value = mock_movie
    monkeypatch.setattr("tmdb_client.api_call", requests_mock)

    movie = tmdb_client.get_single_movie(0)
    assert movie == mock_movie


def test_get_movie_image(monkeypatch):
    mock_image_url = "url"

    requests_mock = Mock()
    requests_mock.return_value = mock_image_url
    monkeypatch.setattr("tmdb_client.get_poster_url", requests_mock)

    poster = tmdb_client.get_poster_url("path")
    assert poster == mock_image_url


def test_get_single_movie_cast(monkeypatch):
    mock_cast = ["Actor 1", "Actor 2"]

    requests_mock = Mock()
    requests_mock.return_value = mock_cast
    monkeypatch.setattr("tmdb_client.get_single_movie_cast", requests_mock)

    cast = tmdb_client.get_single_movie_cast(1000)
    assert cast == mock_cast


@pytest.mark.parametrize("list_type",
                         (("now_playing"),
                          ("popular"),
                          ("top_rated"),
                          ("upcoming")))
def test_homepage(monkeypatch, list_type):
   api_mock = Mock(return_value={"results": []})
   monkeypatch.setattr("tmdb_client.api_call", api_mock)

   with app.test_client() as client:
       response = client.get(f"/?list_type={list_type}")
       assert response.status_code == 200
       api_mock.assert_called_once_with(f"movie/{list_type}")
