namespace UnoTrip.Contracts.Trip;

public record NoteResponse(
    int Id,
    string Name,
    string FileId,
    string ContentType,
    bool IsPrivate);