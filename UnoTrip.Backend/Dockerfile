﻿FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443

ARG STARTUP_PROJECT="Prod.Api"
ARG APPLICATION_CONTEXT="Prod.Infrastructure.Persistence.ApplicationContext"

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

COPY . /src

RUN dotnet restore --runtime linux-x64
COPY . .
WORKDIR /src

# Run database update
FROM build as migrations
ENV PATH="$PATH:/root/.dotnet/tools"
RUN dotnet tool install --version 8.0.2 --global dotnet-ef
ENTRYPOINT dotnet ef database update --project "{$STARTUP_PROJECT}\{$STARTUP_PROJECT}.csproj" --startup-project "{$STARTUP_PROJECT}\{$STARTUP_PROJECT}.csproj" --context {$APPLICATION_CONTEXT} --configuration Release

RUN dotnet build -c Release -o /app/build

FROM build AS publish
RUN dotnet publish -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "${STARTUP_PROJECT}.dll"]