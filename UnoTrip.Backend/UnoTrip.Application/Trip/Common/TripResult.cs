using UnoTrip.Domain.Entities;

namespace UnoTrip.Application.Trip.Common;

public record TripResult(
    Guid Uuid,
    string Name,
    string Description,
    List<Note> Notes,
    List<long> SubscribersIds,
    List<Location> Locations);