using System.Text.Json.Serialization;

namespace UnoTrip.Application.Trip.Common;

public record LocationResult(
    string Name,
    [property: JsonPropertyName("lat")] float Latitude,
    [property: JsonPropertyName("lng")] float Longitude);