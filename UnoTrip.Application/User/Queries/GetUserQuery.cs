using ErrorOr;
using Mediator;
using UnoTrip.Application.Common.Interfaces.Persistence;
using UnoTrip.Application.User.Common;
using UnoTrip.Domain.Common.Errors;

namespace UnoTrip.Application.User.Queries;

public class GetUserQueryHandler(
    IUserRepository userRepository)
    : IRequestHandler<GetUserQuery, ErrorOr<UserResult>>
{
    public async ValueTask<ErrorOr<UserResult>> Handle(
        GetUserQuery request,
        CancellationToken cancellationToken)
    {
        var user = await userRepository
            .Get(request.TelegramId, cancellationToken);

        if (user is null)
            return Errors.User.NotFound();
        
        return new UserResult(user.TelegramId, user.Description, user.City, user.Country, user.Age);
    }
}

public record GetUserQuery(long TelegramId) : IRequest<ErrorOr<UserResult>>;