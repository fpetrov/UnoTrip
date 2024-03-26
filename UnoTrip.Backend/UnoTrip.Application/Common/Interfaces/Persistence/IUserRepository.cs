using System.Linq.Expressions;

namespace UnoTrip.Application.Common.Interfaces.Persistence;

public interface IUserRepository
{
    public Task Create(
        Domain.Entities.User user,
        CancellationToken cancellationToken = default);
    
    public Task<Domain.Entities.User?> Get(
        long telegramId,
        CancellationToken cancellationToken = default);
    
    public Task Update(
        Domain.Entities.User user,
        CancellationToken cancellationToken = default);
    
    public IQueryable<Domain.Entities.User> QueryBy(
        Expression<Func<Domain.Entities.User, bool>> predicate);
}