using System.Text.Json;

namespace QualityDashboard.Services;

public class DashboardService
{
    private readonly ILogger<DashboardService> _logger;

    public DashboardService(ILogger<DashboardService> logger)
    {
        _logger = logger;
    }

    public async Task<DashboardState> GetDashboardStateAsync()
    {
        return new DashboardState
        {
            CurrentMode = "idle",
            Stage = "Ready",
            TotalEvaluations = 0,
            AverageCorrectness = 0.0,
            LastUpdate = DateTime.UtcNow
        };
    }

    public async Task<List<ConversationResult>> GetConversationResultsAsync()
    {
        try
        {
            // Try multiple possible paths
            var paths = new[]
            {
                Path.Combine(Directory.GetCurrentDirectory(), "..", "metrics", "evaluations.json"),
                Path.Combine(Directory.GetCurrentDirectory(), "metrics", "evaluations.json"),
                Path.Combine(AppContext.BaseDirectory, "..", "..", "metrics", "evaluations.json"),
                @"C:\Users\user\Downloads\Net Africa\Demo\metrics\evaluations.json"
            };

            foreach (var filePath in paths)
            {
                var fullPath = Path.GetFullPath(filePath);
                _logger.LogInformation($"Checking: {fullPath}");
                if (File.Exists(fullPath))
                {
                    _logger.LogInformation($"Found evaluations at: {fullPath}");
                    var json = await File.ReadAllTextAsync(fullPath);
                    var results = JsonSerializer.Deserialize<List<ConversationResult>>(json)
                        ?? new List<ConversationResult>();
                    return results;
                }
            }
        }
        catch (Exception ex)
        {
            _logger.LogError($"Error loading evaluations: {ex.Message}");
        }

        return new List<ConversationResult>();
    }

    public async Task<ProductionMetrics?> GetProductionMetricsAsync()
    {
        try
        {
            var paths = new[]
            {
                Path.Combine(Directory.GetCurrentDirectory(), "..", "metrics", "prod-monitoring.json"),
                Path.Combine(Directory.GetCurrentDirectory(), "metrics", "prod-monitoring.json"),
                Path.Combine(AppContext.BaseDirectory, "..", "..", "metrics", "prod-monitoring.json"),
                @"C:\Users\user\Downloads\Net Africa\Demo\metrics\prod-monitoring.json"
            };

            foreach (var filePath in paths)
            {
                var fullPath = Path.GetFullPath(filePath);
                if (File.Exists(fullPath))
                {
                    _logger.LogInformation($"Found prod metrics at: {fullPath}");
                    var json = await File.ReadAllTextAsync(fullPath);
                    var metrics = JsonSerializer.Deserialize<ProductionMetrics>(json);
                    return metrics;
                }
            }
        }
        catch (Exception ex)
        {
            _logger.LogError($"Error loading prod metrics: {ex.Message}");
        }

        return null;
    }

    public async Task<List<TraceResult>> GetTracesAsync()
    {
        try
        {
            var paths = new[]
            {
                Path.Combine(Directory.GetCurrentDirectory(), "..", "traces", "interactive.json"),
                Path.Combine(Directory.GetCurrentDirectory(), "traces", "interactive.json"),
                Path.Combine(AppContext.BaseDirectory, "..", "..", "traces", "interactive.json"),
                @"C:\Users\user\Downloads\Net Africa\Demo\traces\interactive.json"
            };

            foreach (var filePath in paths)
            {
                var fullPath = Path.GetFullPath(filePath);
                if (File.Exists(fullPath))
                {
                    _logger.LogInformation($"Found traces at: {fullPath}");
                    var json = await File.ReadAllTextAsync(fullPath);
                    var traces = JsonSerializer.Deserialize<List<TraceResult>>(json)
                        ?? new List<TraceResult>();
                    return traces;
                }
            }
        }
        catch (Exception ex)
        {
            _logger.LogError($"Error loading traces: {ex.Message}");
        }

        return new List<TraceResult>();
    }
}

public class DashboardState
{
    public string CurrentMode { get; set; } = "idle";
    public string Stage { get; set; } = "";
    public int TotalEvaluations { get; set; }
    public double AverageCorrectness { get; set; }
    public DateTime LastUpdate { get; set; }
}

public class ConversationResult
{
    [System.Text.Json.Serialization.JsonPropertyName("query")]
    public string Query { get; set; } = "";

    [System.Text.Json.Serialization.JsonPropertyName("correctness")]
    public double Correctness { get; set; }

    [System.Text.Json.Serialization.JsonPropertyName("tool_use_accuracy")]
    public double ToolUseAccuracy { get; set; }

    [System.Text.Json.Serialization.JsonPropertyName("helpfulness")]
    public double Helpfulness { get; set; }

    [System.Text.Json.Serialization.JsonPropertyName("instruction_following")]
    public double InstructionFollowing { get; set; }

    [System.Text.Json.Serialization.JsonPropertyName("timestamp")]
    public DateTime Timestamp { get; set; }
}

public class ProductionMetrics
{
    public DateTime Timestamp { get; set; }
    public int EvaluationsRun { get; set; }
    public int TotalRequests { get; set; }
    public double SamplingRate { get; set; }
    public List<double> CorrectnessHistory { get; set; } = new();
    public List<double> ToolAccuracyHistory { get; set; } = new();
    public double CostEstimate { get; set; }
    public bool AlertTriggered { get; set; }
    public string? AlertMessage { get; set; }
}

public class TraceResult
{
    public string Query { get; set; } = "";
    public string Response { get; set; } = "";
    public List<string> ToolsUsed { get; set; } = new();
    public long DurationMs { get; set; }
    public DateTime Timestamp { get; set; }
}
