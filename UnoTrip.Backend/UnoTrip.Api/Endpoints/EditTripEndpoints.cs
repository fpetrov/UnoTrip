using Mediator;
using Microsoft.AspNetCore.Mvc;
using UnoTrip.Application.Trip.Commands;
using UnoTrip.Contracts.Trip;
using UnoTrip.Contracts.Trip.Add;
using UnoTrip.Contracts.Trip.Edit;
using UnoTrip.Domain.Entities;

namespace UnoTrip.Api.Endpoints;

public static class EditTripEndpoints
{
    public static RouteGroupBuilder MapEditTripEndpoints(this RouteGroupBuilder group)
    {
        group.MapPatch("/{uuid:guid}/description", EditTripDescription);
        group.MapPatch("/{uuid:guid}/name", EditTripName);
        group.MapPost("/{uuid:guid}/location", AddTripLocation);
        group.MapDelete("/{uuid:guid}/location/{locationId:int}", DeleteTripLocation);
        group.MapPost("/{uuid:guid}/subscribe", AddTripSubscriber);
        group.MapPost("/{uuid:guid}/note", AddTripNote);
        
        return group;
    }
    
    private static async Task<IResult> EditTripDescription(
        [FromRoute] Guid uuid,
        [FromBody] EditTripDescriptionRequest request,
        [FromServices] ISender sender)
    {
        var command = new EditTripDescriptionCommand(uuid, request.Description);
        var result = await sender.Send(command);
        
        return result.MatchFirst(
            Results.Ok,
            _ => Results.NotFound());
    }
    
    private static async Task<IResult> EditTripName(
        [FromRoute] Guid uuid,
        [FromBody] EditTripNameRequest request,
        [FromServices] ISender sender)
    {
        var command = new EditTripNameCommand(uuid, request.Name);
        var result = await sender.Send(command);
        
        return result.MatchFirst(
            Results.Ok,
            _ => Results.NotFound());
    }
    
    private static async Task<IResult> AddTripLocation(
        [FromRoute] Guid uuid,
        [FromBody] Location location,
        [FromServices] ISender sender)
    {
        var command = new AddTripLocationCommand(uuid, location);
        var result = await sender.Send(command);
        
        return result.MatchFirst(
            Results.Ok,
            _ => Results.NotFound());
    }

    private static async Task<IResult> DeleteTripLocation(
        [FromRoute] Guid uuid,
        [FromRoute] int locationId,
        [FromServices] ISender sender)
    {
        var command = new RemoveTripLocationCommand(uuid, locationId);
        var result = await sender.Send(command);

        return result.MatchFirst(
            Results.Ok,
            _ => Results.NotFound());
    }
    
    private static async Task<IResult> AddTripSubscriber(
        [FromRoute] Guid uuid,
        [FromBody] AddTripSubscriberRequest request,
        [FromServices] ISender sender)
    {
        var command = new AddTripSubscriberCommand(uuid, request.TelegramId);
        var result = await sender.Send(command);
        
        return result.MatchFirst(
            subscriberResult => Results.Ok(new { Subscribers = subscriberResult }),
            _ => Results.NotFound());
    }
    
    private static async Task<IResult> AddTripNote(
        [FromRoute] Guid uuid,
        [FromBody] AddTripNoteRequest request,
        [FromServices] ISender sender)
    {
        var command = new AddTripNoteCommand(request.TelegramId, uuid, request.Name, request.ContentType, request.FileId, request.IsPrivate);
        var result = await sender.Send(command);
        
        return result.MatchFirst(
            Results.Ok,
            _ => Results.NotFound());
    }
}