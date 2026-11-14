namespace QualityDashboard.Services;

public class AgentService
{
    private readonly ILogger<AgentService> _logger;

    public AgentService(ILogger<AgentService> logger)
    {
        _logger = logger;
    }

    public async Task<AgentInteractionResult> ProcessQueryAsync(string query)
    {
        // Simulate agent processing
        await Task.Delay(Random.Shared.Next(500, 1500));

        var tools = SelectTools(query);
        var response = await GenerateResponse(query, tools);
        var scores = await EvaluateResponse(query, response, tools);

        return new AgentInteractionResult
        {
            Query = query,
            Response = response,
            ToolsUsed = tools,
            ExecutionTimeMs = Random.Shared.Next(200, 800),
            Scores = scores,
            Timestamp = DateTime.UtcNow,
            Trace = GenerateTrace(query, tools)
        };
    }

    private List<string> SelectTools(string query)
    {
        var queryLower = query.ToLower();
        var tools = new List<string>();

        if (queryLower.Contains("password") || queryLower.Contains("reset"))
            tools.Add("SearchKnowledgeBase");
        if (queryLower.Contains("bill") || queryLower.Contains("payment"))
            tools.Add("GetCustomerHistory");
        if (queryLower.Contains("ticket") || queryLower.Contains("issue") || queryLower.Contains("problem"))
            tools.Add("CreateTicket");

        if (!tools.Any())
            tools.Add("SearchKnowledgeBase");

        return tools;
    }

    private async Task<string> GenerateResponse(string query, List<string> tools)
    {
        var responses = new Dictionary<string, string>
        {
            ["password"] = "To reset your password, visit Settings > Security > Change Password. Enter your email and follow the verification link sent to your inbox.",
            ["bill"] = "Your current bill is $299.99, due on December 15th. You can view your full billing history in the Billing section of your account.",
            ["history"] = "Your account has 3 open support tickets and 12 resolved tickets this year. Your most recent interaction was on November 1st.",
            ["cancel"] = "I understand you'd like to cancel. Your subscription will be deactivated immediately. You'll have access until the end of your current billing period.",
            ["upgrade"] = "You can upgrade your plan anytime. Premium includes priority support, advanced analytics, and API access. Would you like more details?"
        };

        foreach (var key in responses.Keys)
        {
            if (query.ToLower().Contains(key))
                return responses[key];
        }

        return "I'd be happy to help. Could you provide more details about what you need?";
    }

    private async Task<ResponseScores> EvaluateResponse(string query, string response, List<string> tools)
    {
        // Simulate evaluation
        await Task.Delay(Random.Shared.Next(300, 800));

        var baseScore = 0.85 + (Random.Shared.NextDouble() * 0.15);

        return new ResponseScores
        {
            Correctness = Math.Round(baseScore, 2),
            ToolUseAccuracy = Math.Round(baseScore + Random.Shared.NextDouble() * 0.05, 2),
            Helpfulness = Math.Round(baseScore - Random.Shared.NextDouble() * 0.05, 2),
            InstructionFollowing = Math.Round(baseScore, 2)
        };
    }

    private TraceData GenerateTrace(string query, List<string> tools)
    {
        return new TraceData
        {
            TraceId = Guid.NewGuid().ToString("N")[..16],
            Spans = new List<Span>
            {
                new Span
                {
                    Name = "agent.run",
                    DurationMs = Random.Shared.Next(200, 800),
                    Attributes = new Dictionary<string, string>
                    {
                        { "query", query },
                        { "tools_count", tools.Count.ToString() }
                    }
                },
                new Span
                {
                    Name = "llm.call",
                    DurationMs = Random.Shared.Next(200, 500),
                    Attributes = new Dictionary<string, string>
                    {
                        { "model", "claude-3-5-sonnet" },
                        { "tokens_in", "245" },
                        { "tokens_out", "89" }
                    }
                },
                new Span
                {
                    Name = "tool.execution",
                    DurationMs = Random.Shared.Next(50, 200),
                    Attributes = new Dictionary<string, string>
                    {
                        { "tools_used", string.Join(",", tools) },
                        { "success", "true" }
                    }
                }
            }
        };
    }
}

public class AgentInteractionResult
{
    public string Query { get; set; } = "";
    public string Response { get; set; } = "";
    public List<string> ToolsUsed { get; set; } = new();
    public int ExecutionTimeMs { get; set; }
    public ResponseScores Scores { get; set; } = new();
    public DateTime Timestamp { get; set; }
    public TraceData Trace { get; set; } = new();
}

public class ResponseScores
{
    public double Correctness { get; set; }
    public double ToolUseAccuracy { get; set; }
    public double Helpfulness { get; set; }
    public double InstructionFollowing { get; set; }

    public double Average => (Correctness + ToolUseAccuracy + Helpfulness + InstructionFollowing) / 4;
}

public class TraceData
{
    public string TraceId { get; set; } = "";
    public List<Span> Spans { get; set; } = new();
}

public class Span
{
    public string Name { get; set; } = "";
    public int DurationMs { get; set; }
    public Dictionary<string, string> Attributes { get; set; } = new();
}
