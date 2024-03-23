using Mediator;
using Microsoft.AspNetCore.Mvc;
using UnoTrip.Api.Common.Mappings;
using UnoTrip.Application.Trip.Commands;
using UnoTrip.Application.Trip.Queries;
using UnoTrip.Contracts.Trip;

namespace UnoTrip.Api.Endpoints;

public static class TripEndpoints
{
    public static RouteGroupBuilder MapTripEndpoints(
        this RouteGroupBuilder group)
    {
        group.MapGet("/{uuid:guid}", GetTrip);
        group.MapGet("/my/{telegramId:long}", GetMyTrips);
        group.MapPost("/", CreateTrip);
        group.MapDelete("/{id:guid}", DeleteTrip);

        return group;
    }
    
    private static async Task<IResult> GetTrip(
        [FromRoute] Guid uuid,
        [FromServices] ISender sender)
    {
        var query = new GetTripById(uuid);
        var result = await sender.Send(query);
        
        return result.MatchFirst(
            tripResult => Results.Ok(TripMapper.Map(tripResult)),
            _ => Results.NotFound());
    }
    
    private static async Task<IResult> GetMyTrips(
        [FromRoute] long telegramId,
        [FromServices] ISender sender)
    {
        var query = new GetMyTrips(telegramId);
        var result = await sender.Send(query);
        
        return result.MatchFirst(
            tripResult => Results.Ok(tripResult.ConvertAll(TripMapper.Map)),
            _ => Results.NotFound());
    }
    
    private static async Task<IResult> CreateTrip(
        [FromBody] CreateTripRequest request,
        [FromServices] ISender sender)
    {
        var query = TripMapper.Map(request);
        var result = await sender.Send(query);
        
        return result.MatchFirst(
            tripResult => Results.Ok(TripMapper.Map(tripResult)),
            _ => Results.NotFound());
    }
    
    private static async Task<IResult> DeleteTrip(
        [FromRoute] Guid id,
        [FromServices] ISender sender)
    {
        var command = new DeleteTripCommand(id);
        var result = await sender.Send(command);
        
        return result.MatchFirst(
            subscribersResult => Results.Ok(new { Subscribers = subscribersResult }),
            _ => Results.NotFound());
    }
}