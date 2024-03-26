import httpx

from entities.requests.PromptRequest import PromptRequest


class GptBotProvider:
    def __init__(self, provider_token: str, address: str = 'https://api.pawan.krd/v1/chat/completions'):
        self.address = address
        self.provider_token = provider_token

    async def ask_question(self, request: PromptRequest):
        async with httpx.AsyncClient() as client:
            auth_header = {'Authorization': f'Bearer {self.provider_token}'}
            data = {
                "model": "pai-001",
                "max_tokens": 15000,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant."
                    },
                    {
                        "role": "user",
                        "content": request.question
                    }
                ]
            }

            response = await client.post(f'{self.address}', json=data, headers=auth_header, timeout=30)
            response_json = response.json()

            answer = response_json['choices'][0]['message']['content']

            return {'answer': answer}
