using ErrorOr;
using FluentValidation;
using Mediator;

namespace UnoTrip.Application.Common.Behaviors;

public class ValidationBehavior<TRequest, TResponse>(
    IValidator<TRequest>? validator = null)
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
    where TResponse : IErrorOr

{
    public async ValueTask<TResponse> Handle(
        TRequest request,
        CancellationToken cancellationToken,
        MessageHandlerDelegate<TRequest, TResponse> next)
    {
        if (validator is null)
            return await next(request, cancellationToken);

        var validationResult = await validator.ValidateAsync(request, cancellationToken);
        
        if (validationResult.IsValid)
            return await next(request, cancellationToken);

        var firstError = validationResult.Errors.First();
        var error = Error.Validation(
            firstError.PropertyName,
            firstError.ErrorMessage);
        
        return (dynamic)error;
    }
}