using ErrorOr;

namespace UnoTrip.Domain.Common.Errors;

public static partial class Errors
{
    public static class Trip
    {
        public static Error NotFound()
            => Error.NotFound(
                code: "Trip.NotFound",
                description: "Trip was not found.");
        
        public static Error AlreadyExists()
            => Error.Conflict(
                code: "Trip.AlreadyExists",
                description: "Trip already exists.");
    }
}