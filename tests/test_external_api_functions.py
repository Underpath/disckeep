import json
from unittest.mock import patch

from disckeep.web import musicbrainz


@patch("disckeep.web.musicbrainz.musicbrainzngs.search_artists")
def test_search_group(mock_get):
    search_results = get_data_from_file("search_results")
    mock_get.return_value = search_results
    response = musicbrainz.search_group("Alestorm")

    assert response == search_results["artist-list"]


@patch("disckeep.web.musicbrainz.musicbrainzngs.browse_release_groups")
def test_get_release_groups_for_group(mock_get):
    release_groups_for_group = get_data_from_file("release_groups_for_group")
    mock_get.return_value = release_groups_for_group
    response = musicbrainz.get_release_groups_for_group("c0252a1b-0133-46bb-8c4f-cade46349ec3")
    assert response == release_groups_for_group["release-group-list"]


def get_data_from_file(data):
    with open("tests/data/external_api_responses.json", "r") as datafile:
        return json.load(datafile)[data]
