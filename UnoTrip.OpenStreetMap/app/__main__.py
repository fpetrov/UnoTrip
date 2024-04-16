import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, Response

from geopy.geocoders import Nominatim

from entities.requests.DestinationRequest import DestinationRequest, Destination
from entities.requests.PromptRequest import PromptRequest
from entities.requests.WeatherForecastRequest import WeatherForecastRequest
from providers.GptBotProvider import GptBotProvider
from providers.WeatherForecastProvider import WeatherForecastProvider
from providers.OpenStreetMapProvider import OpenStreetMapProvider

app = FastAPI()
geolocator = Nominatim(user_agent="UnoTrip")

GRAPHHOPPER_TOKEN = 'ed83a659-67df-473e-aa47-7bfb2a4907dd'
# GPT_TOKEN = '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'
GPT_TOKEN = 'pk-jbBBdlromcXaXHtAyJmIWdEbVOIyTXsehFZMLnBLFXJSEwVF'

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

route_provider = OpenStreetMapProvider(GRAPHHOPPER_TOKEN)
weather_provider = WeatherForecastProvider()
gpt_provider = GptBotProvider(provider_token=GPT_TOKEN)


@app.get("/route/{route_address}")
async def get_route(route_address: str):
    location = geolocator.geocode(route_address)

    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    return JSONResponse({
        "address": location.address,
        "lat": location.latitude,
        "lng": location.longitude
    })


@app.post("/route/screenshot")
async def get_route_screenshot(destination_request: DestinationRequest):
    origin_location = geolocator.geocode(destination_request.origin)
    origin_destination = Destination(
        name='Ты',
        lat=origin_location.latitude,
        lng=origin_location.longitude
    )

    destination_request.destinations.insert(0, origin_destination)
    plot = route_provider.draw_plot(destination_request.destinations)
    image_content = route_provider.take_screenshot(plot)

    return Response(content=image_content, media_type="image/png")


@app.post("/weather")
async def get_weather_forecast(
        weather_request: WeatherForecastRequest):
    forecast = weather_provider.get_weather_forecast(weather_request)

    return forecast

@app.post("/ask")
async def ask_prompt(
        prompt_request: PromptRequest):
    response = await gpt_provider.ask_question(prompt_request)

    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    route_provider.__del__()