using ErrorOr;

namespace UnoTrip.Domain.Common.Errors;

public static partial class Errors
{
    public static class User
    {
        public static Error Duplicate()
            => Error.Conflict(
                code: "User.Duplicate",
                description: "User already exists.");
        
        public static Error NotFound()
            => Error.NotFound(
                code: "User.NotFound",
                description: "User not found.");
        
        public static Error Validation()
            => Error.Validation(
                code :"User.Validation",
                description: "User validation failed.");
    }
}