using UnoTrip.Application.Common.Interfaces.Persistence;
using UnoTrip.Domain.Entities;

namespace UnoTrip.Infrastructure.Persistence;

public class LocationRepository(
    ApplicationContext context)
    : ILocationRepository
{
    public ValueTask<Location?> Get(int id, CancellationToken cancellationToken = default)
    {
        return context
            .Set<Location>()
            .FindAsync(
                cancellationToken: cancellationToken,
                keyValues: [id]);
    }
}