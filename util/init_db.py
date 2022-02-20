#!/usr/bin/env python

import os
import sys

sys.path.append(os.path.join(sys.path[0], ".."))

from web import db  # noqa: E402
from web.models import Group, ReleaseGroup, ReleaseGroupType  # noqa: E402

db.drop_all()
db.create_all()

# Add groups
db.session.add(Group(id="feb5ba97-6862-4864-a44b-321ab06d41b2", name="Mojiganga"))

# Add release types
release_types_to_track = ["album", "ep", "compilation", "soundtrack", "live"]
PRIMARY_RELEASE_TYPES = ["album", "single", "ep", "broadcast", "other"]
SECONDARY_RELEASE_TYPES = [
    "compilation",
    "soundtrack",
    "spokenword",
    "interview",
    "audiobook",
    "audio drama",
    "live",
    "remix",
    "dj-mix",
    "mixtape/street",
]
for release_type in PRIMARY_RELEASE_TYPES + SECONDARY_RELEASE_TYPES:
    track = release_type in release_types_to_track
    primary = release_type in PRIMARY_RELEASE_TYPES
    db.session.add(ReleaseGroupType(name=release_type, primary=primary, track=track))

db.session.commit()
