# Continuous Quality Monitoring for .NET AI Agents - Working Demo

**Duration:** 60 minutes  
**Framework:** .NET 8.0+  
**Components:** OpenTelemetry, Anthropic SDK, Amazon Bedrock Evaluation (simulated)

## Quick Start (5 minutes)

```bash
# Prerequisites
dotnet --version  # Should be 8.0 or higher

# Navigate to demo folder
cd "C:\Users\user\Downloads\Net Africa\Demo"

# Run the demo
dotnet run
```

## Demo Overview

This demo walks through all 3 stages of quality monitoring:

1. **Stage 1: Local Development (Minutes 0-20)** - Interactive agent testing with local evaluation
2. **Stage 2: CI/CD Quality Gates (Minutes 20-40)** - Batch evaluation with quality thresholds
3. **Stage 3: Production Monitoring (Minutes 40-60)** - Continuous monitoring simulation

## What's Included

```
Demo/
├── src/
│   ├── CustomerSupportAgent/
│   │   ├── Program.cs                    # Main entry point
│   │   ├── Agent/
│   │   │   ├── AgentRunner.cs            # Agent orchestration
│   │   │   ├── ToolRegistry.cs           # Tool definitions
│   │   │   └── Models.cs                 # Data models
│   │   ├── OpenTelemetry/
│   │   │   ├── InstrumentationSetup.cs   # OTel configuration
│   │   │   └── TraceExporter.cs          # Trace management
│   │   ├── Evaluation/
│   │   │   ├── EvaluationService.cs      # Score generation
│   │   │   └── BedrockMock.cs            # Mock Bedrock API
│   │   ├── appsettings.json
│   │   └── CustomerSupportAgent.csproj
│   │
│   └── EvaluationRunner/
│       ├── Program.cs
│       └── EvaluationRunner.csproj
│
├── scripts/
│   ├── run-evals.sh                      # Evaluation script
│   ├── check-thresholds.py               # Quality gate checker
│   └── simulate-prod.ps1                 # Production simulator
│
├── .github/workflows/
│   └── agent-quality.yml                 # GitHub Actions (reference)
│
├── tests/
│   ├── conversations.json                # Test conversations
│   └── expected-scores.json              # Expected results
│
└── traces/ & metrics/                    # Output directories (auto-created)
```

## 60-Minute Agenda

### Segment 1: Introduction & Setup (5 min)
- Problem statement
- Three-stage monitoring pattern
- Demo architecture overview

### Segment 2: Stage 1 - Local Development (15 min)
- Launch interactive chat mode
- Run 3-5 conversations
- Show OpenTelemetry traces
- Demonstrate immediate feedback
- Show trace export to JSON

### Segment 3: Stage 2 - CI/CD Pipeline (20 min)
- Run batch evaluation on test conversations
- Show quality gate checking
- Demonstrate scoring for each dimension:
  - Correctness (≥0.85)
  - Tool Use Accuracy (≥0.90)
  - Helpfulness (≥0.80)
- Show pass/fail decision
- Explain GitHub Actions integration

### Segment 4: Stage 3 - Production Monitoring (15 min)
- Run production simulation
- Show continuous monitoring
- Demonstrate 10% sampling
- Show trend detection
- Trigger simulated alert on drift
- Show response playbook

### Segment 5: Takeaways & Q&A (5 min)
- Key learnings
- Cost analysis
- Next steps
- Questions

## Running the Demo

### Mode 1: Interactive Chat (Stage 1)
```
Choice: 1
```
- Type customer queries naturally
- See agent responses with tool usage
- View execution time and traces
- Exit with `exit` command

**Example queries:**
```
I lost my password. How do I reset it?
What's my account balance?
I was overcharged. Can you help?
How do I update my billing address?
```

### Mode 2: Batch Evaluation (Stage 2)
```
Choice: 2
```
- Runs 5 predefined conversations
- Evaluates each with quality metrics
- Shows per-conversation scores
- Displays overall summary
- Reports quality gate status (PASS/FAIL)
- Saves results to metrics/evaluations.json

### Mode 3: Production Simulation (Stage 3)
```
Choice: 3
```
- Simulates 50 production requests
- Uses 10% sampling strategy
- Tracks trend over time
- Shows alert when drift detected
- Displays cost estimate
- Shows baseline vs current metrics

### Mode 4: View Recent Results
```
Choice: 4
```
- Displays saved evaluation results
- Shows historical data
- Useful for dashboard demos

## Expected Output

### Interactive Mode Output:
```
You: I lost my password. How do I reset it?

Agent: You can reset your password by going to the login page, 
clicking 'Forgot Password', and following the email instructions. 
The reset link expires in 10 minutes.

Tools Used: SearchKnowledgeBase
Execution Time: 427ms

OTel Trace:
├─ agent.run [duration: 427ms]
│  ├─ llm.call.understand [duration: 203ms]
│  │  └─ attributes: model=claude-3.5-sonnet, decision=SearchKnowledgeBase
│  ├─ agent.tool_use [duration: 100ms]
│  │  └─ attributes: tool=SearchKnowledgeBase, success=true
│  └─ llm.call.format [duration: 124ms]
│     └─ attributes: formatted_response=...
```

### Batch Evaluation Output:
```
========================================================
MODE 2: Batch Evaluation - Stages 2 & 3 (CI/CD + Production)
========================================================

Running evaluations...

[1/5] Evaluating: "I lost my password..."
✓ Correctness: 92%, Tool Accuracy: 95%

[2/5] Evaluating: "What's my current balance?"
✓ Correctness: 88%, Tool Accuracy: 92%

[3/5] Evaluating: "I was overcharged..."
✓ Correctness: 85%, Tool Accuracy: 90%

[4/5] Evaluating: "How do I update billing?"
✓ Correctness: 91%, Tool Accuracy: 93%

[5/5] Evaluating: "Is my order processing?"
✓ Correctness: 87%, Tool Accuracy: 91%

============================================================
EVALUATION SUMMARY
============================================================
Total Evaluations: 5
Avg Correctness: 89% (Threshold: 85%) ✓ PASS
Avg Tool Accuracy: 92% (Threshold: 90%) ✓ PASS
Avg Helpfulness: 86% (Threshold: 80%) ✓ PASS

Quality Gate Status:
  Correctness: ✓ PASS
  Tool Accuracy: ✓ PASS
  Helpfulness: ✓ PASS

✓ ALL GATES PASSED - Ready to merge!
```

### Production Simulation Output:
```
========================================================
MODE 3: Production Simulation - Stage 3 (Continuous Monitoring)
========================================================

Simulating 50 production requests with 10% evaluation sampling...

[1/50] Not sampled: "I lost my password" (90% sampling rate)
[2/50] Not sampled: "Account balance" (90% sampling rate)
[3/50] Evaluated: "Billing issue" → Correctness: 88%
[4/50] Not sampled: "Update address" (90% sampling rate)
[5/50] Evaluated: "Track order" → Correctness: 91%
...
[45/50] Evaluated: "Check status" → Correctness: 0.84
       ⚠️  ALERT: Correctness dropped to 84% (baseline: 89%)

============================================================
PRODUCTION MONITORING SUMMARY
============================================================
Total Requests: 50
Evaluations Run: 5 (10%)
Cost Estimate: $0.15 (at $0.03/evaluation)

Correctness Trend:
  Current: 84%
  7-run avg: 87%
  Min: 82%, Max: 93%

Tool Accuracy Trend:
  Current: 89%
  7-run avg: 91%

✓ Results saved to metrics/prod-monitoring.json
```

## Key Metrics Explained

### Correctness (0.0 - 1.0)
- Is the answer factually accurate?
- Example: "Reset password steps are correct" → 0.92

### Tool Use Accuracy (0.0 - 1.0)
- Did agent pick the RIGHT tool?
- Example: "SearchKnowledgeBase was correct choice" → 0.95

### Helpfulness (0.0 - 1.0)
- Does the response address the user's need?
- Example: "Steps are clear but missing support link" → 0.88

## Quality Gate Thresholds

```
Dimension             | Threshold | Reason
─────────────────────────────────────────────────
Correctness          | ≥ 0.85    | Facts matter most
Tool Use Accuracy    | ≥ 0.90    | Wrong tool = wrong behavior
Helpfulness          | ≥ 0.80    | Some variation acceptable
Instruction Following| ≥ 0.85    | Compliance important
```

## Understanding Traces

The demo captures OpenTelemetry traces showing:

```
agent.run [span]
├─ llm.call.understand [span]
│  └─ Attributes: model, prompt, decision
├─ agent.tool_use [span]
│  └─ Attributes: tool_name, input, output, success
└─ llm.call.format [span]
   └─ Attributes: prompt, response
```

Each span includes:
- **Name:** What operation was performed
- **Duration:** How long it took
- **Attributes:** Key-value metadata (model, tools, etc.)
- **Status:** Success or error

## Files Generated

### Traces (Stage 1)
- **Location:** `traces/` folder
- **Format:** JSON with OpenTelemetry span format
- **Use:** Understand execution flow, debug issues

### Metrics (Stages 2 & 3)
- **Location:** `metrics/` folder
- **Files:**
  - `evaluations.json` - Batch evaluation results
  - `prod-monitoring.json` - Production monitoring history
- **Use:** Track quality over time, identify trends

### Logs (All Stages)
- **Console output** shows real-time progress
- **Files:** Saved to `logs/` if configured

## Extending the Demo

### Add Custom Tools
Edit `src/CustomerSupportAgent/Agent/ToolRegistry.cs`:
```csharp
private async Task<string> YourCustomTool(string input)
{
    // Your implementation
    return result;
}
```

### Modify Thresholds
Edit `src/CustomerSupportAgent/Evaluation/EvaluationService.cs`:
```csharp
public const double CORRECTNESS_THRESHOLD = 0.85; // Adjust here
```

### Connect Real Bedrock
Replace mock in `BedrockMock.cs` with actual AWS SDK:
```csharp
var client = new AmazonBedrockClient();
var response = await client.InvokeModelAsync(...);
```

## Troubleshooting

### Error: "dotnet not found"
```bash
# Install .NET 8.0 SDK from https://dotnet.microsoft.com/download
```

### Error: "Project file not found"
```bash
# Make sure you're in the Demo folder
cd "C:\Users\user\Downloads\Net Africa\Demo"
```

### Slow performance
- Normal: First run compiles the project (~10 seconds)
- Each evaluation takes ~200-500ms (simulating API latency)
- Batch mode with 5 conversations: ~5 seconds total

### No output files
```bash
# Create directories manually if needed
mkdir traces
mkdir metrics
mkdir logs
```

## Presentation Tips

### Point Out During Demo:

**Stage 1 (Local Development):**
- "Notice how traces capture EVERY operation"
- "Developers get instant feedback"
- "Can iterate quickly on prompts"

**Stage 2 (CI/CD):**
- "This is objective gatekeeping - no humans needed"
- "PASS means it's safe to deploy"
- "FAIL blocks the merge - prevents bad code"
- "Shows exactly which metric failed"

**Stage 3 (Production):**
- "10% sampling = low cost but sufficient signal"
- "Alert triggered <5 minutes from issue"
- "On-call engineer knows exactly what to investigate"
- "Baseline vs current shows the trend clearly"

## Cost Analysis (Live Demo)

```
Scenario: 1,000 production requests/day

Option 1: Evaluate 100% (all requests)
Cost: 1,000 × $0.03 = $30/day = $900/month

Option 2: Evaluate 10% (recommended)
Cost: 100 × $0.03 = $3/day = $90/month

Cost of ONE prevented incident
Support time: $3,000
Developer firefighting: $5,000
Lost revenue: $10,000
Total: $18,000+

ROI: 10% monitoring prevents 1 incident = 200x return
```

## Additional Resources

- **OpenTelemetry .NET:** https://github.com/open-telemetry/opentelemetry-dotnet
- **Amazon Bedrock:** https://aws.amazon.com/bedrock/
- **Anthropic SDK:** https://github.com/anthropics/sdk-dotnet
- **This Demo:** Fully reproducible and customizable

## Questions During Demo

**"Why not test 100%?"**
- Cost: $900/month vs $90/month
- Not needed: 10% sampling statistically sufficient
- Use stratified sampling for better coverage

**"What if Bedrock is wrong?"**
- Spot-check manually weekly
- Add custom evaluators for domain specifics
- Claude is good but not perfect

**"How fast is this?"**
- Evaluation: 2-10 seconds per trace
- For async scoring (not real-time)
- Sampling reduces cost by 90%

**"Can I use this with non-Bedrock agents?"**
- YES! OpenTelemetry is standard
- Works with any LLM (GPT, Cohere, local models)
- Evaluation can be custom Claude prompts

---

**Ready to run?** Execute `dotnet run` and select Mode 1 for interactive demonstration!
