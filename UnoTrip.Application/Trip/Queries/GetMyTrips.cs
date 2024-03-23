using ErrorOr;
using Mediator;
using UnoTrip.Application.Common.Interfaces.Persistence;
using UnoTrip.Application.Common.Mappings;
using UnoTrip.Application.Trip.Common;
using UnoTrip.Domain.Common.Errors;

namespace UnoTrip.Application.Trip.Queries;

public class GetMyTripsHandler(
    IUserRepository userRepository)
    : IRequestHandler<GetMyTrips, ErrorOr<List<TripResult>>>
{
    public async ValueTask<ErrorOr<List<TripResult>>> Handle(
        GetMyTrips request,
        CancellationToken cancellationToken)
    {
        var user = await userRepository
            .Get(request.TelegramId, cancellationToken);
        
        if (user is null)
            return Errors.User.NotFound();
        
        return user
            .Trips
            .ConvertAll(TripMapper.Map);
    }
}

public record GetMyTrips(long TelegramId)
    : IRequest<ErrorOr<List<TripResult>>>;