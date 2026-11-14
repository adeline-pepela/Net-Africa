# Quick Start Guide - 5 Minute Setup

## Prerequisites
- .NET 8.0 SDK or later
- Windows, Mac, or Linux
- ~100MB disk space
- Administrator access (for port binding, if needed)

## Installation (2 minutes)

```bash
# Navigate to demo folder
cd "C:\Users\user\Downloads\Net Africa\Demo"

# Restore dependencies (required once)
dotnet restore

# Verify setup
dotnet --version
```

## Running the Demo (1 minute)

```bash
# Run the application
dotnet run

# You should see the menu:
╔════════════════════════════════════════════════════════════╗
║  Continuous Quality Monitoring for .NET AI Agents          ║
║  Using Amazon Bedrock AgentCore Evaluations               ║
║  60-Minute Working Demo                                    ║
╚════════════════════════════════════════════════════════════╝

Select Demo Mode:
  1. Interactive Chat (Stage 1 - Local Development)
  2. Batch Evaluation (Stages 2 & 3 - CI/CD + Production)
  3. Production Simulation (Stage 3 - Continuous Monitoring)
  4. View Recent Evaluations

Enter choice (1-4):
```

## Demo Scenarios (60 minutes total)

### Scenario 1: Interactive Chat (15 minutes)
**Time: 00:00 - 15:00**

**What to do:**
1. Select Mode 1 (Interactive Chat)
2. Type 5 customer support questions:
   ```
   I lost my password. How do I reset it?
   What's my current account balance?
   I was overcharged. Can you help?
   How do I update my billing address?
   Is my order still being processed?
   ```
3. Observe the responses and OpenTelemetry traces
4. Note execution times (typically 300-500ms)
5. Exit by typing `exit`

**What to explain:**
- "Each query generates OpenTelemetry spans capturing the entire execution"
- "Tools (SearchKnowledgeBase, GetCustomerHistory, CreateTicket) are traced"
- "This is Stage 1: Local Development - immediate feedback to developer"
- "Traces would be exported to Bedrock for evaluation in production"

**Output:**
```
You: I lost my password. How do I reset it?

Agent: You can reset your password by going to the login page, 
clicking 'Forgot Password', and following the email instructions...

Tools Used: SearchKnowledgeBase
Execution Time: 427ms

OpenTelemetry Trace Captured:
  ├─ Span: agent.run [duration: 427ms]
  │  ├─ llm.call.understand
  │  ├─ agent.tool_use [tool: SearchKnowledgeBase]
  │  └─ llm.call.format
  └─ Status: Ok

Quick Evaluation (local):
  Correctness: 92% | Tool Accuracy: 95%
```

---

### Scenario 2: Batch Evaluation (20 minutes)
**Time: 15:00 - 35:00**

**What to do:**
1. Select Mode 2 (Batch Evaluation)
2. Watch it automatically evaluate 5 test conversations
3. Observe the quality gate checking
4. See pass/fail results

**What to explain:**
- "This is Stage 2: CI/CD Pipeline - runs on every PR"
- "Same evaluation logic as production, but on test data"
- "Quality gates prevent bad changes from merging"
- "Each metric has a threshold:"
  - Correctness: ≥ 85%
  - Tool Accuracy: ≥ 90%
  - Helpfulness: ≥ 80%
- "If ANY gate fails, PR is blocked"
- "Developer gets immediate feedback"

**Expected Output:**
```
========================================================
MODE 2: BATCH EVALUATION - Stages 2 & 3 (CI/CD + Production)
========================================================

[1/5] Evaluating: "I lost my password..." ✓
    Correctness: 92%, Tool Accuracy: 95%
[2/5] Evaluating: "What's my current balance?" ✓
    Correctness: 88%, Tool Accuracy: 92%
[3/5] Evaluating: "I was overcharged..." ✓
    Correctness: 85%, Tool Accuracy: 90%
[4/5] Evaluating: "How do I update billing?" ✓
    Correctness: 91%, Tool Accuracy: 93%
[5/5] Evaluating: "Is my order processing?" ✓
    Correctness: 87%, Tool Accuracy: 91%

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

✓ ALL QUALITY GATES PASSED - Ready to merge!
```

**Talking Points:**
- "Without this gate, a bad prompt change could ship to production"
- "That would result in support tickets and lost revenue"
- "With automated evaluation, we catch it in 2 minutes"
- "Cost: ~$0.15 for 5 evaluations"
- "Cost of prevented incident: ~$10,000"
- "ROI: 67x return on investment"

---

### Scenario 3: Production Simulation (20 minutes)
**Time: 35:00 - 55:00**

**What to do:**
1. Select Mode 3 (Production Simulation)
2. Watch it simulate 40 production requests
3. Notice the 10% sampling (only 4 get evaluated)
4. Watch for alert when drift is detected
5. Review metrics at the end

**What to explain:**
- "This is Stage 3: Production Monitoring"
- "Real-world traffic patterns and edge cases"
- "10% sampling = 90% cost reduction vs 100% evaluation"
- "Still sufficient for trend detection"
- "Alert triggered when score drops >2%"
- "On-call engineer responds within 5 minutes"

**Expected Output:**
```
========================================================
MODE 3: PRODUCTION SIMULATION - Stage 3 (Continuous Monitoring)
========================================================

Simulating 40 production requests with 10% evaluation sampling...

[1/40] Not sampled: "I lost my password" (90% sampling)
[2/40] Not sampled: "Account balance" (90% sampling)
[3/40] Evaluated: "Billing issue" → Correctness: 88%
[4/40] Not sampled: "Update address" (90% sampling)
[5/40] Evaluated: "Track order" → Correctness: 91%
...
[35/40] Evaluated: "Check status" → Correctness: 0.84
     ⚠️  ALERT: Correctness dropped to 84% (baseline: 89%)

============================================================
PRODUCTION MONITORING SUMMARY
============================================================
Requests Processed: 40
Evaluations Run: 4 (10%)
Cost Estimate: $0.12 (at $0.03/evaluation)

Correctness Metrics:
  Current: 84%
  7-run avg: 87%
  Range: 82% - 93%

Tool Accuracy Metrics:
  Current: 89%
  7-run avg: 91%

✓ Metrics saved to metrics/prod-monitoring.json
```

**Talking Points:**
- "Notice the alert triggered automatically"
- "On-call engineer gets Slack notification"
- "Dashboard shows the dip clearly"
- "Investigation: Check recent deployments"
- "Found: New prompt version causes correctness to drop"
- "Action: Rollback or hotfix"
- "Time to detection: <5 minutes"
- "Time to resolution: ~10 minutes"
- "Impact: Zero support tickets"

---

### Scenario 4: Review Results (5 minutes)
**Time: 55:00 - 60:00**

**What to do:**
1. Select Mode 4 (View Recent Evaluations)
2. Show the saved JSON metrics

**What to explain:**
- "This data would feed into your dashboard"
- "Grafana, CloudWatch, or custom dashboards"
- "Historical trending helps identify patterns"
- "Export to BI tools (Tableau, Power BI) for business metrics"

**Example Dashboard Metrics:**
```
24-Hour Correctness Trend: 89% (Baseline: 89%, Change: 0%)
24-Hour Tool Accuracy: 92% (Baseline: 91%, Change: +1%)
24-Hour Helpfulness: 86% (Baseline: 85%, Change: +1%)
24-Hour Cost: $2.70 (at 10% sampling, ~90 evaluations)
Baseline Cost Prevention: Prevented 2 incidents = $20,000 saved
```

---

## Files Generated

After running all scenarios, you'll have:

```
traces/
  └─ interactive.json         # Interactive chat traces

metrics/
  ├─ evaluations.json         # Batch evaluation results
  └─ prod-monitoring.json     # Production monitoring metrics
```

## What Each Mode Demonstrates

| Mode | Stage | Focus | Use Case |
|------|-------|-------|----------|
| 1 | Local Dev | Interactive testing | Developer iteration |
| 2 | CI/CD | Objective gates | PR validation |
| 3 | Production | Continuous monitoring | Drift detection |

## Common Questions During Demo

**Q: Why not evaluate 100% of traffic?**
A: Cost vs benefit trade-off. 10% sampling is statistically sufficient and costs 90% less.

**Q: What if Bedrock evaluation is wrong?**
A: Spot-check results weekly. Claude is good but not perfect. Add custom evaluators for your domain.

**Q: Can I use this with other LLMs?**
A: Yes! OpenTelemetry is framework-agnostic. Works with Claude, GPT-4, Cohere, local models, etc.

**Q: How do I get started with my own agent?**
A: Follow the 4-week implementation checklist in the README. Start with Week 1 (instrumentation).

**Q: What's the ROI?**
A: Prevents 1-2 incidents per year = $18K-36K savings. Costs ~$2K/year. 9-18x return.

**Q: Can I customize thresholds?**
A: Yes! Edit `appsettings.json` to adjust thresholds for your use case.

---

## Timing Checklist

Use this to stay on track during the 60-minute demo:

```
00:00 - Start (Menu)
00:05 - Explain three-stage pattern
00:15 - Mode 1 complete (Interactive Chat)
00:20 - Explain CI/CD gates
00:35 - Mode 2 complete (Batch Evaluation)
00:40 - Explain production monitoring
00:55 - Mode 3 complete (Production Simulation)
00:58 - Mode 4 (Show results)
01:00 - Q&A
```

## Troubleshooting

**Error: "dotnet: not found"**
```
Install .NET 8 SDK from https://dotnet.microsoft.com/download
```

**Error: "Building..." takes too long**
```
Normal first time: ~10-15 seconds
Subsequent runs: <1 second (cached)
```

**Error: "No output files"**
```
mkdir traces
mkdir metrics
# Directories are auto-created, but you can create manually
```

**Slow simulations**
```
Each conversation: ~200-500ms (simulating API latency)
Batch mode (5 conversations): ~5 seconds total
Production sim (40 requests): ~10-15 seconds total
This is intentional (simulates real Bedrock latency)
```

---

## Success Criteria

After the demo, attendees should understand:

- ✓ Three-stage quality monitoring pattern
- ✓ How OpenTelemetry traces work
- ✓ How evaluation scores are generated
- ✓ Quality gate logic (thresholds)
- ✓ Cost-benefit analysis
- ✓ Implementation roadmap
- ✓ How to extend for their own agents

If all checked, the demo was successful!

---

**Ready?** Run `dotnet run` and select Mode 1 to start!
