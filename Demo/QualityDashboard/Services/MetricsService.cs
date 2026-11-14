namespace QualityDashboard.Services;

public class MetricsService
{
    private readonly DashboardService _dashboardService;
    private readonly ILogger<MetricsService> _logger;

    public MetricsService(DashboardService dashboardService, ILogger<MetricsService> logger)
    {
        _dashboardService = dashboardService;
        _logger = logger;
    }

    public async Task<MetricsSummary> GetSummaryAsync()
    {
        var conversations = await _dashboardService.GetConversationResultsAsync();
        var prodMetrics = await _dashboardService.GetProductionMetricsAsync();

        var summary = new MetricsSummary();

        if (conversations.Any())
        {
            summary.TotalConversations = conversations.Count;
            summary.AverageCorrectness = conversations.Average(c => c.Correctness);
            summary.AverageToolAccuracy = conversations.Average(c => c.ToolUseAccuracy);
            summary.AverageHelpfulness = conversations.Average(c => c.Helpfulness);
            summary.AverageInstructionFollowing = conversations.Average(c => c.InstructionFollowing);
        }

        if (prodMetrics != null)
        {
            summary.ProductionRequests = prodMetrics.TotalRequests;
            summary.SamplingRate = prodMetrics.SamplingRate;
            summary.CostEstimate = prodMetrics.CostEstimate;
            summary.AlertTriggered = prodMetrics.AlertTriggered;
            summary.AlertMessage = prodMetrics.AlertMessage;

            if (prodMetrics.CorrectnessHistory.Any())
            {
                summary.ProductionCorrectnessAverage = prodMetrics.CorrectnessHistory.Average();
                summary.CurrentCorrectnessTrend = prodMetrics.CorrectnessHistory.Last();
            }
        }

        return summary;
    }

    public async Task<QualityGateStatus> CheckQualityGatesAsync()
    {
        var conversations = await _dashboardService.GetConversationResultsAsync();
        var status = new QualityGateStatus();

        if (!conversations.Any())
            return status;

        var avgCorrectness = conversations.Average(c => c.Correctness);
        var avgToolAccuracy = conversations.Average(c => c.ToolUseAccuracy);
        var avgHelpfulness = conversations.Average(c => c.Helpfulness);

        status.CorrectnessGate = new GateResult
        {
            Name = "Correctness",
            Threshold = 0.85,
            CurrentValue = avgCorrectness,
            Passed = avgCorrectness >= 0.85
        };

        status.ToolAccuracyGate = new GateResult
        {
            Name = "Tool Accuracy",
            Threshold = 0.90,
            CurrentValue = avgToolAccuracy,
            Passed = avgToolAccuracy >= 0.90
        };

        status.HelpfulnessGate = new GateResult
        {
            Name = "Helpfulness",
            Threshold = 0.80,
            CurrentValue = avgHelpfulness,
            Passed = avgHelpfulness >= 0.80
        };

        status.AllPassed = status.CorrectnessGate.Passed
            && status.ToolAccuracyGate.Passed
            && status.HelpfulnessGate.Passed;

        return status;
    }
}

public class MetricsSummary
{
    public int TotalConversations { get; set; }
    public double AverageCorrectness { get; set; }
    public double AverageToolAccuracy { get; set; }
    public double AverageHelpfulness { get; set; }
    public double AverageInstructionFollowing { get; set; }
    public int ProductionRequests { get; set; }
    public double SamplingRate { get; set; }
    public double CostEstimate { get; set; }
    public bool AlertTriggered { get; set; }
    public string? AlertMessage { get; set; }
    public double ProductionCorrectnessAverage { get; set; }
    public double CurrentCorrectnessTrend { get; set; }
}

public class QualityGateStatus
{
    public GateResult CorrectnessGate { get; set; } = new();
    public GateResult ToolAccuracyGate { get; set; } = new();
    public GateResult HelpfulnessGate { get; set; } = new();
    public bool AllPassed { get; set; }
}

public class GateResult
{
    public string Name { get; set; } = "";
    public double Threshold { get; set; }
    public double CurrentValue { get; set; }
    public bool Passed { get; set; }
}
