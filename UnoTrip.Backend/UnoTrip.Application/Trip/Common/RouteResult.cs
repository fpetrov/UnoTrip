namespace UnoTrip.Application.Trip.Common;

/// <summary>
/// Route result of trip
/// </summary>
/// <param name="Origin">Origin city of user</param>
/// <param name="Destinations">All destination points of trip</param>
public record RouteResult(
    string Origin,
    List<LocationResult> Destinations);