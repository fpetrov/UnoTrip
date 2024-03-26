namespace UnoTrip.Contracts.Trip.Add;

public record AddTripNoteRequest(
    long TelegramId,
    string Name,
    string FileId,
    string ContentType,
    bool IsPrivate);