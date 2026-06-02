from shapely.geometry import Point

from zones import (
    CAM1_SKINCARE_ZONE,
    CAM2_MAKEUP_ZONE
)


def get_zone(
        camera_id,
        center_x,
        center_y
):

    point = Point(
        center_x,
        center_y
    )

    if (
        camera_id == "CAM1"
        and
        CAM1_SKINCARE_ZONE.contains(
            point
        )
    ):

        return "SKINCARE"

    if (
        camera_id == "CAM2"
        and
        CAM2_MAKEUP_ZONE.contains(
            point
        )
    ):

        return "MAKEUP"

    return None