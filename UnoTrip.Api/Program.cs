using UnoTrip.Api;
using UnoTrip.Api.Endpoints;
using UnoTrip.Application;
using UnoTrip.Infrastructure;

var builder = WebApplication.CreateSlimBuilder(args);

// Register layers.
builder.Services
    .AddPresentation()
    .AddApplication()
    .AddInfrastructure(builder.Configuration);

var app = builder.Build();

var api = app.MapGroup("/api");

api
    .MapGroup("/user")
    .MapUserEndpoints();

app.UseExceptionHandler();

app.Run();

// Stack:
// NativeAOT (in future, EF Core has no NativeAOT support yet)
// Mediator
// Mapperly
// FluentValidation