import httpx

from services.common import BaseService
from typing import Union, NamedTuple


class Location(NamedTuple):
    address: str
    lat: float
    lon: float


class OpenStreetMapService(BaseService):
    def __init__(self, address: str):
        super().__init__(address)

    async def take_screenshot(self, user_id: int, route_id: int):
        # TODO: Реализовать вызов из бекенда
        # а затем уже вызов скриншота из OpenStreetMap,
        # чтобы не тратить лишние ресурсы
        route = await self.get_route(route_id)
        pass

    async def get_route(self, route_id: int):
        # TODO: Реализовать вызов из бекенда
        pass

    async def get_route_information(self, query: str) -> Union[Location, None]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.address}/route/{query}')

            if response.status_code != 200:
                return None

            json = response.json()

            location = Location(
                address=json['address'],
                lat=json['lat'],
                lon=json['lng']
            )

            return location
