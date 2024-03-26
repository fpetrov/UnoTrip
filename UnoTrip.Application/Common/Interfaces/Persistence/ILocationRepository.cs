using UnoTrip.Domain.Entities;

namespace UnoTrip.Application.Common.Interfaces.Persistence;

public interface ILocationRepository
{
    public ValueTask<Location?> Get(int id,
        CancellationToken cancellationToken = default);
}