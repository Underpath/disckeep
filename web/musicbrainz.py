import musicbrainzngs

from . import keep

PAGE_SIZE = 50

musicbrainzngs.set_useragent(
    "disckeep",
    "0.1",
    "https://github.com/Underpath/disckeep",
)


def search_group(name: str):
    result = musicbrainzngs.search_artists(artist=name, type="group", limit=5)
    return result.get("artist-list", [])


def get_group(id: str):
    group = musicbrainzngs.get_artist_by_id(id).get("artist")
    return group


def get_release_groups_for_group(group_id):
    print(f'Getting all releases for group "{group_id}".')
    tracked_release_types = keep.get_tracked_release_group_types()
    offset = 0
    count = 1
    page = 1
    all_release_groups = []
    while count > offset:
        release_group_set = musicbrainzngs.browse_release_groups(
            artist=group_id, release_type=tracked_release_types["primary"], limit=PAGE_SIZE, offset=offset
        )

        for release_group in release_group_set.get("release-group-list", []):
            all_release_groups.append(release_group)

        count = release_group_set.get("release-group-count")
        this_page_size = len(release_group_set.get("release-group-list", []))
        print(f"Fetched {this_page_size} release groups on page {page} out of {count//PAGE_SIZE + 1}")
        page += 1
        offset += len(release_group_set.get("release-group-list", []))

    return all_release_groups
