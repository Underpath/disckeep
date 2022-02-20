from flask import jsonify, request

from web import app, keep, musicbrainz


@app.route("/")
@app.route("/index")
def index():
    return "Hello, World!"


@app.route("/api/group/search", methods=["GET"])
def group_search():
    name = request.args.get("name")
    if not name:
        return (
            jsonify(error=400, success=False, text="Please provide a group name."),
            400,
        )
    return (
        jsonify(status=200, success=True, result=musicbrainz.search_group(name)),
        200,
    )


@app.route("/api/group/", methods=["PUT"])
def group_create():
    group_id = request.get_json().get("id")
    if not group_id:
        return (
            jsonify(error=400, success=False, text="Please provide a group ID."),
            400,
        )
    # if not isinstance(follow, bool):
    #     return (
    #         jsonify(error=400, success=False, text="Follow must be `true` or `false`."),
    #         400,
    #     )

    keep.create_group(group_id)

    return "200"


@app.route("/test")
def test():
    return "OK"
