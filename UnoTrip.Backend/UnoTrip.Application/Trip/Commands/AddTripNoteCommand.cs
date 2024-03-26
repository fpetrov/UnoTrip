using ErrorOr;
using Mediator;
using UnoTrip.Application.Common.Interfaces.Persistence;
using UnoTrip.Domain.Common.Errors;
using UnoTrip.Domain.Entities;

namespace UnoTrip.Application.Trip.Commands;

public class AddTripNoteCommandHandler(
    ITripRepository tripRepository,
    IUserRepository userRepository)
    : IRequestHandler<AddTripNoteCommand, ErrorOr<bool>>
{
    public async ValueTask<ErrorOr<bool>> Handle(
        AddTripNoteCommand request,
        CancellationToken cancellationToken)
    {
        var existingUser = await userRepository
            .Get(request.TelegramId, cancellationToken);
        
        if (existingUser is null)
            return Errors.User.NotFound();
        
        var trip = await tripRepository
            .Get(request.TripId, cancellationToken);
        
        if (trip is null)
            return Errors.Trip.NotFound();
        
        var newNote = new Note
        {
            Name = request.Name,
            Author = existingUser,
            FileId = request.FileId,
            ContentType = request.ContentType,
            IsPrivate = request.IsPrivate
        };
        
        trip.Notes.Add(newNote);
        
        await tripRepository
            .Update(trip, cancellationToken);
        
        return true;
    }
}

public record AddTripNoteCommand(
    long TelegramId,
    Guid TripId,
    string Name,
    string ContentType,
    string FileId,
    bool IsPrivate) : IRequest<ErrorOr<bool>>;