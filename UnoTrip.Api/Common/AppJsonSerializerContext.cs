using System.Text.Json.Serialization;
using UnoTrip.Application.Trip.Common;
using UnoTrip.Contracts.Trip;
using UnoTrip.Contracts.Trip.Add;
using UnoTrip.Contracts.Trip.Edit;
using UnoTrip.Contracts.User;

namespace UnoTrip.Api.Common;

[JsonSerializable(typeof(UserResponse))]
[JsonSerializable(typeof(CreateUserRequest))]
[JsonSerializable(typeof(UpdateUserRequest))]
[JsonSerializable(typeof(TripResponse))]
[JsonSerializable(typeof(CreateTripRequest))]
[JsonSerializable(typeof(AddTripSubscriberRequest))]
[JsonSerializable(typeof(AddTripNoteRequest))]
[JsonSerializable(typeof(EditTripDescriptionRequest))]
[JsonSerializable(typeof(EditTripNameRequest))]
[JsonSerializable(typeof(NoteResponse))]
[JsonSerializable(typeof(GetMyNotesResponse))]
[JsonSerializable(typeof(LocationResult))]
[JsonSerializable(typeof(RouteResult))]
internal partial class AppJsonSerializerContext : JsonSerializerContext;