using ErrorOr;
using Mediator;
using UnoTrip.Application.Common.Interfaces.Persistence;
using UnoTrip.Application.Common.Mappings;
using UnoTrip.Application.User.Common;
using UnoTrip.Domain.Common.Errors;

namespace UnoTrip.Application.User.Commands;

public class UpdateUserCommandHandler(
    IUserRepository userRepository)
    : IRequestHandler<UpdateUserCommand, ErrorOr<UserResult>>
{
    public async ValueTask<ErrorOr<UserResult>> Handle(
        UpdateUserCommand request,
        CancellationToken cancellationToken)
    {
        var existingUser = await userRepository
            .Get(request.TelegramId, cancellationToken);
        
        if (existingUser is null)
            return Errors.User.NotFound();
        
        if (request.Description is not null)
            existingUser.Description = request.Description;
        
        if (request.City is not null)
            existingUser.City = request.City;
        
        if (request.Age is not null)
            existingUser.Age = request.Age.Value;
        
        await userRepository.Update(existingUser, cancellationToken);
        
        return UserMapper.Map(existingUser);
    }
}

public record UpdateUserCommand(
    long TelegramId,
    string? Description,
    string? City,
    int? Age)
    : IRequest<ErrorOr<UserResult>>;