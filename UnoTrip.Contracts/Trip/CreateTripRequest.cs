using UnoTrip.Domain.Entities;

namespace UnoTrip.Contracts.Trip;

public record CreateTripRequest(
    long TelegramId,
    string Name,
    string Description,
    List<Location>? Locations);