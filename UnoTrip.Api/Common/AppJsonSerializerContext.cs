using System.Text.Json.Serialization;
using UnoTrip.Contracts.Trip;
using UnoTrip.Contracts.User;

namespace UnoTrip.Api.Common;

[JsonSerializable(typeof(UserResponse))]
[JsonSerializable(typeof(CreateUserRequest))]
[JsonSerializable(typeof(UpdateUserRequest))]
[JsonSerializable(typeof(TripResponse))]
[JsonSerializable(typeof(CreateTripRequest))]
[JsonSerializable(typeof(AddTripSubscriberRequest))]
[JsonSerializable(typeof(EditTripDescriptionRequest))]
[JsonSerializable(typeof(EditTripNameRequest))]
// [JsonSerializable(typeof(RemoveTripLocationRequest))]
internal partial class AppJsonSerializerContext : JsonSerializerContext;