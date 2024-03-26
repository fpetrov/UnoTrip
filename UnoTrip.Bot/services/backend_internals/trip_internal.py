from typing import Union

import httpx

from services.common import BaseService


class TripService(BaseService):
    def __init__(self, address: str):
        super().__init__(f'{address}/trip')

    async def get(self, trip_id: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.address}/{trip_id}')

            return response.json()

    async def create(self,
                     user_id: int,
                     name: str,
                     description: str) -> Union[bool, dict]:
        data = {
            'telegramId': user_id,
            'name': name,
            'description': description
        }

        async with httpx.AsyncClient() as client:
            result = await client.post(self.address, json=data)

            if result.status_code == 200:
                return result.json()

            return False

    async def get_my(self, user_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.address}/my/{user_id}')

            return response.json()

    async def get_route(self, user_id: int, trip_id: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.address}/{trip_id}/route?for={user_id}')

            return response.json()

    async def delete(self, trip_id: str):
        async with httpx.AsyncClient() as client:
            await client.delete(f'{self.address}/{trip_id}')

    # Edit
    async def change_description(self,
                                 trip_id: str,
                                 description: str):
        data = {
            'description': description
        }

        async with httpx.AsyncClient() as client:
            await client.patch(f'{self.address}/{trip_id}/description', json=data)

    async def change_name(self,
                          trip_id: str,
                          name: str):
        data = {
            'name': name
        }

        async with httpx.AsyncClient() as client:
            await client.patch(f'{self.address}/{trip_id}/name', json=data)

    async def add_location(self,
                           trip_id: str,
                           location: dict):
        async with httpx.AsyncClient() as client:
            await client.post(f'{self.address}/{trip_id}/location', json=location)

    async def add_note(self,
                       trip_id: str,
                       data: dict):
        async with httpx.AsyncClient() as client:
            await client.post(f'{self.address}/{trip_id}/note', json=data)

    async def get_my_notes(self,
                           user_id: int,
                           trip_id: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.address}/my/{user_id}/notes?trip_id={trip_id}')

            return response.json()

    async def delete_location(self,
                              trip_id: str,
                              location_id: int):
        async with httpx.AsyncClient() as client:
            await client.delete(f'{self.address}/{trip_id}/location/{location_id}')

    async def add_companion(self,
                            trip_id: str,
                            companion_id: int):
        data = {
            'telegramId': companion_id
        }

        async with httpx.AsyncClient() as client:
            result = await client.post(f'{self.address}/{trip_id}/subscribe', json=data)

            return result.json()

    async def get_location(self,
                           location_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.address}/location/{location_id}')

            return response.json()
