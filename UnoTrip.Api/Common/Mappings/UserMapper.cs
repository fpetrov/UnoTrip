using Riok.Mapperly.Abstractions;
using UnoTrip.Application.User.Commands;
using UnoTrip.Application.User.Common;
using UnoTrip.Application.User.Queries;
using UnoTrip.Contracts.User;

namespace UnoTrip.Api.Common.Mappings;

[Mapper]
public static partial class UserMapper
{
    public static partial CreateUserCommand Map(CreateUserRequest request);
    public static partial UpdateUserCommand Map(UpdateUserRequest request);
    public static partial UserResponse Map(UserResult command);
}