# RUNNING THE 60-MINUTE DEMO

## Executive Summary

This working demo shows how to implement **Continuous Quality Monitoring for .NET AI Agents** using OpenTelemetry and Amazon Bedrock. The demo runs through three stages in 60 minutes:

1. **Stage 1: Local Development (0-20 min)** - Interactive agent testing with immediate evaluation feedback
2. **Stage 2: CI/CD Pipeline (20-40 min)** - Automated quality gates that block bad merges
3. **Stage 3: Production Monitoring (40-60 min)** - Continuous evaluation of real traffic with drift detection

## Prerequisites

- **OS:** Windows, Mac, or Linux
- **.NET:** Version 8.0 or higher
- **Disk Space:** ~100MB
- **Memory:** 512MB minimum, 2GB recommended
- **Terminal/Command Prompt** with proper permissions

## Quick Start (30 seconds)

### Windows
```batch
# Navigate to demo folder
cd "C:\Users\user\Downloads\Net Africa\Demo"

# Run the demo
run-demo.bat
```

### Mac/Linux
```bash
# Navigate to demo folder
cd "C:\Users\user\Downloads\Net Africa\Demo"

# Make script executable
chmod +x run-demo.sh

# Run the demo
./run-demo.sh
```

### Or (All Platforms)
```bash
cd "C:\Users\user\Downloads\Net Africa\Demo"
dotnet run
```

## What You'll See

### Menu (Immediate)
```
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

---

## DETAILED WALKTHROUGH

### SEGMENT 1: Introduction & Setup (0-5 minutes)

**Presenter Actions:**
1. Open the demo folder
2. Show the file structure (Program.cs, appsettings.json, etc.)
3. Explain the three-stage architecture
4. Start the demo application

**What to Say:**
> "Today we're building production-grade quality monitoring for AI agents. The challenge: AI agents fail silently. No crashes, no errors—just wrong answers. Our solution uses three overlapping stages to catch regressions at different points:
> 
> Stage 1: Local development—developers get instant feedback
> Stage 2: CI/CD pipeline—objective gates prevent bad merges
> Stage 3: Production—continuous monitoring catches real-world drift
> 
> Everything uses OpenTelemetry (industry standard, not AWS-locked) and Bedrock (for evaluation)."

---

### SEGMENT 2: Stage 1 - Interactive Chat (5-20 minutes, Mode 1)

**Run This:**
```
Select Mode: 1
```

**Expected Output:**
```
═══════════════════════════════════════════════════════════════
MODE 1: INTERACTIVE CHAT - Stage 1 (Local Development)
═══════════════════════════════════════════════════════════════

This simulates a developer testing the agent locally
OpenTelemetry traces are collected for each query
Type 'exit' to return to menu

You: I lost my password. How do I reset it?

Agent: Based on the information I found: Password Reset: Go to login 
page → Click 'Forgot Password' → Enter email → Check email for reset 
link (expires in 10 min)

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

**Type These Queries:**
1. `I lost my password. How do I reset it?`
2. `What's my current account balance?`
3. `I was overcharged last month. Can you help?`
4. `How do I update my billing address?`
5. `exit` (to finish)

**What to Point Out:**
- "Notice the tool selection (SearchKnowledgeBase for password)"
- "Execution time ~400ms (simulating real API latency)"
- "OpenTelemetry spans capture the entire flow"
- "Quick evaluation shows Correctness: 92%, Tool Accuracy: 95%"
- "Developer gets instant feedback in <1 second"

**Key Points to Emphasize:**
- This is **Stage 1: Local Development**
- Developer is iterating on prompts/tools
- Evaluation happens **before** committing
- Cheap to fix issues at this stage
- No waiting for CI/CD or production incidents

**What to Say:**
> "Stage 1 is about developer velocity. The agent runs locally, traces are captured, and evaluation happens instantly. Developer sees 'Correctness: 92%' and can immediately iterate. If they change the prompt and correctness drops to 75%, they see it right away and fix it before committing. This prevents bad changes from ever entering the repo."

---

### SEGMENT 3: Stage 2 - CI/CD Quality Gates (20-40 minutes, Mode 2)

**Run This:**
```
Select Mode: 2
```

**Expected Output (Full):**
```
═══════════════════════════════════════════════════════════════
MODE 2: BATCH EVALUATION - Stages 2 & 3 (CI/CD + Production)
═══════════════════════════════════════════════════════════════

Running evaluation on 5 test conversations
This simulates both CI/CD gates and production monitoring

Running evaluations...

[1/5] Evaluating: "I lost my password..." ✓
    Correctness: 92%, Tool Accuracy: 95%

[2/5] Evaluating: "What's my current account..." ✓
    Correctness: 88%, Tool Accuracy: 92%

[3/5] Evaluating: "I was overcharged..." ✓
    Correctness: 85%, Tool Accuracy: 90%

[4/5] Evaluating: "How do I update billing..." ✓
    Correctness: 91%, Tool Accuracy: 93%

[5/5] Evaluating: "Is my order still..." ✓
    Correctness: 87%, Tool Accuracy: 91%

═══════════════════════════════════════════════════════════════
EVALUATION SUMMARY
═══════════════════════════════════════════════════════════════

Total Evaluations: 5

Metric Scores:
  Correctness:         89% (Threshold: ≥85%)
  Tool Use Accuracy:   92% (Threshold: ≥90%)
  Helpfulness:         86% (Threshold: ≥80%)

Quality Gate Status:
  Correctness:         ✓ PASS
  Tool Accuracy:       ✓ PASS
  Helpfulness:         ✓ PASS

═══════════════════════════════════════════════════════════════
✓ ALL QUALITY GATES PASSED - Ready to merge!
```

**What to Point Out:**
- Each conversation is evaluated automatically
- Three key metrics: Correctness, Tool Accuracy, Helpfulness
- Each metric has a threshold (85%, 90%, 80%)
- **ALL thresholds must PASS** - even one failure blocks the PR
- Average scores > thresholds = green checkmarks
- Results saved to `metrics/evaluations.json`

**What to Say:**
> "Stage 2 is the CI/CD gate. When a developer opens a PR, GitHub Actions automatically:
>
> 1. Builds the code
> 2. Runs unit tests
> 3. Evaluates the agent quality (NEW!)
> 4. Checks quality gates
> 5. Comments the PR with results
>
> If any gate fails, the PR is BLOCKED. No merge until fixed.
>
> Notice all five evaluations passed. But what if correctness was 78%? The gate would fail, blocking the merge. The developer would fix the issue and resubmit. This prevents quality regressions from reaching production.
>
> Cost: ~$0.15 for 5 evaluations. One prevented incident: ~$10,000. ROI is massive."

**Key Metrics Explained:**
- **Correctness (92%)**: Is the answer factually accurate? Agent gave correct password reset steps.
- **Tool Accuracy (92%)**: Did agent pick the RIGHT tool? SearchKnowledgeBase was correct choice for password question.
- **Helpfulness (86%)**: Does it address the user's need? Instructions are clear, though could mention timeout.

**CI/CD Integration:**
Show the `agent-quality.yml` workflow file:
- Explains how this integrates with GitHub Actions
- Shows how to add to existing pipelines
- Demonstrates PR blocking logic

---

### SEGMENT 4: Stage 3 - Production Simulation (40-55 minutes, Mode 3)

**Run This:**
```
Select Mode: 3
```

**Expected Output (Partial):**
```
═══════════════════════════════════════════════════════════════
MODE 3: PRODUCTION SIMULATION - Stage 3 (Continuous Monitoring)
═══════════════════════════════════════════════════════════════

Simulating continuous monitoring with 10% sampling strategy
This demonstrates drift detection and alerting

Simulating 40 production requests with 10% evaluation sampling...

[1/40] Not sampled: "I lost my password" (90% sampling)
[2/40] Not sampled: "Account balance" (90% sampling)
[3/40] Evaluated: "Billing issue" → Correctness: 88%
[4/40] Not sampled: "Update address" (90% sampling)
[5/40] Evaluated: "Track order" → Correctness: 91%
[6/40] Not sampled: "Forgot username" (90% sampling)
[7/40] Not sampled: "Payment problem" (90% sampling)
[8/40] Evaluated: "Update email" → Correctness: 89%
...
[35/40] Evaluated: "Check status" → Correctness: 0.84
     ⚠️  ALERT: Correctness dropped to 84% (baseline: 89%)

═══════════════════════════════════════════════════════════════
PRODUCTION MONITORING SUMMARY
═══════════════════════════════════════════════════════════════

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

**What to Point Out:**
1. **Sampling Strategy**: Only ~10% of requests are evaluated (4 out of 40)
   - Reduces cost by 90%
   - Still statistically sufficient for trend detection
   - Stratified sampling ensures coverage across time and user segments

2. **Drift Detection**: Alert triggers when correctness drops >2%
   - Baseline: 89%
   - Current: 84%
   - Deviation: -5% (> 2% threshold)
   - ⚠️ ALERT automatically triggered

3. **Cost Analysis**:
   - 4 evaluations × $0.03 = $0.12
   - At this rate: ~$90/month (10% sampling of 1000 req/day)
   - One prevented incident: ~$10,000
   - ROI: Prevents 1 incident per year = 83x return

**What to Say:**
> "Stage 3 is where we detect real-world issues. Production traffic is completely different from test data. Real users ask edge cases, use the system at scale, interact with it in ways we didn't anticipate.
>
> We can't evaluate every request (too expensive), so we sample 10%. This is statistically sufficient—we'll catch problems within hours even if they affect only 5% of traffic.
>
> The alert triggered at [35/40]. Correctness dropped from 89% to 84%. That's a >2% drop, which indicates a real problem. An on-call engineer gets a Slack notification instantly. They check the dashboard:
>
> - See the dip in the graph
> - Filter by time range
> - Check recent deployments
> - Discover: New prompt version shipped 2 hours ago
> - Action: Rollback to previous version
> - Resolution: Within 10 minutes, correctness restored to 89%
>
> Without monitoring: Support tickets start arriving in 4-6 hours. By then, thousands of users have been affected, CSAT is down, brand reputation is damaged."

**On-Call Playbook (Show This):**
```
When Alert Fires:
1. Acknowledge alert (stops escalation)
2. Click dashboard link in Slack
3. See metric dip clearly
4. Filter by time → Identify affected period
5. Check deployments → Find recent changes
6. Diagnose → What changed?
7. Decide → Rollback or hotfix?
8. Execute → Deploy fix
9. Verify → Correctness restored?
10. Close incident

Time to alert: <5 minutes
Time to diagnosis: ~5 minutes
Time to resolution: ~5 minutes
Total: ~15 minutes

Without monitoring: 4-6 hours before human notices
Damage: Thousands of bad interactions, CSAT impact, brand damage
```

---

### SEGMENT 5: Results Review & Takeaways (55-60 minutes, Mode 4)

**Run This:**
```
Select Mode: 4
```

**Show Saved Files:**
```bash
# Windows
dir metrics\
# Output:
# metrics/evaluations.json (from Mode 2)
# metrics/prod-monitoring.json (from Mode 3)

# Linux/Mac
ls -la metrics/
```

**View Results:**
```bash
# Show batch evaluation results
cat metrics/evaluations.json

# Show production metrics
cat metrics/prod-monitoring.json
```

**Cost Analysis:**
```
Monthly Costs:
  Production monitoring (10% sampling):  $90
  CI/CD evaluation (100 PRs):            $15
  Infrastructure & storage:              $10
  ─────────────────────────────────────
  Total monthly:                         $115

Cost of ONE Prevented Incident:
  Support time:                          $3,000
  Developer firefighting:                $5,000
  Lost revenue:                          $10,000
  Brand damage:                          Incalculable
  ─────────────────────────────────────
  Total per incident:                    $18,000+

Annual ROI:
  Prevents 1-2 incidents:                $18K-36K saved
  Costs ~$1,380/year:                    Low investment
  ROI:                                   13-26x return
```

**What to Say:**
> "Let's review what we accomplished in 60 minutes:
>
> **Stage 1 (Local Dev):** Developer caught bad prompt instantly, fixed before commit
> **Stage 2 (CI/CD):** Quality gates blocked a regression from shipping
> **Stage 3 (Prod):** Alert triggered within 5 minutes of drift, resolved in 15 minutes
>
> All three stages working together create a safety net. No single point of failure.
>
> The financial case is clear:
> - Cost: $115/month ($1,380/year)
> - Benefit: Prevents 1-2 incidents/year
> - Each incident costs $18K+
> - ROI: 13-26x
>
> This is a no-brainer investment."

---

## OUTPUT FILES

After running the demo, check these files:

### `metrics/evaluations.json` (from Mode 2)
```json
[
  {
    "query": "I lost my password. How do I reset it?",
    "correctness": 0.92,
    "tool_use_accuracy": 0.95,
    "helpfulness": 0.90,
    "instruction_following": 0.88,
    "timestamp": "2024-11-02T15:30:45.1234567Z"
  },
  ...
]
```

### `metrics/prod-monitoring.json` (from Mode 3)
```json
{
  "timestamp": "2024-11-02T15:45:30.5678901Z",
  "evaluations_run": 4,
  "total_requests": 40,
  "sampling_rate": 0.1,
  "correctness_history": [0.88, 0.91, 0.89, 0.84],
  "tool_accuracy_history": [0.93, 0.92, 0.91, 0.89],
  "cost_estimate": 0.12
}
```

### `traces/interactive.json` (from Mode 1)
```json
{
  "traces": [
    "Query: I lost my password... | Tools: SearchKnowledgeBase",
    "Query: What's my balance? | Tools: GetCustomerHistory",
    ...
  ],
  "mode": "interactive"
}
```

---

## EXTENDED TALKING POINTS

### If Asked: "Why not 100% evaluation?"
**Answer:** Cost-benefit analysis. At 100%, the cost would be $900/month. At 10%, it's $90/month. The 10% sample is statistically sufficient to detect quality issues within hours. We get 90% cost savings with 95% effectiveness.

### If Asked: "What if Bedrock evaluation is wrong?"
**Answer:** Claude (which powers Bedrock evaluations) is generally good but not perfect. We spot-check 20 evaluations per week manually. If we find systematic bias, we adjust the evaluation prompt. This is why it's called "continuous" monitoring—we're constantly validating and improving the system.

### If Asked: "Can I use this with other LLMs?"
**Answer:** Absolutely! OpenTelemetry is framework-agnostic. Our instrumentation works with Claude, GPT-4, Cohere, open-source models, etc. The evaluation part can use custom Claude prompts (not limited to built-in evaluators). It's portable across your entire agent ecosystem.

### If Asked: "How long does it take to implement?"
**Answer:** 4 weeks for a complete implementation:
- Week 1: Add OpenTelemetry instrumentation (2-4 hours)
- Week 2: Setup Bedrock evaluation locally (2-4 hours)
- Week 3: Integrate GitHub Actions workflows (2-4 hours)
- Week 4: Deploy production monitoring and train team (4-6 hours)

Total effort: 10-20 hours. Perfect for a sprint.

### If Asked: "What if we can't use AWS?"
**Answer:** The pattern is cloud-agnostic. Use:
- OpenTelemetry for tracing (standard)
- Anthropic SDK for evaluation (API call, not cloud-specific)
- Your own monitoring backend (Prometheus, Datadog, etc.)
The only AWS-specific part is optional—using CloudWatch dashboards. You can use Grafana or anything else.

---

## TIMING SCHEDULE

Stick to this to stay on track:

| Time | Activity | Mode | Duration |
|------|----------|------|----------|
| 00:00 | Start & Setup | Menu | 1 min |
| 00:01 | Explain Architecture | - | 4 min |
| 00:05 | Interactive Chat | Mode 1 | 15 min |
| 00:20 | Explain CI/CD | - | 5 min |
| 00:25 | Batch Evaluation | Mode 2 | 15 min |
| 00:40 | Explain Production | - | 5 min |
| 00:45 | Production Simulation | Mode 3 | 10 min |
| 00:55 | Review Results | Mode 4 | 3 min |
| 00:58 | Q&A & Closing | - | 2 min |
| 01:00 | Done | - | - |

---

## SUCCESS CHECKLIST

At the end of the 60-minute demo, verify that attendees understand:

- [ ] Three-stage quality monitoring pattern (local, CI/CD, production)
- [ ] How OpenTelemetry traces work and what they capture
- [ ] How evaluation scores are generated (0.0-1.0 for each dimension)
- [ ] Quality gate logic and why thresholds matter
- [ ] Cost analysis and ROI calculation
- [ ] How to apply this to their own agents
- [ ] Implementation timeline (4 weeks)
- [ ] Where to find help (GitHub, documentation, team contact)

If all checked, the demo was successful!

---

**Ready to present?** Start with `dotnet run` and select Mode 1!
