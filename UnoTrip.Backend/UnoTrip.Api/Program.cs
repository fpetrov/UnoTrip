using UnoTrip.Api;
using UnoTrip.Api.Endpoints;
using UnoTrip.Application;
using UnoTrip.Infrastructure;
using UnoTrip.Infrastructure.Extensions;

var builder = WebApplication.CreateSlimBuilder(args);

// Register layers.
builder.Services
    .AddPresentation()
    .AddApplication()
    .AddInfrastructure(builder.Configuration);

var app = builder.Build();

// Apply database migrations.
app.ApplyMigrations();

var api = app.MapGroup("/api");

api
    .MapGroup("/user")
    .MapUserEndpoints();

api
    .MapGroup("/trip")
    .MapTripEndpoints()
    .MapEditTripEndpoints();

app.UseExceptionHandler();

app.Run();

// Stack:
// NativeAOT (in future, EF Core has no NativeAOT support yet)
// Mediator
// Mapperly
// FluentValidation

// TODO: Fix issue where Contracts references Domain layer (just add local Location class?)