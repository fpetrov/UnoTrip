namespace UnoTrip.Application.User.Common;

public record UserResult(
    long TelegramId,
    string Description,
    string City,
    int Age);