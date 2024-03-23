using System.Linq.Expressions;

namespace UnoTrip.Application.Common.Interfaces.Persistence;

public interface ITripRepository
{
    public Task Create(
        Domain.Entities.Trip trip,
        CancellationToken cancellationToken = default);
    
    public Task<Domain.Entities.Trip?> Get(
        Guid uuid,
        CancellationToken cancellationToken = default);
    
    public Task Update(
        Domain.Entities.Trip trip,
        CancellationToken cancellationToken = default);
    
    public Task Delete(
        Domain.Entities.Trip trip,
        CancellationToken cancellationToken = default);
    
    public IQueryable<Domain.Entities.Trip> QueryBy(
        Expression<Func<Domain.Entities.Trip, bool>> predicate);
}