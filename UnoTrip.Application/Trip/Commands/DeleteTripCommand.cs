using ErrorOr;
using Mediator;
using UnoTrip.Application.Common.Interfaces.Persistence;
using UnoTrip.Domain.Common.Errors;

namespace UnoTrip.Application.Trip.Commands;

public class DeleteTripCommandHandler(
    ITripRepository tripRepository)
    : IRequestHandler<DeleteTripCommand, ErrorOr<List<long>>>
{
    public async ValueTask<ErrorOr<List<long>>> Handle(
        DeleteTripCommand request,
        CancellationToken cancellationToken)
    {
        var existingTrip = await tripRepository
            .Get(request.Uuid, cancellationToken);
        
        if (existingTrip is null)
            return Errors.Trip.NotFound();
        
        var notificationSubscribers = existingTrip
            .Subscribers
            .ConvertAll(u => u.TelegramId);
        
        await tripRepository
            .Delete(existingTrip, cancellationToken);
        
        return notificationSubscribers;
    }
}

public record DeleteTripCommand(Guid Uuid)
    : IRequest<ErrorOr<List<long>>>;