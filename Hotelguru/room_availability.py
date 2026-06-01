from flask import current_app


def is_room_bookable(room):
    if room.status is None:
        return True
    blocked = current_app.config.get(
        "UNAVAILABLE_ROOM_STATUS_NAMES",
        ["Karbantartás", "Karbantartás alatt", "Nem elérhető"],
    )
    name = room.status.name.lower()
    for blocked_name in blocked:
        if blocked_name.lower() in name:
            return False
    return True
