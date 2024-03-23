using ErrorOr;
using Mediator;
using UnoTrip.Application.Common.Interfaces.Persistence;
using UnoTrip.Domain.Common.Errors;
using UnoTrip.Domain.Entities;

namespace UnoTrip.Application.Trip.Commands;

public class AddTripLocationCommandHandler(
    ITripRepository tripRepository) : IRequestHandler<AddTripLocationCommand, ErrorOr<bool>>
{
    public async ValueTask<ErrorOr<bool>> Handle(
        AddTripLocationCommand request,
        CancellationToken cancellationToken)
    {
        var existingTrip = await tripRepository
            .Get(request.Uuid, cancellationToken);
        
        if (existingTrip is null)
            return Errors.Trip.NotFound();
        
        existingTrip.Locations.Add(request.Location);
        
        await tripRepository
            .Update(existingTrip, cancellationToken);
        
        return true;
    }
}

public record AddTripLocationCommand(
    Guid Uuid,
    Location Location) : IRequest<ErrorOr<bool>>;