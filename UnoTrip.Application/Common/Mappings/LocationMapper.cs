using Riok.Mapperly.Abstractions;
using UnoTrip.Application.Trip.Common;
using UnoTrip.Domain.Entities;

namespace UnoTrip.Application.Common.Mappings;

[Mapper]
public static partial class LocationMapper
{
    public static partial LocationResult Map(Location location);
}