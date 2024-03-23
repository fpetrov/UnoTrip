using ErrorOr;
using Mediator;
using UnoTrip.Application.Common.Interfaces.Persistence;
using UnoTrip.Domain.Common.Errors;

namespace UnoTrip.Application.Trip.Commands;

public class EditTripNameCommandHandler(
    ITripRepository tripRepository) : IRequestHandler<EditTripNameCommand, ErrorOr<bool>>
{
    public async ValueTask<ErrorOr<bool>> Handle(
        EditTripNameCommand request,
        CancellationToken cancellationToken)
    {
        var existingTrip = await tripRepository
            .Get(request.Uuid, cancellationToken);
        
        if (existingTrip is null)
            return Errors.Trip.NotFound();
        
        existingTrip.Name = request.Name;
        
        await tripRepository
            .Update(existingTrip, cancellationToken);
        
        return true;
    }
}

public record EditTripNameCommand(
    Guid Uuid,
    string Name) : IRequest<ErrorOr<bool>>;