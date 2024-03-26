using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using UnoTrip.Application.Common.Interfaces.Persistence;

namespace UnoTrip.Infrastructure.Persistence;

public static class DependencyInjection
{
    public static IServiceCollection AddPersistence(
        this IServiceCollection services,
        ConfigurationManager configuration)
    {
        // var connectionString = configuration.GetConnectionString("DefaultConnection");
        
        var connectionString = configuration["CONNECTION_STRING"];
        
        services
            .AddDbContext<ApplicationContext>(
                options => options.UseNpgsql(connectionString));

        services.AddScoped<IUserRepository, UserRepository>();
        services.AddScoped<ITripRepository, TripRepository>();
        services.AddScoped<ILocationRepository, LocationRepository>();
        
        return services;
    }
}