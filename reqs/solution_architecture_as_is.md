# Solution architecture for the Practix online cinema

```mermaid
flowchart TB
    subgraph clientFrontend[Client Frontend]
        userInterface[User Interface]
    end
    
    subgraph adminFrontend[Admin Frontend]
        webBrowser[Web Browser]
    end

    subgraph apiGateway[API Gateway]
        Nginx[Nginx Reverse proxy and Load balancer]
    end

    subgraph moviesCatalog[Movies Catalog]
        moviesAPI[Movies API]
        elasticsearchStorage[(Elasticsearch)]
        redisCacheMovies[(Redis)]
    end

    subgraph authService[Auth Service]
        direction TB
        authAPI[Auth API]
        postgresAuthDB[(PostgreSQL)]
        redisCacheAuth[(Redis)]
    end

    subgraph analyticsService[Analytics Service]
        analyticsAPI[Analytics API]
    end

    subgraph adminService[Admin Service]
        adminAPI[Admin API]
        postgresMoviesDB[(PostgreSQL)]
    end

    subgraph analytics[Analytics]
        clickhouseDB[(Clickhous)]
    end

    subgraph ETL[ETL]
        direction TB
        ETLConveyer[ETL]
        redisCacheETL[(Redis)]
    end

    clientFrontend --> apiGateway
    adminFrontend --> apiGateway
    apiGateway --> moviesCatalog
    apiGateway --> authService
    apiGateway --> analyticsService
    apiGateway --> adminService
    moviesAPI --Read--> elasticsearchStorage
    moviesAPI--Cache-->redisCacheMovies

    authAPI --> postgresAuthDB
    authAPI--Cache-->redisCacheAuth

    analyticsService --> kafka[Kafka]
    kafka --> consumer[Consumer]
    consumer --> clickhouseDB

    adminAPI --> postgresMoviesDB
    adminAPI --> authService
    
    postgresMoviesDB --Extract--> ETL
    ETLConveyer--State-->redisCacheETL
    ETL --Load--> elasticsearchStorage
```
