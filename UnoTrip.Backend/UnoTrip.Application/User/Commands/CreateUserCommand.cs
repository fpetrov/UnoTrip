using ErrorOr;
using Mediator;
using UnoTrip.Application.Common.Interfaces.Persistence;
using UnoTrip.Application.Common.Mappings;
using UnoTrip.Application.User.Common;
using UnoTrip.Domain.Common.Errors;

namespace UnoTrip.Application.User.Commands;

public class CreateUserCommandHandler(
    IUserRepository userRepository)
    : IRequestHandler<CreateUserCommand, ErrorOr<UserResult>>
{
    public async ValueTask<ErrorOr<UserResult>> Handle(
        CreateUserCommand request,
        CancellationToken cancellationToken)
    {
        var existingUser = await userRepository
            .Get(request.TelegramId, cancellationToken);
        
        if (existingUser is not null)
            return Errors.User.Duplicate();
        
        var user = new Domain.Entities.User
        {
            TelegramId = request.TelegramId,
            Description = request.Description,
            City = request.City,
            Age = request.Age
        };

        await userRepository.Create(user, cancellationToken);
        
        return UserMapper.Map(user);
    }
}

public record CreateUserCommand(
    long TelegramId,
    string Description,
    string City,
    int Age)
    : IRequest<ErrorOr<UserResult>>;