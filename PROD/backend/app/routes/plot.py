from fastapi import APIRouter, HTTPException, Query, Response
from fastapi.responses import JSONResponse
from app.services.plot_service import PlotService
from io import BytesIO

router = APIRouter()

# Path to the lunar albedo map and XRF data
albedo_map_path = 'lunar_albedo_map.tif'
xrf_data_path = 'output.csv'

# Initialize PlotService
plot_service = PlotService(albedo_map_path, xrf_data_path)

@router.get("/plot")
async def get_plot(max_val: int = Query(..., gt=0)):
    """
    Fetch the generated plot based on the max_val provided.
    The plot is returned as a PNG image.
    """
    try:
        # Generate plot using the PlotService
        buf = plot_service.generate_plot(max_val)
        
        # Ensure buf is reset to the start before reading if it's a BytesIO object
        buf.seek(0)
        
        # Return the plot image as a response
        return Response(content=buf.read(), media_type="image/png")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Data files not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


