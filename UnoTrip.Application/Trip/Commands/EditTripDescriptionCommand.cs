using ErrorOr;
using Mediator;
using UnoTrip.Application.Common.Interfaces.Persistence;
using UnoTrip.Domain.Common.Errors;

namespace UnoTrip.Application.Trip.Commands;

public class EditTripDescriptionCommandHandler(
    ITripRepository tripRepository) : IRequestHandler<EditTripDescriptionCommand, ErrorOr<bool>>
{
    public async ValueTask<ErrorOr<bool>> Handle(
        EditTripDescriptionCommand request,
        CancellationToken cancellationToken)
    {
        var existingTrip = await tripRepository
            .Get(request.Uuid, cancellationToken);
        
        if (existingTrip is null)
            return Errors.Trip.NotFound();
        
        existingTrip.Description = request.Description;
        
        await tripRepository
            .Update(existingTrip, cancellationToken);
        
        return true;
    }
}

public record EditTripDescriptionCommand(
    Guid Uuid,
    string Description) : IRequest<ErrorOr<bool>>;