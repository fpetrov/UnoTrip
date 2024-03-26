using ErrorOr;
using Mediator;
using UnoTrip.Application.Common.Interfaces.Persistence;
using UnoTrip.Application.Common.Mappings;
using UnoTrip.Application.Trip.Common;
using UnoTrip.Domain.Common.Errors;

namespace UnoTrip.Application.Trip.Queries;

public class GetLocationQueryHandler(
    ILocationRepository locationRepository)
    : IRequestHandler<GetLocationQuery, ErrorOr<LocationResult>>
{
    public async ValueTask<ErrorOr<LocationResult>> Handle(
        GetLocationQuery request,
        CancellationToken cancellationToken)
    {
        var location = await locationRepository
            .Get(request.Id, cancellationToken);
        
        if (location is null)
            return Errors.Trip.NotFound();
        
        return LocationMapper.Map(location);
    }
}

public record GetLocationQuery(int Id)
    : IRequest<ErrorOr<LocationResult>>;