using Riok.Mapperly.Abstractions;
using UnoTrip.Application.Trip.Common;

namespace UnoTrip.Application.Common.Mappings;

[Mapper]
internal static partial class TripMapper
{
    [MapProperty("Subscribers", "SubscribersIds")]
    public static partial TripResult Map(Domain.Entities.Trip trip);

    private static List<long> UsersToListId(List<Domain.Entities.User> source)
        => source.ConvertAll(u => u.TelegramId);
}