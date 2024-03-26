from typing import Union

import httpx

from services.common import BaseService

import wikipediaapi


class PlacesService:
    def __init__(self,
                 token: str,
                 address: str = 'https://api.foursquare.com/v3/places/search'):
        self.address = address
        self.params = {
            "Accept": "application/json",
            "Authorization": token
        }
        self.wiki = wikipediaapi.Wikipedia('UnoTrip', 'ru')

    async def get_sights(self, longitude: float, latitude: float, categories: list, custom_params: str = ''):
        async with httpx.AsyncClient() as client:
            client.headers.update(self.params)
            response = await client.get(f'{self.address}'
                                        f'?ll={latitude},{longitude}'
                                        f'&radius=5000'
                                        f'&categories={",".join(map(str, categories))}'
                                        f'&sort=RELEVANCE'
                                        f'&limit=5'
                                        f'{custom_params}')

            return response.json()

    async def register(self,
                       user_id: int,
                       description: str,
                       city: str,
                       age: int):
        data = {
            'telegramId': user_id,
            'description': description,
            'city': city,
            'age': age
        }

        async with httpx.AsyncClient() as client:
            await client.post(self.address, json=data)

    async def update(self,
                     user_id: int,
                     args: dict):
        data = {
            'telegramId': user_id,
            **args
        }

        async with httpx.AsyncClient() as client:
            await client.patch(self.address, json=data)

    def get_wiki_article(self, location_name: str) -> Union[None, tuple[str, str]]:
        city = location_name.split(',')[0]
        page = self.wiki.page(city)

        if not page.exists():
            return None

        return page.summary, page.fullurl
