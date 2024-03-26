using Riok.Mapperly.Abstractions;
using UnoTrip.Application.Trip.Commands;
using UnoTrip.Application.Trip.Common;
using UnoTrip.Contracts.Trip;

namespace UnoTrip.Api.Common.Mappings;

[Mapper]
public static partial class TripMapper
{
    public static partial CreateTripCommand Map(CreateTripRequest request);
    
    public static partial TripResponse Map(TripResult command);
}