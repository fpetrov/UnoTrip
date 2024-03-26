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

# Run database update
FROM build as migrations
ENV PATH="$PATH:/root/.dotnet/tools"
RUN dotnet tool install --version 8.0.2 --global dotnet-ef
ENTRYPOINT dotnet ef database update --project "{$STARTUP_PROJECT}\{$STARTUP_PROJECT}.csproj" --startup-project "{$STARTUP_PROJECT}\{$STARTUP_PROJECT}.csproj" --context {$APPLICATION_CONTEXT} --configuration Release

WORKDIR "/src/UnoTrip.Api"

RUN dotnet build "UnoTrip.Api.csproj" -c $BUILD_CONFIGURATION -o /app/build

FROM build AS publish
ARG BUILD_CONFIGURATION=Release
RUN dotnet publish "UnoTrip.Api.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "UnoTrip.Api.dll"]
