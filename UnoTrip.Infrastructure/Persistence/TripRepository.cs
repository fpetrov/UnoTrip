using System.Linq.Expressions;
using Microsoft.EntityFrameworkCore;
using UnoTrip.Application.Common.Interfaces.Persistence;
using UnoTrip.Domain.Entities;

namespace UnoTrip.Infrastructure.Persistence;

public class TripRepository(
    ApplicationContext context) : ITripRepository
{
    public Task Create(Trip trip, CancellationToken cancellationToken = default)
    {
        var createdEntity = context
            .Set<Trip>()
            .Add(trip);
        
        return context
            .SaveChangesAsync(cancellationToken);
    }

    public Task<Trip?> Get(Guid uuid, CancellationToken cancellationToken = default)
    {
        return context
            .Set<Trip>()
            .Where(t => t.Uuid == uuid)
            .Include(t => t.Locations)
            .Include(t => t.Subscribers)
            .Include(t => t.Notes)
            .FirstOrDefaultAsync(cancellationToken: cancellationToken);
    }

    public Task Update(Trip trip, CancellationToken cancellationToken = default)
    {
        trip.Locations = trip
            .Locations
            .OrderBy(t => t.Start)
            .ToList();
        
        context
            .Entry(trip)
            .State = EntityState.Modified;
        
        return context
            .SaveChangesAsync(cancellationToken);
    }

    public Task Delete(Trip trip, CancellationToken cancellationToken = default)
    {
        context
            .Set<Trip>()
            .Remove(trip);
        
        return context
            .SaveChangesAsync(cancellationToken);
    }
    
    public IQueryable<Trip> QueryBy(Expression<Func<Trip, bool>> predicate)
    {
        return context
            .Set<Trip>()
            .Where(predicate);
    }
}