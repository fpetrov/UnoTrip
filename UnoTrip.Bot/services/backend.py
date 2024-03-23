from services.common import BaseService

from services.backend_internals import user_internal, trip_internal


class BackendService(BaseService):
    def __init__(self, address: str):
        super().__init__(address)

        # Дополнительные сервисы, которые находятся внутри бекенда
        self.user_service = user_internal.UserService(self.address)
        self.trip_service = trip_internal.TripService(self.address)
