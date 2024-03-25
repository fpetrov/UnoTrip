from dataclasses import dataclass

from app.entities.requests.DestinationRequest import Destination


@dataclass
class WeatherForecastRequest:
    date: str
    destination: Destination
    forecast_days: int = 16