# Quality Monitoring Dashboard

A professional ASP.NET Core Blazor web dashboard for visualizing continuous quality monitoring of AI agents.

## Overview

This dashboard provides real-time insights into the three-stage quality monitoring framework:
- **Stage 1:** Local Development (interactive chat testing)
- **Stage 2:** CI/CD Pipeline (quality gates)
- **Stage 3:** Production Monitoring (real-world drift detection)

## Features

### 🏠 Overview Dashboard
- Real-time KPI cards (Correctness, Tool Accuracy, Helpfulness, Monthly Cost)
- Quality gate status visualization
- Recent evaluations table
- Quick action buttons
- Production alert notifications

### 💬 Interactive Chat
- Test the agent in real-time
- See OpenTelemetry traces for every interaction
- View quality scores instantly
- Immediate feedback for developers
- Trace tree visualization

### ✓ Quality Gates
- Visual gate status cards
- Pass/fail indicators
- Threshold comparison
- Evaluation details table
- GitHub Actions workflow integration example

### 📈 Production Monitoring
- Correctness trend chart
- Tool accuracy trend chart
- Sampling strategy info
- Cost analysis per sampling rate
- Alert triggered notification
- Real-world metrics display

### 🔍 Trace Analysis
- OpenTelemetry trace visualization
- Span hierarchy display
- Detailed attributes and timing
- Tool execution tracking
- Interactive trace inspection

### 💰 Cost Analysis
- Monthly monitoring cost breakdown
- Incident cost analysis
- ROI calculations (1-3 incidents/year)
- Payback period analysis
- Cost optimization strategies
- Comparison with traditional approaches

## Quick Start

### Prerequisites
- .NET 8.0 SDK or later
- Visual Studio, VS Code, or any .NET IDE

### Running the Dashboard

```bash
# Navigate to the dashboard directory
cd "C:\Users\user\Downloads\Net Africa\Demo\QualityDashboard"

# Restore dependencies
dotnet restore

# Run the application
dotnet run

# Open in browser
# Navigate to: https://localhost:5001
```

First run compiles the application (~5-10 seconds). Subsequent runs start in 1-2 seconds.

### Environment Configuration

Create `appsettings.json` in the dashboard root:

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information"
    }
  },
  "AllowedHosts": "*"
}
```

## Architecture

### Services

#### DashboardService
Loads evaluation data and trace files from the console demo output.

```csharp
public class DashboardService
{
    public async Task<DashboardState> GetDashboardStateAsync();
    public async Task<List<ConversationResult>> GetConversationResultsAsync();
    public async Task<ProductionMetrics?> GetProductionMetricsAsync();
    public async Task<List<TraceResult>> GetTracesAsync();
}
```

#### MetricsService
Calculates summary statistics and quality gate status.

```csharp
public class MetricsService
{
    public async Task<MetricsSummary> GetSummaryAsync();
    public async Task<QualityGateStatus> CheckQualityGatesAsync();
}
```

#### AgentService
Simulates agent interactions for the interactive chat mode.

```csharp
public class AgentService
{
    public async Task<AgentInteractionResult> ProcessQueryAsync(string query);
}
```

#### MetricsHub
SignalR hub for real-time updates across all connected clients.

```csharp
public class MetricsHub : Hub
{
    public async Task RefreshAllMetrics();
    public async Task BroadcastEvaluation(object evaluation);
    public async Task BroadcastAlertTriggered(object alert);
}
```

### Components

- **GateCard** - Quality gate status card with progress visualization
- **ScoreBar** - Score progress bar with threshold comparison
- **MainLayout** - Navigation sidebar and main layout

### Pages

| Page | Route | Purpose |
|------|-------|---------|
| Overview | `/` | Main dashboard with KPIs and quick actions |
| Chat | `/chat` | Interactive agent testing with live traces |
| Evaluation | `/evaluation` | Quality gates and CI/CD integration |
| Production | `/production` | Real-world monitoring and drift detection |
| Traces | `/traces` | OpenTelemetry trace analysis |
| Cost | `/cost` | ROI and cost analysis |

## Integration with Console Demo

The dashboard reads output files from the console demo:

```
metrics/evaluations.json       ← Mode 2 (Batch evaluation)
metrics/prod-monitoring.json   ← Mode 3 (Production simulation)
traces/interactive.json        ← Mode 1 (Interactive chat)
```

**Workflow:**
1. Run console demo: `cd Demo && dotnet run`
2. Select a mode (1-4)
3. Dashboard automatically reads output files
4. Refresh browser to see updated data

## Data Flow

```
Console Demo (Program.cs)
    ↓
    ├─ Mode 1: Interactive Chat
    │  └─→ traces/interactive.json
    │
    ├─ Mode 2: Batch Evaluation
    │  └─→ metrics/evaluations.json
    │
    └─ Mode 3: Production Simulation
       └─→ metrics/prod-monitoring.json
    
    ↓
Dashboard (Blazor)
    ├─ DashboardService reads JSON files
    ├─ MetricsService calculates stats
    └─ Components render visualizations
```

## Real-Time Updates

The dashboard uses SignalR for real-time communication:

```csharp
// In components
hubConnection = new HubConnectionBuilder()
    .WithUrl(Navigation.ToAbsoluteUri("/metrics-hub"))
    .WithAutomaticReconnect()
    .Build();

hubConnection.On<MetricsSummary>("MetricsSummaryUpdated", 
    async (newSummary) => {
        summary = newSummary;
        await InvokeAsync(StateHasChanged);
    });
```

## Styling

- **Bootstrap 5** for responsive layout
- **CSS Grid** for quality scores display
- **Custom theme** with professional color scheme
- **Dark navbar** with light content
- **Card-based** components
- **Responsive design** for mobile/tablet

### Color Scheme

| Color | Use |
|-------|-----|
| Primary (#0d6efd) | Buttons, links, primary metrics |
| Success (#198754) | Passed gates, positive metrics |
| Danger (#dc3545) | Failed gates, alerts |
| Warning (#ffc107) | Warnings, review needed |
| Info (#0dcaf0) | Information, secondary metrics |

## Customization

### Adding a New Page

1. Create file: `Pages/NewPage.razor`
2. Add route: `@page "/newpage"`
3. Add navigation link in `MainLayout.razor`

### Changing Thresholds

Edit `appsettings.json`:

```json
{
  "QualityThresholds": {
    "Correctness": 0.85,
    "ToolAccuracy": 0.90,
    "Helpfulness": 0.80
  }
}
```

### Customizing Colors

Edit `wwwroot/app.css`:

```css
:root {
    --primary-color: #0d6efd;
    --success-color: #198754;
    --danger-color: #dc3545;
}
```

## Production Deployment

### Azure App Service

```bash
# Create resource group
az group create -n quality-dashboard -l eastus

# Create App Service plan
az appservice plan create -n dashboard-plan \
  -g quality-dashboard --sku B2

# Create web app
az webapp create -n quality-dashboard \
  -g quality-dashboard -p dashboard-plan \
  --runtime "dotnet|8.0"

# Deploy
dotnet publish -c Release -o publish
cd publish && zip -r ../app.zip . && cd ..
az webapp deployment source config-zip \
  -g quality-dashboard \
  -n quality-dashboard \
  --src app.zip
```

### Docker

```dockerfile
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 80 443

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["QualityDashboard.csproj", "."]
RUN dotnet restore "QualityDashboard.csproj"
COPY . .
RUN dotnet build -c Release -o /app/build

FROM build AS publish
RUN dotnet publish -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "QualityDashboard.dll"]
```

Run:
```bash
docker build -t quality-dashboard .
docker run -p 80:80 quality-dashboard
```

## Troubleshooting

### Port Already in Use
```bash
# Change port in launchSettings.json or run with custom port
dotnet run --urls "http://localhost:5002"
```

### No Data Showing
1. Ensure console demo has been run with modes 1-3
2. Check that files exist:
   - `../metrics/evaluations.json`
   - `../metrics/prod-monitoring.json`
   - `../traces/interactive.json`
3. Refresh the browser

### SignalR Connection Issues
1. Check browser console for errors
2. Ensure WebSocket is enabled
3. Check firewall/proxy settings
4. Look at server logs for Hub exceptions

## Performance

- **Dashboard load:** <500ms
- **Page navigation:** <200ms
- **Chat response:** 500-1500ms (simulated)
- **Real-time updates:** <100ms latency
- **Trace rendering:** <200ms for 50+ spans

## Security Considerations

- No authentication required (internal tool)
- To add auth, use ASP.NET Core Identity
- For production, enable HTTPS
- Validate file access paths (prevent directory traversal)

## Future Enhancements

- [ ] Database persistence instead of JSON files
- [ ] User authentication and roles
- [ ] Email alerts for quality gate failures
- [ ] Slack integration for alerts
- [ ] Custom dashboard builder
- [ ] Export reports (PDF, CSV)
- [ ] Historical data analysis
- [ ] A/B testing framework
- [ ] Custom evaluation prompts
- [ ] Multi-tenant support

## Support

For issues or questions:
1. Check `RUNNING-THE-DEMO.md` for console demo help
2. See `Demo-README.md` for architecture details
3. Review code comments in services and components
4. Check browser console for client-side errors

## License

Same as parent project
