using ErrorOr;
using Mediator;
using Microsoft.AspNetCore.Mvc;
using UnoTrip.Api.Common.Mappings;
using UnoTrip.Application.User.Queries;
using UnoTrip.Contracts.User;

namespace UnoTrip.Api.Endpoints;

public static class UserEndpoints
{
    public static RouteGroupBuilder MapUserEndpoints(
        this RouteGroupBuilder group)
    {
        group.MapGet("/{telegramId:long}", GetUser);
        group.MapPost("/", CreateUser);
        group.MapPatch("/", UpdateUser);
        
        return group;
    }
    
    private static async Task<IResult> UpdateUser(
        [FromBody] UpdateUserRequest request,
        [FromServices] ISender sender)
    {
        var command = UserMapper.Map(request);
        var result = await sender.Send(command);
        
        return result.MatchFirst(
            user => Results.Ok(UserMapper.Map(user)),
            ErrorMatch);
    }
    
    private static async Task<IResult> CreateUser(
        [FromBody] CreateUserRequest request,
        [FromServices] ISender sender)
    {
        var command = UserMapper.Map(request);
        var result = await sender.Send(command);
        
        return result.MatchFirst(
            user => Results.Ok(UserMapper.Map(user)),
            ErrorMatch);
    }
    
    private static async Task<IResult> GetUser(
        [FromRoute] long telegramId,
        [FromServices] ISender sender)
    {
        var query = new GetUserQuery(telegramId);
        var result = await sender.Send(query);
        
        return result.MatchFirst(
            user => Results.Ok(UserMapper.Map(user)),
            ErrorMatch);
    }
    
    private static IResult ErrorMatch(Error error) =>
        error.Type switch
        {
            ErrorType.Validation => Results.BadRequest("Данные переданы в некорректном формате."),
            ErrorType.Conflict => Results.Conflict("Пользователь с таким логином или почтой или телефоном уже существует."),
            _ => Results.NotFound()
        };
}