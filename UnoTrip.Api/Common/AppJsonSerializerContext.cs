using System.Text.Json.Serialization;
using UnoTrip.Contracts.User;

namespace UnoTrip.Api.Common;

[JsonSerializable(typeof(UserResponse))]
[JsonSerializable(typeof(CreateUserRequest))]
internal partial class AppJsonSerializerContext : JsonSerializerContext;