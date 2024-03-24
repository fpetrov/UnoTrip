using ErrorOr;
using Mediator;
using UnoTrip.Application.Common.Interfaces.Persistence;
using UnoTrip.Application.Common.Mappings;
using UnoTrip.Application.Trip.Common;
using UnoTrip.Domain.Common.Errors;
using UnoTrip.Domain.Entities;

namespace UnoTrip.Application.Trip.Queries;

public class GetMyTripNotesQueryHandler(
    IUserRepository userRepository,
    ITripRepository tripRepository)
    : IRequestHandler<GetMyTripNotesQuery, ErrorOr<List<NoteResult>>>
{
    public async ValueTask<ErrorOr<List<NoteResult>>> Handle(
        GetMyTripNotesQuery request,
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

        // Находим все публичные заметки
        var uniqueNotes = trip
            .Notes
            .Where(note => !note.IsPrivate)
            .ToHashSet();
        
        // Находим все заметки, принадлежащие пользователю
        var userNotes = trip.Notes
            .Where(note => note.Author.TelegramId == existingUser.TelegramId)
            .ToList();

        // Исключаем повторяющиеся
        uniqueNotes.UnionWith(userNotes);
        
        return uniqueNotes
            .ToList()
            .ConvertAll(NoteMapper.Map);
    }
}

public record GetMyTripNotesQuery(
    long TelegramId,
    Guid TripId) : IRequest<ErrorOr<List<NoteResult>>>;