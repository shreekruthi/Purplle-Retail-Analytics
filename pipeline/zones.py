from shapely.geometry import Polygon


CAM1_SKINCARE_ZONE = Polygon([
    (0, 0),
    (1500, 0),
    (1500, 900),
    (0, 900)
])


CAM2_MAKEUP_ZONE = Polygon([
    (300, 100),
    (1700, 100),
    (1700, 900),
    (300, 900)
])


CAM3_ENTRY_ZONE = Polygon([
    (900, 50),
    (1700, 50),
    (1700, 1000),
    (900, 1000)
])


CAM5_BILLING_ZONE = Polygon([
    (0, 0),
    (900, 0),
    (900, 1080),
    (0, 1080)
])