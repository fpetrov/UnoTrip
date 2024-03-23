using ErrorOr;
using Mediator;
using UnoTrip.Application.Common.Interfaces.Persistence;
using UnoTrip.Application.Common.Mappings;
using UnoTrip.Application.Trip.Common;
using UnoTrip.Domain.Common.Errors;

namespace UnoTrip.Application.Trip.Queries;

public class GetTripByIdHandler(
    ITripRepository tripRepository) : IRequestHandler<GetTripById, ErrorOr<TripResult>>
{
    public async ValueTask<ErrorOr<TripResult>> Handle(GetTripById request, CancellationToken cancellationToken)
    {
        var existingTrip = await tripRepository
            .Get(request.Uuid, cancellationToken);
        
        if (existingTrip is null)
            return Errors.Trip.NotFound();

        var result = TripMapper.Map(existingTrip);

        return result;
    }
}

public record GetTripById(Guid Uuid)
    : IRequest<ErrorOr<TripResult>>;