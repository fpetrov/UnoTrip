from dataclasses import dataclass, field

@dataclass
class Destination:
    name: str
    lat: float
    lng: float

@dataclass
class DestinationRequest:
    origin: str
    destinations: list[Destination] = field(default_factory=list)