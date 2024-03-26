using ErrorOr;
using Mediator;
using UnoTrip.Application.Common.Interfaces.Persistence;
using UnoTrip.Application.Common.Mappings;
using UnoTrip.Application.Trip.Common;
using UnoTrip.Domain.Common.Errors;

namespace UnoTrip.Application.Trip.Queries;

public class GetMyTripsHandler(
    IUserRepository userRepository)
    : IRequestHandler<GetMyTripsQuery, ErrorOr<List<TripResult>>>
{
    public async ValueTask<ErrorOr<List<TripResult>>> Handle(
        GetMyTripsQuery request,
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

public record GetMyTripsQuery(long TelegramId)
    : IRequest<ErrorOr<List<TripResult>>>;