using Microsoft.EntityFrameworkCore;
using UnoTrip.Domain.Entities;

namespace UnoTrip.Infrastructure.Persistence;

public class ApplicationContext : DbContext
{
    public DbSet<User> Users { get; set; }

    public ApplicationContext(DbContextOptions<ApplicationContext> options)
        : base(options)
    {
        
    }
}