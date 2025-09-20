import io
import base64
import random
from pyproj import Geod
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, box


def GeneratePlot(lonlatCoord: list[tuple[float, float]], 
                 buffer_zone: int=7, 
                 plot_size:int=5, 
                 fig_size:tuple=(17, 17), 
                 minimum_area: float= 400):
    try:
        # Creating Polygons
        poly = Polygon(lonlatCoord)
        shrunk_poly = poly.buffer(-buffer_zone / 111000.0)
        geod = Geod(ellps="WGS84")
        lon, lat = zip(*lonlatCoord)
        area, _ = geod.polygon_area_perimeter(lon, lat)
        area_sq_meters = abs(area)
        min_x, min_y, max_x, max_y = shrunk_poly.bounds
        square_size_deg = plot_size / 111000.0
        
        # Finding all valid boxes
        squares_inside = []
        x = min_x
        while x + square_size_deg <= max_x:
            y = min_y
            while y + square_size_deg <= max_y:
                sq = box(x, y, x + square_size_deg, y + square_size_deg)
                if shrunk_poly.contains(sq):
                    squares_inside.append(sq)
                y += square_size_deg
            x += square_size_deg

        # random box selection
        selected_plot = random.choice(squares_inside) if squares_inside else None
        
        # figure plotting
        plt.figure(figsize=fig_size)
        x_poly, y_poly = shrunk_poly.exterior.xy
        x1_poly, y1_poly = poly.exterior.xy
        plt.fill(x_poly, y_poly, alpha=0.3, edgecolor='blue', facecolor='lightblue', linewidth=2)
        plt.fill(x1_poly, y1_poly, alpha=0.3, edgecolor='green', facecolor='#FFFDD0', linewidth=2)

        for sq in squares_inside:
            x_sq, y_sq = sq.exterior.xy
            if sq == selected_plot:
                plt.fill(x_sq, y_sq, color='green', alpha=0.6)
                selected_coords_lonlat = [(y, x) for x, y in selected_plot.exterior.coords[:-1]]
            else:
                plt.plot(x_sq, y_sq, color='red')
        plt.axis('equal')

        # converting to base64 image
        buf = io.BytesIO()
        plt.savefig(buf, format="jpg")
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode("utf-8")
        buf.close()
        plt.close()

        response = {
        "status": "success" if (selected_plot and area_sq_meters >= minimum_area)  else "failed",
        "area": area_sq_meters,
        "message": "2D Land map generation succesful" if (selected_plot and area_sq_meters >= minimum_area)  else f"Can not select a land plot. Minimum area required is {minimum_area} square meter (m²)",
        "data": {
            "image": f"data:image/jpg;base64,{image_base64}",
            "plot_coordinates": [
                {"latitude": lat, "longitude": lon}
                for lat, lon in selected_coords_lonlat
            ] if selected_plot else [],
            "land_area": [
                {"latitude": lat, "longitude": lon}
                for lon, lat in lonlatCoord
                ]
            }
        }


    except Exception as e:
        response = {
        "status": "failed",
        "area": None,
        "message": f"Error Occurred {str(e)}",
        "data": {
            "image": None,
            "plot_coordinates": None,
            "land_area": None
            }
        }
    finally:
        status_code = 200 if response['status'] == 'success' else 400
        return response, status_code


if __name__ == "__main__":
    coords_latlon = [
    (23.79724348906552, 90.38212145072005),
    (23.796810560401855, 90.38233266944614),
    (23.796722210134078, 90.38228975410415),
    (23.79643261716849, 90.38240240688384),
    (23.796430162988063, 90.38239436025671),
    (23.796155294486255, 90.38246677990082),
    (23.796155294486255, 90.38219587678772),
    (23.79617001959931, 90.38200007552778),
    (23.796216649112964, 90.38194106692889),
    (23.7964399797095, 90.38175063008701),
    (23.796557780309087, 90.38159237975363),
    (23.796781110319273, 90.38146631592872),
    (23.79692590649438, 90.38146899813776),
    (23.797009348284693, 90.3816433417254),
    (23.79712224003337, 90.38181500310398),
    (23.79724348906552, 90.38212145072005)
]

    # Here I interchange the latlon to lonlat as Polygon class requires (lon, lat) system inputs
    coords = [(lon, lat) for lat, lon in coords_latlon]

    import time

    st = time.time()
    resp = GeneratePlot(coords)
    end = time.time()

    print(f'Time to respond: {end - st}s')

    

