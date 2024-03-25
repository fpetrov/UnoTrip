from dataclasses import dataclass


@dataclass
class CurrentWeatherResponse:
    temperature: int
    apparent_temperature: int
    wind_speed: int
