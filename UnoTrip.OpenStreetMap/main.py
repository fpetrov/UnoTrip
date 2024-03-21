import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, Response

from geopy.geocoders import Nominatim

from entities.DestinationRequest import DestinationRequest
from providers.OpenStreetMapProvider import OpenStreetMapProvider

app = FastAPI()
geolocator = Nominatim(user_agent="UnoTrip")

GRAPHHOPPER_TOKEN = 'ed83a659-67df-473e-aa47-7bfb2a4907dd'

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

provider = OpenStreetMapProvider(GRAPHHOPPER_TOKEN)

@app.get("/route/{route_address}")
async def get_route(route_address: str):
    location = geolocator.geocode(route_address)

    if not location:
        return HTTPException(status_code=404, detail="Location not found")

    return JSONResponse({
        "address": location.address,
        "lat": location.latitude,
        "lng": location.longitude
    })


@app.post("/route/screenshot")
async def get_route_screenshot(destination_request: DestinationRequest):
    plot = provider.draw_plot(destination_request.destinations)
    image_content = provider.take_screenshot(plot)

    return Response(content=image_content, media_type="image/png")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    provider.__del__()