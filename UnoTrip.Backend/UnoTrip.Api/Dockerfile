FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
USER $APP_UID
WORKDIR /app
EXPOSE 8080
EXPOSE 8081

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
ARG BUILD_CONFIGURATION=Release
WORKDIR /src
COPY ["UnoTrip.Api/UnoTrip.Api.csproj", "UnoTrip.Api/"]
COPY ["UnoTrip.Application/UnoTrip.Application.csproj", "UnoTrip.Application/"]
COPY ["UnoTrip.Domain/UnoTrip.Domain.csproj", "UnoTrip.Domain/"]
COPY ["UnoTrip.Contracts/UnoTrip.Contracts.csproj", "UnoTrip.Contracts/"]
COPY ["UnoTrip.Infrastructure/UnoTrip.Infrastructure.csproj", "UnoTrip.Infrastructure/"]
RUN dotnet restore "UnoTrip.Api/UnoTrip.Api.csproj"
COPY . .
WORKDIR "/src/UnoTrip.Api"
RUN dotnet build "UnoTrip.Api.csproj" -c $BUILD_CONFIGURATION -o /app/build

FROM build AS publish
ARG BUILD_CONFIGURATION=Release
RUN dotnet publish "UnoTrip.Api.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "UnoTrip.Api.dll"]
