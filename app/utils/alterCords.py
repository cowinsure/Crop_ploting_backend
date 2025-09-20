from app.schemas.plot_schema import LatLon

def convertCord(coords: list[LatLon]):
    return [(point.longitude, point.latitude) for point in coords]