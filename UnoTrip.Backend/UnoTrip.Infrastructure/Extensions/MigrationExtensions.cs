using Microsoft.AspNetCore.Builder;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using UnoTrip.Infrastructure.Persistence;

namespace UnoTrip.Infrastructure.Extensions;

public static class MigrationExtensions
{
    public static IApplicationBuilder ApplyMigrations(this IApplicationBuilder app)
    {
        using var context = app.ApplicationServices.CreateScope();
        using var dbContext = context.ServiceProvider.GetRequiredService<ApplicationContext>();

        dbContext.Database.Migrate();
        
        return app;
    }
}