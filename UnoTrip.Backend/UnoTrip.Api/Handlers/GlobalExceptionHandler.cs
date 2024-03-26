using Microsoft.AspNetCore.Diagnostics;

namespace UnoTrip.Api.Handlers;

public class GlobalExceptionHandler(
    ILogger<GlobalExceptionHandler> logger) 
    : IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(
        HttpContext context,
        Exception exception,
        CancellationToken cancellationToken)
    {
        context.Response.StatusCode = StatusCodes.Status400BadRequest;
        context.Response.ContentType = "application/json";
        
        logger.LogError(exception.Message);
        await context.Response.WriteAsync("{ \"reason\": \"Bad request\" }", cancellationToken: cancellationToken);

        return true;
    }
}