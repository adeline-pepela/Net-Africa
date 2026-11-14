using Microsoft.AspNetCore.SignalR;
using QualityDashboard.Services;

namespace QualityDashboard.Hubs;

public class MetricsHub : Hub
{
    private readonly DashboardService _dashboardService;
    private readonly MetricsService _metricsService;
    private readonly ILogger<MetricsHub> _logger;

    public MetricsHub(
        DashboardService dashboardService,
        MetricsService metricsService,
        ILogger<MetricsHub> logger)
    {
        _dashboardService = dashboardService;
        _metricsService = metricsService;
        _logger = logger;
    }

    public async Task GetDashboardState()
    {
        var state = await _dashboardService.GetDashboardStateAsync();
        await Clients.Caller.SendAsync("DashboardStateUpdated", state);
    }

    public async Task GetMetricsSummary()
    {
        var summary = await _metricsService.GetSummaryAsync();
        await Clients.All.SendAsync("MetricsSummaryUpdated", summary);
    }

    public async Task GetQualityGates()
    {
        var gates = await _metricsService.CheckQualityGatesAsync();
        await Clients.All.SendAsync("QualityGatesUpdated", gates);
    }

    public async Task RefreshAllMetrics()
    {
        var summary = await _metricsService.GetSummaryAsync();
        var gates = await _metricsService.CheckQualityGatesAsync();
        var conversations = await _dashboardService.GetConversationResultsAsync();
        var prodMetrics = await _dashboardService.GetProductionMetricsAsync();

        await Clients.All.SendAsync("MetricsRefreshed", new
        {
            summary,
            gates,
            conversations,
            prodMetrics
        });
    }

    public async Task BroadcastEvaluation(object evaluation)
    {
        await Clients.All.SendAsync("EvaluationCompleted", evaluation);
    }

    public async Task BroadcastAlertTriggered(object alert)
    {
        _logger.LogWarning("Alert triggered: {@Alert}", alert);
        await Clients.All.SendAsync("AlertTriggered", alert);
    }

    public override async Task OnConnectedAsync()
    {
        _logger.LogInformation($"Client connected: {Context.ConnectionId}");
        await base.OnConnectedAsync();
    }

    public override async Task OnDisconnectedAsync(Exception? exception)
    {
        _logger.LogInformation($"Client disconnected: {Context.ConnectionId}");
        await base.OnDisconnectedAsync(exception);
    }
}
