using ErrorOr;
using Mediator;
using UnoTrip.Application.Common.Interfaces.Persistence;
using UnoTrip.Domain.Common.Errors;
using UnoTrip.Domain.Entities;

namespace UnoTrip.Application.Trip.Commands;

public class RemoveTripLocationCommandHandler(
    ITripRepository tripRepository) : IRequestHandler<RemoveTripLocationCommand, ErrorOr<bool>>
{
    public async ValueTask<ErrorOr<bool>> Handle(
        RemoveTripLocationCommand request,
        CancellationToken cancellationToken)
    {
        var existingTrip = await tripRepository
            .Get(request.Uuid, cancellationToken);
        
        if (existingTrip is null)
            return Errors.Trip.NotFound();

        var existingLocation = existingTrip
            .Locations
            .FirstOrDefault(l => l.Id == request.LocationId);
        
        if (existingLocation is null)
            return Errors.Trip.NotFound();
        
        existingTrip.Locations.Remove(existingLocation);
        
        await tripRepository
            .Update(existingTrip, cancellationToken);
        
        return true;
    }
}

public record RemoveTripLocationCommand(
    Guid Uuid,
    int LocationId) : IRequest<ErrorOr<bool>>;