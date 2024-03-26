using ErrorOr;
using Mediator;
using UnoTrip.Application.Common.Interfaces.Persistence;
using UnoTrip.Application.Common.Mappings;
using UnoTrip.Application.Trip.Common;
using UnoTrip.Domain.Common.Errors;

namespace UnoTrip.Application.Trip.Queries;

public class GetTripRouteQueryHandler(
    ITripRepository tripRepository,
    IUserRepository userRepository)
    : IRequestHandler<GetTripRouteQuery, ErrorOr<RouteResult>>
{
    public async ValueTask<ErrorOr<RouteResult>> Handle(
        GetTripRouteQuery request,
        CancellationToken cancellationToken)
    {
        var trip = await tripRepository
            .Get(request.Uuid, cancellationToken);
        
        if (trip is null)
            return Errors.Trip.NotFound();
        
        var user = await userRepository
            .Get(request.TelegramId, cancellationToken);
        
        if (user is null)
            return Errors.User.NotFound();

        var locations = trip
            .Locations
            .ConvertAll(LocationMapper.Map);
        
        var result = new RouteResult(
            user.City,
            locations);
        
        return result;
    }
}

public record GetTripRouteQuery(Guid Uuid, long TelegramId)
    : IRequest<ErrorOr<RouteResult>>;