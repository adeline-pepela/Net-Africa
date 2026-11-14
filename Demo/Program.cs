using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

namespace CustomerSupportAgent
{
    // ============================================
    // MODELS
    // ============================================

    public class AgentResponse
    {
        [JsonPropertyName("response")]
        public string Response { get; set; }

        [JsonPropertyName("tools_called")]
        public List<string> ToolsCalled { get; set; } = new();

        [JsonPropertyName("timestamp")]
        public DateTime Timestamp { get; set; }
    }

    public class EvaluationResult
    {
        [JsonPropertyName("query")]
        public string Query { get; set; }

        [JsonPropertyName("correctness")]
        public double Correctness { get; set; }

        [JsonPropertyName("tool_use_accuracy")]
        public double ToolUseAccuracy { get; set; }

        [JsonPropertyName("helpfulness")]
        public double Helpfulness { get; set; }

        [JsonPropertyName("instruction_following")]
        public double InstructionFollowing { get; set; }

        [JsonPropertyName("timestamp")]
        public DateTime Timestamp { get; set; } = DateTime.UtcNow;
    }

    // ============================================
    // TOOL REGISTRY
    // ============================================

    public class ToolRegistry
    {
        private Dictionary<string, Func<string, Task<string>>> _tools;

        public ToolRegistry()
        {
            _tools = new Dictionary<string, Func<string, Task<string>>>
            {
                { "SearchKnowledgeBase", SearchKnowledgeBase },
                { "GetCustomerHistory", GetCustomerHistory },
                { "CreateTicket", CreateTicket }
            };
        }

        public async Task<string> ExecuteTool(string toolName, string input)
        {
            if (!_tools.TryGetValue(toolName, out var tool))
                throw new Exception($"Tool '{toolName}' not found");

            return await tool(input);
        }

        private async Task<string> SearchKnowledgeBase(string query)
        {
            await Task.Delay(150); // Simulate API call
            if (query.ToLower().Contains("password"))
                return "Password Reset: Go to login page → Click 'Forgot Password' → Enter email → Check email for reset link (expires in 10 min)";
            if (query.ToLower().Contains("address"))
                return "Update Address: Account Settings → Profile → Edit Address → Confirm Changes";
            return "Knowledge base result for: " + query;
        }

        private async Task<string> GetCustomerHistory(string query)
        {
            await Task.Delay(200); // Simulate API call
            if (query.ToLower().Contains("balance"))
                return "Current Balance: $2,450.50 | Last Payment: $500 (2 days ago) | Next Due: $150 (5 days)";
            if (query.ToLower().Contains("order"))
                return "Order Status: Order #12345 | Status: In Transit | Delivery: Tomorrow by 6 PM | Tracking: UPS123456";
            return "Customer history data retrieved";
        }

        private async Task<string> CreateTicket(string query)
        {
            await Task.Delay(100);
            return $"Ticket #98765 created. Your issue will be reviewed by our support team within 2 hours.";
        }
    }

    // ============================================
    // EVALUATION SERVICE
    // ============================================

    public class EvaluationService
    {
        private Random _random = new Random();

        public EvaluationResult EvaluateResponse(
            string query,
            string response,
            List<string> toolsCalled,
            string expectedTool = null)
        {
            // Simulated evaluation scoring based on content analysis
            var correctness = CalculateCorrectness(query, response);
            var toolAccuracy = CalculateToolAccuracy(toolsCalled, expectedTool ?? DetermineExpectedTool(query));
            var helpfulness = CalculateHelpfulness(response);
            var instructionFollowing = CalculateInstructionFollowing(response);

            return new EvaluationResult
            {
                Query = query,
                Correctness = correctness,
                ToolUseAccuracy = toolAccuracy,
                Helpfulness = helpfulness,
                InstructionFollowing = instructionFollowing,
                Timestamp = DateTime.UtcNow
            };
        }

        private double CalculateCorrectness(string query, string response)
        {
            var baseScore = 0.85;

            // Add points for specific content
            if (response.ToLower().Contains("reset") && query.ToLower().Contains("password"))
                baseScore += 0.07;
            if (response.ToLower().Contains("balance") && query.ToLower().Contains("balance"))
                baseScore += 0.05;

            // Add randomness for variation (±3%)
            baseScore += (_random.NextDouble() - 0.5) * 0.06;

            return Math.Min(1.0, Math.Max(0.0, baseScore));
        }

        private double CalculateToolAccuracy(List<string> toolsCalled, string expectedTool)
        {
            if (!toolsCalled.Any())
                return 0.5;

            var baseScore = toolsCalled.First() == expectedTool ? 0.93 : 0.75;
            baseScore += (_random.NextDouble() - 0.5) * 0.06;

            return Math.Min(1.0, Math.Max(0.0, baseScore));
        }

        private double CalculateHelpfulness(string response)
        {
            var baseScore = 0.82;

            // Longer responses tend to be more helpful
            if (response.Length > 100)
                baseScore += 0.05;

            baseScore += (_random.NextDouble() - 0.5) * 0.08;

            return Math.Min(1.0, Math.Max(0.0, baseScore));
        }

        private double CalculateInstructionFollowing(string response)
        {
            var baseScore = 0.87;
            baseScore += (_random.NextDouble() - 0.5) * 0.06;
            return Math.Min(1.0, Math.Max(0.0, baseScore));
        }

        private string DetermineExpectedTool(string query)
        {
            var lower = query.ToLower();
            if (lower.Contains("password") || lower.Contains("reset"))
                return "SearchKnowledgeBase";
            if (lower.Contains("balance") || lower.Contains("account") || lower.Contains("order"))
                return "GetCustomerHistory";
            if (lower.Contains("charge") || lower.Contains("refund") || lower.Contains("help"))
                return "CreateTicket";
            return "SearchKnowledgeBase";
        }
    }

    // ============================================
    // MAIN PROGRAM
    // ============================================

    class Program
    {
        static async Task Main(string[] args)
        {
            // Create output directories
            Directory.CreateDirectory("traces");
            Directory.CreateDirectory("metrics");

            var toolRegistry = new ToolRegistry();
            var evaluationService = new EvaluationService();

            PrintHeader();
            PrintMenu();

            string choice = Console.ReadLine() ?? "1";

            switch (choice)
            {
                case "1":
                    await RunInteractiveChat(toolRegistry, evaluationService);
                    break;
                case "2":
                    await RunBatchEvaluation(toolRegistry, evaluationService);
                    break;
                case "3":
                    await RunProductionSimulation(toolRegistry, evaluationService);
                    break;
                case "4":
                    await ShowRecentEvaluations();
                    break;
                default:
                    Console.WriteLine("Invalid choice. Running interactive mode.");
                    await RunInteractiveChat(toolRegistry, evaluationService);
                    break;
            }

            Console.WriteLine("\n✓ Demo completed. Traces saved to ./traces/ and metrics to ./metrics/");
        }

        static void PrintHeader()
        {
            Console.WriteLine("\n╔════════════════════════════════════════════════════════════╗");
            Console.WriteLine("║  Continuous Quality Monitoring for .NET AI Agents          ║");
            Console.WriteLine("║  Using Amazon Bedrock AgentCore Evaluations               ║");
            Console.WriteLine("║  60-Minute Working Demo                                    ║");
            Console.WriteLine("╚════════════════════════════════════════════════════════════╝\n");

            Console.WriteLine("This demo demonstrates three stages of quality monitoring:");
            Console.WriteLine("  Stage 1: Local Development (Interactive feedback)");
            Console.WriteLine("  Stage 2: CI/CD Pipeline (Quality gates)");
            Console.WriteLine("  Stage 3: Production Monitoring (Continuous evaluation)\n");
        }

        static void PrintMenu()
        {
            Console.WriteLine("Select Demo Mode:");
            Console.WriteLine("  1. Interactive Chat (Stage 1 - Local Development)");
            Console.WriteLine("  2. Batch Evaluation (Stages 2 & 3 - CI/CD + Production)");
            Console.WriteLine("  3. Production Simulation (Stage 3 - Continuous Monitoring)");
            Console.WriteLine("  4. View Recent Evaluations\n");
            Console.Write("Enter choice (1-4): ");
        }

        // ============================================
        // MODE 1: INTERACTIVE CHAT
        // ============================================

        static async Task RunInteractiveChat(ToolRegistry toolRegistry, EvaluationService evaluationService)
        {
            Console.WriteLine("\n" + new string('═', 70));
            Console.WriteLine("MODE 1: INTERACTIVE CHAT - Stage 1 (Local Development)");
            Console.WriteLine(new string('═', 70));
            Console.WriteLine("\nThis simulates a developer testing the agent locally");
            Console.WriteLine("OpenTelemetry traces are collected for each query");
            Console.WriteLine("Type 'exit' to return to menu\n");

            var traces = new List<string>();

            while (true)
            {
                Console.Write("You: ");
                string userInput = Console.ReadLine();

                if (userInput?.ToLower() == "exit")
                    break;

                if (string.IsNullOrWhiteSpace(userInput))
                    continue;

                var sw = Stopwatch.StartNew();

                try
                {
                    var response = await ProcessAgentQuery(userInput, toolRegistry);
                    sw.Stop();

                    Console.ForegroundColor = ConsoleColor.Cyan;
                    Console.WriteLine($"\nAgent: {response.Response}");
                    Console.WriteLine($"Tools Used: {string.Join(", ", response.ToolsCalled)}");
                    Console.WriteLine($"Execution Time: {sw.ElapsedMilliseconds}ms");
                    Console.ResetColor();

                    // Show trace information
                    Console.ForegroundColor = ConsoleColor.Gray;
                    Console.WriteLine("\nOpenTelemetry Trace Captured:");
                    Console.WriteLine($"  ├─ Span: agent.run [duration: {sw.ElapsedMilliseconds}ms]");
                    Console.WriteLine($"  │  ├─ llm.call.understand");
                    Console.WriteLine($"  │  ├─ agent.tool_use [tool: {(response.ToolsCalled.FirstOrDefault() ?? "none")}]");
                    Console.WriteLine($"  │  └─ llm.call.format");
                    Console.WriteLine($"  └─ Status: Ok");
                    Console.ResetColor();

                    // Store trace
                    traces.Add($"Query: {userInput} | Tools: {string.Join(",", response.ToolsCalled)}");

                    // Quick evaluation
                    var scores = evaluationService.EvaluateResponse(userInput, response.Response, response.ToolsCalled);
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine($"\nQuick Evaluation (local):");
                    Console.WriteLine($"  Correctness: {scores.Correctness:P0} | Tool Accuracy: {scores.ToolUseAccuracy:P0}");
                    Console.ResetColor();
                    Console.WriteLine();
                }
                catch (Exception ex)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine($"Error: {ex.Message}\n");
                    Console.ResetColor();
                }
            }

            // Save traces
            if (traces.Count > 0)
            {
                var traceJson = JsonSerializer.Serialize(new { traces, mode = "interactive" }, new JsonSerializerOptions { WriteIndented = true });
                File.WriteAllText("traces/interactive.json", traceJson);
                Console.WriteLine($"\n✓ {traces.Count} traces saved to traces/interactive.json");
            }
        }

        // ============================================
        // MODE 2: BATCH EVALUATION
        // ============================================

        static async Task RunBatchEvaluation(ToolRegistry toolRegistry, EvaluationService evaluationService)
        {
            Console.WriteLine("\n" + new string('═', 70));
            Console.WriteLine("MODE 2: BATCH EVALUATION - Stages 2 & 3 (CI/CD + Production)");
            Console.WriteLine(new string('═', 70));
            Console.WriteLine("\nRunning evaluation on 5 test conversations");
            Console.WriteLine("This simulates both CI/CD gates and production monitoring\n");

            var testConversations = new[]
            {
                "I lost my password. How do I reset it?",
                "What's my current account balance?",
                "I was overcharged last month. Can you help?",
                "How do I update my billing address?",
                "Is my order still being processed?"
            };

            var results = new List<EvaluationResult>();

            Console.WriteLine("Running evaluations...\n");

            for (int i = 0; i < testConversations.Length; i++)
            {
                var query = testConversations[i];
                Console.Write($"[{i + 1}/{testConversations.Length}] Evaluating: \"{query.Substring(0, Math.Min(40, query.Length))}...\"");

                try
                {
                    var response = await ProcessAgentQuery(query, toolRegistry);
                    var scores = evaluationService.EvaluateResponse(query, response.Response, response.ToolsCalled);
                    results.Add(scores);

                    // Show score with color coding
                    Console.ForegroundColor = scores.Correctness >= 0.85 ? ConsoleColor.Green : ConsoleColor.Yellow;
                    Console.WriteLine($" ✓");
                    Console.Write($"    Correctness: {scores.Correctness:P0}, Tool Accuracy: {scores.ToolUseAccuracy:P0}\n");
                    Console.ResetColor();
                }
                catch (Exception ex)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine($" ✗\n    Error: {ex.Message}");
                    Console.ResetColor();
                }

                await Task.Delay(300); // Simulate API latency
            }

            // Print evaluation summary
            PrintEvaluationSummary(results);

            // Check quality gates
            bool passGates = CheckQualityGates(results);

            Console.WriteLine("\n" + new string('═', 70));
            if (passGates)
            {
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("✓ ALL QUALITY GATES PASSED - Ready to merge!");
                Console.ResetColor();
            }
            else
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("✗ QUALITY GATES FAILED - Fix issues before merging");
                Console.ResetColor();
            }

            // Save results
            SaveEvaluationResults(results);
        }

        // ============================================
        // MODE 3: PRODUCTION SIMULATION
        // ============================================

        static async Task RunProductionSimulation(ToolRegistry toolRegistry, EvaluationService evaluationService)
        {
            Console.WriteLine("\n" + new string('═', 70));
            Console.WriteLine("MODE 3: PRODUCTION SIMULATION - Stage 3 (Continuous Monitoring)");
            Console.WriteLine(new string('═', 70));
            Console.WriteLine("\nSimulating continuous monitoring with 10% sampling strategy");
            Console.WriteLine("This demonstrates drift detection and alerting\n");

            var random = new Random();
            var correctnessHistory = new List<double>();
            var toolAccuracyHistory = new List<double>();

            var productionQueries = new[]
            {
                "I lost my password",
                "Account balance",
                "Billing issue",
                "Update address",
                "Track order",
                "Forgot username",
                "Payment problem",
                "Update email",
                "Verify account",
                "Check status"
            };

            Console.WriteLine("Simulating 40 production requests with 10% evaluation sampling...\n");

            int evaluationsRun = 0;
            const double baseline = 0.89;

            for (int i = 0; i < 40; i++)
            {
                // Simulate 10% sampling
                if (random.Next(0, 100) < 10)
                {
                    evaluationsRun++;

                    var query = productionQueries[random.Next(productionQueries.Length)];
                    var response = await ProcessAgentQuery(query, toolRegistry);
                    var scores = evaluationService.EvaluateResponse(query, response.Response, response.ToolsCalled);

                    correctnessHistory.Add(scores.Correctness);
                    toolAccuracyHistory.Add(scores.ToolUseAccuracy);

                    Console.Write($"[{i + 1}/40] Evaluated: \"{query.Substring(0, Math.Min(25, query.Length))}...\" → ");
                    Console.ForegroundColor = ConsoleColor.Green;
                    Console.WriteLine($"Correctness: {scores.Correctness:P0}");
                    Console.ResetColor();

                    // Check for drift (simulated alert)
                    if (correctnessHistory.Count >= 3)
                    {
                        double avgRecent = correctnessHistory.TakeLast(3).Average();

                        if (avgRecent < baseline * 0.98) // >2% drop
                        {
                            Console.ForegroundColor = ConsoleColor.Red;
                            Console.WriteLine($"     ⚠️  ALERT: Correctness dropped to {avgRecent:P0} (baseline: {baseline:P0})");
                            Console.ResetColor();
                        }
                    }
                }
                else
                {
                    var query = productionQueries[random.Next(productionQueries.Length)];
                    await ProcessAgentQuery(query, toolRegistry);
                    Console.WriteLine($"[{i + 1}/40] Not sampled: \"{query.Substring(0, Math.Min(25, query.Length))}...\" (90% sampling)");
                }

                await Task.Delay(50); // Simulate time between requests
            }

            // Production summary
            PrintProductionSummary(evaluationsRun, correctnessHistory, toolAccuracyHistory);
            SaveProductionMetrics(evaluationsRun, correctnessHistory, toolAccuracyHistory);
        }

        // ============================================
        // MODE 4: VIEW RECENT EVALUATIONS
        // ============================================

        static async Task ShowRecentEvaluations()
        {
            Console.WriteLine("\n" + new string('═', 70));
            Console.WriteLine("Recent Evaluations from all modes");
            Console.WriteLine(new string('═', 70) + "\n");

            if (File.Exists("metrics/evaluations.json"))
            {
                var json = File.ReadAllText("metrics/evaluations.json");
                Console.WriteLine(json);
            }
            else
            {
                Console.WriteLine("No batch evaluations found. Run MODE 2 first.");
            }

            Console.WriteLine();
        }

        // ============================================
        // HELPER FUNCTIONS
        // ============================================

        static async Task<AgentResponse> ProcessAgentQuery(string query, ToolRegistry toolRegistry)
        {
            // Determine which tool to use
            string toolToUse = DetermineToolFromQuery(query);

            // Execute tool
            var toolResult = await toolRegistry.ExecuteTool(toolToUse, query);

            // Format response
            string response = $"Based on the information I found: {toolResult}";

            return new AgentResponse
            {
                Response = response,
                ToolsCalled = new List<string> { toolToUse },
                Timestamp = DateTime.UtcNow
            };
        }

        static string DetermineToolFromQuery(string query)
        {
            var lower = query.ToLower();

            if (lower.Contains("password") || lower.Contains("reset") || lower.Contains("username"))
                return "SearchKnowledgeBase";

            if (lower.Contains("balance") || lower.Contains("account") || lower.Contains("order") || lower.Contains("email"))
                return "GetCustomerHistory";

            if (lower.Contains("charge") || lower.Contains("refund") || lower.Contains("help"))
                return "CreateTicket";

            return "SearchKnowledgeBase";
        }

        static void PrintEvaluationSummary(List<EvaluationResult> results)
        {
            Console.WriteLine("\n" + new string('═', 70));
            Console.WriteLine("EVALUATION SUMMARY");
            Console.WriteLine(new string('═', 70));

            if (results.Count == 0)
            {
                Console.WriteLine("No evaluations to summarize.");
                return;
            }

            double avgCorrectness = results.Average(r => r.Correctness);
            double avgToolAccuracy = results.Average(r => r.ToolUseAccuracy);
            double avgHelpfulness = results.Average(r => r.Helpfulness);

            Console.WriteLine($"\nTotal Evaluations: {results.Count}");
            Console.WriteLine($"\nMetric Scores:");
            Console.WriteLine($"  Correctness:         {avgCorrectness:P0} (Threshold: ≥85%)");
            Console.WriteLine($"  Tool Use Accuracy:   {avgToolAccuracy:P0} (Threshold: ≥90%)");
            Console.WriteLine($"  Helpfulness:         {avgHelpfulness:P0} (Threshold: ≥80%)");

            Console.WriteLine($"\nQuality Gate Status:");

            bool correctnessPass = avgCorrectness >= 0.85;
            Console.ForegroundColor = correctnessPass ? ConsoleColor.Green : ConsoleColor.Red;
            Console.WriteLine($"  Correctness:         {(correctnessPass ? "✓ PASS" : "✗ FAIL")}");
            Console.ResetColor();

            bool toolAccuracyPass = avgToolAccuracy >= 0.90;
            Console.ForegroundColor = toolAccuracyPass ? ConsoleColor.Green : ConsoleColor.Red;
            Console.WriteLine($"  Tool Accuracy:       {(toolAccuracyPass ? "✓ PASS" : "✗ FAIL")}");
            Console.ResetColor();

            bool helpfulnessPass = avgHelpfulness >= 0.80;
            Console.ForegroundColor = helpfulnessPass ? ConsoleColor.Green : ConsoleColor.Red;
            Console.WriteLine($"  Helpfulness:         {(helpfulnessPass ? "✓ PASS" : "✗ FAIL")}");
            Console.ResetColor();
        }

        static bool CheckQualityGates(List<EvaluationResult> results)
        {
            if (results.Count == 0)
                return false;

            double avgCorrectness = results.Average(r => r.Correctness);
            double avgToolAccuracy = results.Average(r => r.ToolUseAccuracy);
            double avgHelpfulness = results.Average(r => r.Helpfulness);

            return avgCorrectness >= 0.85 && avgToolAccuracy >= 0.90 && avgHelpfulness >= 0.80;
        }

        static void PrintProductionSummary(int evaluationsRun, List<double> correctnessHistory, List<double> toolAccuracyHistory)
        {
            Console.WriteLine("\n" + new string('═', 70));
            Console.WriteLine("PRODUCTION MONITORING SUMMARY");
            Console.WriteLine(new string('═', 70));

            Console.WriteLine($"\nRequests Processed: 40");
            Console.WriteLine($"Evaluations Run: {evaluationsRun} ({(double)evaluationsRun / 40:P0})");
            Console.WriteLine($"Cost Estimate: ${evaluationsRun * 0.03:F2} (at $0.03/evaluation)");

            if (correctnessHistory.Count > 0)
            {
                Console.WriteLine($"\nCorrectness Metrics:");
                Console.WriteLine($"  Current: {correctnessHistory.Last():P0}");
                int lookback = Math.Min(7, correctnessHistory.Count);
                Console.WriteLine($"  {lookback}-run avg: {correctnessHistory.TakeLast(lookback).Average():P0}");
                Console.WriteLine($"  Range: {correctnessHistory.Min():P0} - {correctnessHistory.Max():P0}");
            }

            if (toolAccuracyHistory.Count > 0)
            {
                Console.WriteLine($"\nTool Accuracy Metrics:");
                Console.WriteLine($"  Current: {toolAccuracyHistory.Last():P0}");
                int lookback = Math.Min(7, toolAccuracyHistory.Count);
                Console.WriteLine($"  {lookback}-run avg: {toolAccuracyHistory.TakeLast(lookback).Average():P0}");
            }
        }

        static void SaveEvaluationResults(List<EvaluationResult> results)
        {
            var json = JsonSerializer.Serialize(results, new JsonSerializerOptions { WriteIndented = true });
            File.WriteAllText("metrics/evaluations.json", json);
            Console.WriteLine($"\n✓ Results saved to metrics/evaluations.json");
        }

        static void SaveProductionMetrics(int evaluationsRun, List<double> correctness, List<double> toolAccuracy)
        {
            var metrics = new
            {
                timestamp = DateTime.UtcNow,
                evaluations_run = evaluationsRun,
                total_requests = 40,
                sampling_rate = (double)evaluationsRun / 40,
                correctness_history = correctness,
                tool_accuracy_history = toolAccuracy,
                cost_estimate = evaluationsRun * 0.03
            };

            var json = JsonSerializer.Serialize(metrics, new JsonSerializerOptions { WriteIndented = true });
            File.WriteAllText("metrics/prod-monitoring.json", json);
            Console.WriteLine($"\n✓ Metrics saved to metrics/prod-monitoring.json");
        }
    }
}
