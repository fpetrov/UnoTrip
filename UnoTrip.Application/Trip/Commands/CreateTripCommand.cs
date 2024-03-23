using ErrorOr;
using Mediator;
using Microsoft.EntityFrameworkCore;
using UnoTrip.Application.Common.Interfaces.Persistence;
using UnoTrip.Application.Common.Mappings;
using UnoTrip.Application.Trip.Common;
using UnoTrip.Domain.Common.Errors;
using UnoTrip.Domain.Entities;

namespace UnoTrip.Application.Trip.Commands;

public class CreateTripCommandHandler(
    ITripRepository tripRepository,
    IUserRepository userRepository)
    : IRequestHandler<CreateTripCommand, ErrorOr<TripResult>>
{
    public async ValueTask<ErrorOr<TripResult>> Handle(
        CreateTripCommand request,
        CancellationToken cancellationToken)
    {
        var existingUser = await userRepository
            .Get(request.TelegramId, cancellationToken);
        
        if (existingUser is null)
            return Errors.User.NotFound();

        var existingTrip = await tripRepository
            .QueryBy(t => t.Name == request.Name)
            .FirstOrDefaultAsync(cancellationToken: cancellationToken);
        
        if (existingTrip is not null)
            return Errors.Trip.AlreadyExists();
        
        var newTrip = new Domain.Entities.Trip
        {
            Uuid = Guid.NewGuid(),
            Name = request.Name,
            Description = request.Description,
            Subscribers = [existingUser]
        };

        if (request.Locations is not null)
            newTrip.Locations = request.Locations;
        
        existingUser
            .Trips
            .Add(newTrip);
        
        await tripRepository
            .Create(newTrip, cancellationToken);
        
        await userRepository
            .Update(existingUser, cancellationToken);
        
        return TripMapper.Map(newTrip);
    }
}

public record CreateTripCommand(
    long TelegramId,
    string Name,
    string Description,
    List<Location>? Locations) : IRequest<ErrorOr<TripResult>>;