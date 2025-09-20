from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.schemas.plot_schema import PlotRequest
from app.services.plot_mechanism import GeneratePlot
from app.config import settings
from app.auth import verify_token
from app.utils.alterCords import convertCord


router = APIRouter(
    prefix="/landmap",
    tags=["LandMap"]
)

@router.post("/generate")
def gen_plot(request: PlotRequest, user=Depends(verify_token)):
    coords = convertCord(request.land_area)
    cd_resp, status_code = GeneratePlot(
        lonlatCoord=coords, 
        buffer_zone=settings.DEFAULT_BUFFER_ZONE, 
        plot_size=settings.DEFAULT_PLOT_SIZE, 
        fig_size=settings.DEFAULT_FIG_SIZE,
        minimum_area=settings.MINIMUM_LAND_AREA
    )

    return JSONResponse(cd_resp, status_code=status_code)