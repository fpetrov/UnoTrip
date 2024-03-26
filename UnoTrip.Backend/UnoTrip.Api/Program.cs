using UnoTrip.Api;
using UnoTrip.Api.Endpoints;
using UnoTrip.Application;
using UnoTrip.Infrastructure;

var builder = WebApplication.CreateSlimBuilder(args);

builder.Configuration.AddEnvironmentVariables();

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

api
    .MapGroup("/trip")
    .MapTripEndpoints()
    .MapEditTripEndpoints();

app.UseExceptionHandler();

var address = app.Configuration["API_ADDRESS"] ?? "localhost";

app.Run(address);

// Stack:
// NativeAOT (in future, EF Core has no NativeAOT support yet)
// Mediator
// Mapperly
// FluentValidation

// TODO: Fix issue where Contracts references Domain layer (just add local Location class?)