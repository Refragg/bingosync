FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build

ARG SSL_CERT_FILE
ARG SSL_CERT_PASSWORD
ARG PUBLIC_DOMAIN

ENV SSL_CERT_FILE $SSL_CERT_FILE
ENV SSL_CERT_PASSWORD $SSL_CERT_PASSWORD
ENV PUBLIC_DOMAIN $PUBLIC_DOMAIN

WORKDIR /src
COPY ["BingosyncYarp.csproj", "./"]
RUN dotnet restore "BingosyncYarp.csproj"
COPY . .
WORKDIR "/src/"

RUN sed -i "s/SSL_CERT_FILE/${SSL_CERT_FILE}/" appsettings.json
RUN sed -i "s/SSL_CERT_PASSWORD/${SSL_CERT_PASSWORD}/" appsettings.json
RUN sed -i "s/PUBLIC_DOMAIN/${PUBLIC_DOMAIN}/" appsettings.json

RUN dotnet build "BingosyncYarp.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "BingosyncYarp.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "BingosyncYarp.dll"]
