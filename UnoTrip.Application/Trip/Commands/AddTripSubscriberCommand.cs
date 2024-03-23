using ErrorOr;
using Mediator;
using UnoTrip.Application.Common.Interfaces.Persistence;
using UnoTrip.Domain.Common.Errors;
using UnoTrip.Domain.Entities;

namespace UnoTrip.Application.Trip.Commands;

public class AddTripSubscriberCommandHandler(
    ITripRepository tripRepository,
    IUserRepository userRepository) : IRequestHandler<AddTripSubscriberCommand, ErrorOr<List<long>>>
{
    public async ValueTask<ErrorOr<List<long>>> Handle(
        AddTripSubscriberCommand request,
        CancellationToken cancellationToken)
    {
        var existingTrip = await tripRepository
            .Get(request.Uuid, cancellationToken);
        
        if (existingTrip is null)
            return Errors.Trip.NotFound();
        
        var existingUser = await userRepository
            .Get(request.TelegramId, cancellationToken);
        
        if (existingUser is null)
            return Errors.User.NotFound();
        
        var notificationSubscribers = existingTrip
            .Subscribers
            .ConvertAll(u => u.TelegramId);
        
        if (notificationSubscribers.Contains(request.TelegramId))
            return Array.Empty<long>().ToList();
        
        existingTrip.Subscribers.Add(existingUser);
        
        await tripRepository
            .Update(existingTrip, cancellationToken);
        
        return notificationSubscribers;
    }
}

/// <summary>
/// Add subscriber to trip
/// </summary>
/// <param name="Uuid">Trip unique identifier</param>
/// <param name="TelegramId">Subscriber unique identifier</param>
/// <returns>List of subscribers that needs to be notified</returns>
public record AddTripSubscriberCommand(
    Guid Uuid,
    long TelegramId) : IRequest<ErrorOr<List<long>>>;