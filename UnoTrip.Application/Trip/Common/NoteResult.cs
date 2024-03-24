namespace UnoTrip.Application.Trip.Common;

public record NoteResult(
    int Id,
    string Name,
    string FileId,
    string ContentType,
    bool IsPrivate);