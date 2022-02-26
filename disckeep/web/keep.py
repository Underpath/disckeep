from datetime import datetime

from disckeep.web import db, musicbrainz
from disckeep.web.models import Group, ReleaseGroup, ReleaseGroupType

# TODO: Move to `const.py`
PRIMARY = "primary"
SECONDARY = "secondary"
ALBUM = "album"


def create_group(group_id):
    """
    Checks if a group with given `group_id` is already in the DB. If not, queries the external API for the group
    information and stores it in the DB, then calls another function to also add releases to the DB.
    """

    print(f'Checking whether group "{group_id}" exists in the local database.')
    exists = db.session.query(Group.query.filter(Group.id == group_id).exists()).scalar()

    if exists:
        print(f'Group "{group_id}" is already in the database.')
    else:
        print(f'Group "{group_id}" is not in the database, adding.')
        group = musicbrainz.get_group(group_id)
        db.session.add(Group(id=group_id, name=group.get("name")))
        add_tracked_release_groups_for_group(group_id)


def add_tracked_release_groups_for_group(group_id: str):
    """
    Takes the given `group_id`, then gets all release groups for that group from the external API. Then checks whether
    each release group is in the DB, if not and it is a desired release type then adds it to the DB.
    """

    all_release_groups = musicbrainz.get_release_groups_for_group(group_id)

    tracked_release_group_types = get_tracked_release_group_types()

    for release_group in all_release_groups:

        print(f'Checking whether release group "{release_group["id"]}" exists in the local database.')
        exists = db.session.query(ReleaseGroup.query.filter(ReleaseGroup.id == release_group["id"]).exists()).scalar()
        if exists:
            print(f'Ignoring release group "{release_group["title"]}" because it already exists.')
            continue

        # A release group has one primary type but can have none or multiple secondary types.
        primary_type = release_group.get("primary-type").lower()
        secondary_type = [_.lower() for _ in release_group.get("secondary-type-list", [])]

        # Ignore release groups whose primary type is not tracked.
        if primary_type not in tracked_release_group_types[PRIMARY]:
            print(f'Ignoring release group "{release_group["title"]}" due to type.')
            continue
        # Add to DB only those with no secondary type or with at least one secondary type tracked.
        elif len(secondary_type) == 0 or any(_ in secondary_type for _ in tracked_release_group_types[SECONDARY]):
            print(f'Adding release group "{release_group["title"]}" to database.')
            release_date = parse_date(release_group.get("first-release-date"))

            db.session.add(
                ReleaseGroup(
                    id=release_group["id"],
                    name=release_group["title"],
                    release_type_primary=primary_type,
                    release_types_secondary=str(secondary_type),
                    release_date=release_date,
                    group_id=group_id,
                )
            )

    print("Committing.")
    db.session.commit()


def get_tracked_release_group_types():
    """
    Returns a dictionary with both primary and secondary release group types tracked as per the DB.
    """

    primary_release_group_types = [
        _[0] for _ in db.session.query(ReleaseGroupType.name).filter_by(primary=True, track=True).all()
    ]
    secondary_release_group_types = [
        _[0] for _ in db.session.query(ReleaseGroupType.name).filter_by(primary=False, track=True).all()
    ]
    tracked_release_group_types = {PRIMARY: primary_release_group_types, SECONDARY: secondary_release_group_types}
    return tracked_release_group_types


def parse_date(date_string):
    """
    Small function to parse a string into a datetime object since it can come in multiple formats from the external API.
    """

    if not date_string:
        return None

    for date_format in ["%Y-%m-%d", "%Y-%m", "%Y"]:
        try:
            return datetime.strptime(date_string, date_format)
        except ValueError:
            pass

    print(f'Date format not understood: "{date_string}"')
