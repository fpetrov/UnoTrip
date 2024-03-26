using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Internal;
using UnoTrip.Domain.Entities;

namespace UnoTrip.Infrastructure.Persistence;

public class ApplicationContext : DbContext
{
    public DbSet<User> Users { get; set; }
    public DbSet<Location> Locations { get; set; }

    public ApplicationContext(DbContextOptions<ApplicationContext> options)
        : base(options)
    {
        
    }
    
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder
            .Entity<User>()
            .HasMany(t => t.Trips)
            .WithMany(t => t.Subscribers);
    }
}