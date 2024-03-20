using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using UnoTrip.Infrastructure.Persistence;

namespace UnoTrip.Infrastructure;

public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services,
        ConfigurationManager configuration)
    {
        services.AddPersistence(configuration);
        
        return services;
    }
}