namespace UnoTrip.Contracts.User;

public record UserResponse(
    long TelegramId,
    string Description,
    string City,
    int Age);