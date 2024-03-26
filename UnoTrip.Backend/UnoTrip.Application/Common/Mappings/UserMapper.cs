using Riok.Mapperly.Abstractions;
using UnoTrip.Application.User.Common;

namespace UnoTrip.Application.Common.Mappings;

[Mapper]
internal static partial class UserMapper
{
    public static partial UserResult Map(Domain.Entities.User user);
}