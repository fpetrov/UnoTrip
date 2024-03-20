namespace UnoTrip.Contracts.User;

public record CreateUserRequest(
    long TelegramId,
    string Description,
    string City,
    string Country,
    int Age);