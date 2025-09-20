from pydantic import BaseModel
from typing import List

class LatLon(BaseModel):
    latitude: float
    longitude: float


class PlotRequest(BaseModel):
    land_area: List[LatLon]
    buffer_zone: int = 7
    plot_size: int = 5
