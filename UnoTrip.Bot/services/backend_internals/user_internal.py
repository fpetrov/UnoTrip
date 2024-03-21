import httpx


class UserService:
    def __init__(self, address: str):
        self.address = f'{address}/user'

    async def get(self, user_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.address}/{user_id}')

            return response.json()

    async def register(self,
                       user_id: int,
                       description: str,
                       city: str,
                       country: str,
                       age: int):
        data = {
            'telegramId': user_id,
            'description': description,
            'city': city,
            'country': country,
            'age': age
        }

        async with httpx.AsyncClient() as client:
            await client.post(self.address, json=data)
