from dataclasses import dataclass, field


@dataclass
class ForecastWeatherResponse:
    date: str
    morning: int
    day: int
    evening: int
    night: int
    wind_speed: list[int] = field(default_factory=list)
    weather_type: list[int] = field(default_factory=list)
