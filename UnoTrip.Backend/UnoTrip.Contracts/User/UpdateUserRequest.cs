namespace UnoTrip.Contracts.User;

public record UpdateUserRequest(
    long TelegramId,
    string? Description,
    string? City,
    int? Age);