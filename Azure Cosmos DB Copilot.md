
# Azure Cosmos DB Copilot Pipeline

```mermaid
graph LR
    A[System Prompts] --> D[Azure OpenAI Service]
    B[Few-shot Examples] --> D
    C[Schema info] --> D
    D --> E[Validation]
    E --> F[Testing]
    F --> G[Microsoft Copilot for Azure in Cosmos DB]
```
