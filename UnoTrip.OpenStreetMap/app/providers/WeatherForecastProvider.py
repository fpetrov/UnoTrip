import datetime

import openmeteo_requests

import requests_cache
import pandas as pd
from openmeteo_sdk.WeatherApiResponse import WeatherApiResponse
from retry_requests import retry

from entities.requests.WeatherForecastRequest import WeatherForecastRequest
from entities.responses.CurrentWeatherResponse import CurrentWeatherResponse
from entities.responses.ForecastWeatherResponse import ForecastWeatherResponse


class WeatherForecastProvider:
    DEFAULT_REQUEST_PARAMS = {
        #"latitude": 55.731876,
        #"longitude": 37.607434,
        "current": ["temperature_2m", "apparent_temperature", "wind_speed_10m"],
        "hourly": ["temperature_2m", "weather_code", "wind_speed_10m"],
        "timezone": "GMT"
        #"forecast_days": 16
    }

    def __init__(self, address: str = 'https://api.open-meteo.com/v1/forecast'):
        self.address = address

        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)

        self.open_meteo = openmeteo_requests.Client(session=retry_session)

    def get_weather_forecast(self,
                                   request: WeatherForecastRequest):
        request_params = self.DEFAULT_REQUEST_PARAMS
        request_params["latitude"] = request.destination.lat
        request_params["longitude"] = request.destination.lng
        request_params["forecast_days"] = request.forecast_days

        responses = self.open_meteo.weather_api(url=self.address,
                                                params=request_params)

        response = responses[0]
        target_date = pd.Timestamp(request.date)
        end_date = target_date + pd.DateOffset(days=request.forecast_days)

        current_weather = self.__get_current_weather__(response)
        hourly_dataframe = self.__prepare_hourly_forecast__(response)

        forecast = []

        current_date = target_date
        while current_date < end_date:
            weather_info = self.__get_date_weather_forecast__(hourly_dataframe,
                                                              current_date)
            forecast.append(weather_info)

            current_date += pd.DateOffset(days=1)

        weather_response = {
            "current_weather": current_weather,
            "weather_forecast": forecast
        }

        return weather_response

    def __get_current_weather__(self, response: WeatherApiResponse) -> CurrentWeatherResponse:
        current = response.Current()
        current_temperature_2m = current.Variables(0).Value()
        current_apparent_temperature = current.Variables(1).Value()
        current_wind_speed_10m = current.Variables(2).Value()

        current_weather = CurrentWeatherResponse(
            temperature=round(current_temperature_2m),
            apparent_temperature=round(current_apparent_temperature),
            wind_speed=round(current_wind_speed_10m)
        )

        return current_weather

    def __get_date_weather_forecast__(self,
                             hourly_dataframe: pd.DataFrame,
                             target_date: pd.Timestamp) -> ForecastWeatherResponse:
        target_forecast = hourly_dataframe[hourly_dataframe['date'].dt.date == target_date.date()]

        morning_forecast = target_forecast[(target_forecast['date'].dt.hour >= 6) &
                                           (target_forecast['date'].dt.hour < 12)]

        day_forecast = target_forecast[(target_forecast['date'].dt.hour >= 12) &
                                       (target_forecast['date'].dt.hour < 18)]

        evening_forecast = target_forecast[(target_forecast['date'].dt.hour >= 18) &
                                           (target_forecast['date'].dt.hour < 24)]

        night_forecast = target_forecast[(target_forecast['date'].dt.hour >= 0) &
                                         (target_forecast['date'].dt.hour < 6)]

        # Только средние температуры с округлением до целого
        morning_temp_mean = round(morning_forecast['temperature_2m'].mean())
        day_temp_mean = round(day_forecast['temperature_2m'].mean())
        evening_temp_mean = round(evening_forecast['temperature_2m'].mean())
        night_temp_mean = round(night_forecast['temperature_2m'].mean())

        # Краткая инфа о погоде
        wind_speed_forecast = [
            round(morning_forecast['wind_speed_10m'].mean()),
            round(day_forecast['wind_speed_10m'].mean()),
            round(evening_forecast['wind_speed_10m'].mean()),
            round(night_forecast['wind_speed_10m'].mean())
        ]

        weather_type_forecast = [
            int(morning_forecast['weather_code'].mode()[0]),
            int(day_forecast['weather_code'].mode()[0]),
            int(evening_forecast['weather_code'].mode()[0]),
            int(night_forecast['weather_code'].mode()[0])
        ]

        return ForecastWeatherResponse(
            date=target_date.strftime("%Y-%m-%d"),
            morning=morning_temp_mean,
            day=day_temp_mean,
            evening=evening_temp_mean,
            night=night_temp_mean,
            wind_speed=wind_speed_forecast,
            weather_type=weather_type_forecast
        )

    def __prepare_hourly_forecast__(self, response: WeatherApiResponse) -> pd.DataFrame:
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        weather_codes = hourly.Variables(1).ValuesAsNumpy()
        wind_speed_10m = hourly.Variables(2).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        ), "temperature_2m": hourly_temperature_2m,
        "weather_code": weather_codes,
        "wind_speed_10m": wind_speed_10m}

        hourly_dataframe = pd.DataFrame(data=hourly_data)

        return hourly_dataframe