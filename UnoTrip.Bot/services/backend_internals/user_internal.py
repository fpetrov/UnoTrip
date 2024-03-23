import httpx

from services.common import BaseService


class UserService(BaseService):
    def __init__(self, address: str):
        super().__init__(f'{address}/user')

    async def get(self, user_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.address}/{user_id}')

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
