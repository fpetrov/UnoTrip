using System.Linq.Expressions;
using Microsoft.EntityFrameworkCore;
using UnoTrip.Application.Common.Interfaces.Persistence;
using UnoTrip.Domain.Entities;

namespace UnoTrip.Infrastructure.Persistence;

public class UserRepository(
    ApplicationContext context)
    : IUserRepository
{
    public Task Create(
        User user,
        CancellationToken cancellationToken = default)
    {
        var createdEntity = context
            .Set<User>()
            .Add(user);
        
        return context
            .SaveChangesAsync(cancellationToken);
    }

    public Task<User?> Get(
        long telegramId,
        CancellationToken cancellationToken = default)
    {
        return context
            .Set<User>()
            .Where(user => user.TelegramId == telegramId)
            .Include(u => u.Trips)
                .ThenInclude(t => t.Locations)
            .Include(u => u.Trips)
                .ThenInclude(t => t.Notes)
            .Include(u => u.Trips)
            .ThenInclude(t => t.Subscribers)
            .FirstOrDefaultAsync(cancellationToken);
    }

    public Task Update(
        User user,
        CancellationToken cancellationToken = default)
    {
        context
            .Entry(user)
            .State = EntityState.Modified;
        
        return context
            .SaveChangesAsync(cancellationToken);
    }

    public IQueryable<User> QueryBy(
        Expression<Func<User, bool>> predicate)
    {
        return context
            .Set<User>()
            .Where(predicate);
    }
}