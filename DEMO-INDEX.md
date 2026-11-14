# Continuous Quality Monitoring for .NET AI Agents - Complete Demo Package

## 📋 Overview

This is a **complete, working 1-hour demo** for "Continuous Quality Monitoring for .NET AI Agents with Amazon Bedrock". The demo implements all three stages of quality monitoring and is ready to run immediately.

**Location:** `C:\Users\user\Downloads\Net Africa\Demo\`

**Language:** C# (.NET 8.0+)

**Duration:** 60 minutes

**What's Included:**
- ✓ Fully functional .NET customer support agent
- ✓ OpenTelemetry instrumentation (Stage 1)
- ✓ Quality evaluation and scoring (Stages 2 & 3)
- ✓ Simulated Bedrock evaluation (with mock data)
- ✓ Multiple demo modes (interactive, batch, production simulation)
- ✓ GitHub Actions workflow example
- ✓ Complete documentation and speaker notes
- ✓ Scripts for easy execution

---

## 📁 File Structure

```
Demo/
├── Program.cs                          # Main application (all demo logic)
├── CustomerSupportAgent.csproj        # Project file with NuGet dependencies
├── appsettings.json                   # Configuration (thresholds, settings)
├── agent-quality.yml                  # GitHub Actions workflow example
├── QUICK-START.md                     # 5-minute quick start guide
├── RUNNING-THE-DEMO.md                # Detailed 60-minute walkthrough
├── Demo-README.md                     # Complete documentation
├── run-demo.bat                       # Windows batch script
├── run-demo.sh                        # Linux/Mac bash script
├── traces/                            # (Created at runtime) OpenTelemetry traces
└── metrics/                           # (Created at runtime) Evaluation results
```

---

## 🚀 Quick Start (2 minutes)

### Option 1: Windows
```batch
cd "C:\Users\user\Downloads\Net Africa\Demo"
run-demo.bat
```

### Option 2: Linux/Mac
```bash
cd "C:\Users\user\Downloads\Net Africa\Demo"
chmod +x run-demo.sh
./run-demo.sh
```

### Option 3: All Platforms
```bash
cd "C:\Users\user\Downloads\Net Africa\Demo"
dotnet run
```

**First Run:** ~10-15 seconds (compilation)  
**Subsequent Runs:** ~1-2 seconds

---

## 📖 Documentation Files

### 1. **QUICK-START.md** - For Attendees (5 minutes)
- Minimal setup instructions
- Four demo scenarios explained
- Expected output for each mode
- Common questions answered

**Read this if:** You want the absolute minimum to understand and run the demo

### 2. **RUNNING-THE-DEMO.md** - For Presenters (Full details)
- Complete 60-minute walkthrough
- What to say at each point
- Expected output for every command
- Detailed explanation of each stage
- Talking points and extended answers
- Timing schedule to stay on track
- Success checklist

**Read this if:** You're presenting to an audience and need complete speaker notes

### 3. **Demo-README.md** - Reference Guide
- Architecture overview
- All four demo modes explained in detail
- Key metrics explained
- Quality gate thresholds
- Understanding traces
- Files generated
- Extending the demo
- Troubleshooting
- Cost analysis
- Additional resources

**Read this if:** You want to understand how the demo works and how to customize it

---

## 🎯 Demo Structure (60 minutes)

### Segment 1: Introduction & Setup (5 minutes)
- Show file structure
- Explain three-stage pattern
- Start the demo application

### Segment 2: Stage 1 - Interactive Chat (15 minutes) - **Mode 1**
- Demonstrate local agent testing
- Show OpenTelemetry traces
- Quick evaluation feedback
- Developer iteration workflow

**Choose:** `1`

### Segment 3: Stage 2 - Batch Evaluation (20 minutes) - **Mode 2**
- Demonstrate CI/CD quality gates
- Show evaluation on 5 test conversations
- Explain thresholds and pass/fail logic
- Show GitHub Actions integration

**Choose:** `2`

### Segment 4: Stage 3 - Production Simulation (15 minutes) - **Mode 3**
- Demonstrate continuous monitoring
- Show 10% sampling strategy
- Trigger alert on quality drift
- Show on-call response workflow

**Choose:** `3`

### Segment 5: Results & Takeaways (5 minutes) - **Mode 4**
- View saved evaluation results
- Discuss cost analysis and ROI
- Answer questions
- Next steps

**Choose:** `4`

---

## 🎮 Four Demo Modes

| Mode | Stage | Focus | Duration | Choose |
|------|-------|-------|----------|--------|
| 1 | Local Dev | Interactive testing with instant feedback | ~10 min | `1` |
| 2 | CI/CD | Batch evaluation with quality gates | ~10 min | `2` |
| 3 | Production | Continuous monitoring with drift detection | ~10 min | `3` |
| 4 | Analysis | View and analyze saved results | ~5 min | `4` |

---

## 📊 What Each Mode Demonstrates

### Mode 1: Interactive Chat
```
Developer tests agent locally
↓
OpenTelemetry captures every operation
↓
Immediate evaluation score (92% correctness, 95% tool accuracy)
↓
Developer sees feedback in <1 second
↓
If bad: fix immediately, re-test
↓
If good: commit with confidence
```

**Real-world analogy:** Running unit tests locally before committing code

---

### Mode 2: Batch Evaluation
```
Developer opens PR
↓
GitHub Actions triggered automatically
↓
Quality evaluation runs on test conversations
↓
Quality gates checked:
  - Correctness >= 85%? PASS ✓
  - Tool Accuracy >= 90%? PASS ✓
  - Helpfulness >= 80%? PASS ✓
↓
All gates pass: PR mergeable ✓
One gate fails: PR blocked, developer fixes, re-tests
↓
Merge happens with confidence
```

**Real-world analogy:** Automated linting + static analysis, but for agent quality

---

### Mode 3: Production Simulation
```
Agent running in production with real traffic
↓
Every request generates OpenTelemetry trace
↓
10% sampling: Only ~10% of traces evaluated (cost optimization)
↓
Trace sent to Bedrock for evaluation
↓
Score (0.0-1.0) stored in metrics database
↓
Dashboard shows trends (24-hour, 7-day averages)
↓
Alert triggered if score drops >2% from baseline
↓
On-call engineer notified (Slack, PagerDuty)
↓
Investigation: Check recent deployments
↓
Root cause found, fix deployed
↓
Verification: Score restored to baseline
```

**Real-world analogy:** Application Performance Monitoring (APM) but for agent behavior

---

### Mode 4: Results Review
```
View saved evaluation data:
  - metrics/evaluations.json (from Mode 2)
  - metrics/prod-monitoring.json (from Mode 3)
  - traces/interactive.json (from Mode 1)
↓
Understand historical trends
↓
Feed into dashboards (Grafana, CloudWatch)
↓
Export to BI tools (Tableau, Power BI)
```

---

## 💡 Key Concepts Explained

### OpenTelemetry Traces
Structured recording of what agent does:
```
agent.run [span]
├─ llm.call [nested span]
│  └─ Attributes: model, prompt, response, tokens
├─ tool_use [nested span]
│  └─ Attributes: tool_name, input, output, success
└─ Attributes: response_time, user_id, etc.
```

### Quality Scores (0.0 - 1.0)
- **Correctness:** Is the answer factually accurate?
- **Tool Use Accuracy:** Did agent pick the RIGHT tool?
- **Helpfulness:** Does it address the user's need?
- **Instruction Following:** Did it respect guidelines?

### Quality Gates
Thresholds that must be PASSED:
- Correctness ≥ 0.85 (85%)
- Tool Use Accuracy ≥ 0.90 (90%)
- Helpfulness ≥ 0.80 (80%)

If ANY gate fails: PR blocks, human must fix

### Sampling Strategy
- Evaluate only 10% of production traffic
- Reduces cost by 90%
- Statistically sufficient for trend detection
- Stratified sampling ensures coverage

---

## 📈 Cost Analysis (Included in Demo)

### Monthly Costs
- Production monitoring (10% sampling): ~$90
- CI/CD evaluation (100 PRs): ~$15
- Total: ~$105/month

### Cost of ONE Prevented Incident
- Support time: $3,000
- Developer firefighting: $5,000
- Lost revenue: $10,000
- Brand damage: Incalculable
- **Total: ~$18,000+**

### ROI
- Prevent 1-2 incidents per year: $18K-36K saved
- Cost of monitoring: ~$1,260/year
- **Return on Investment: 14-28x**

---

## 🔧 What's Simulated (Not Real AWS)

The demo uses **simulated evaluation** instead of real AWS Bedrock because:
1. No AWS credentials needed
2. No API costs incurred
3. Consistent, deterministic output for demos
4. Same pattern applies to real Bedrock API

To connect **real Bedrock**:
```csharp
// In Program.cs, replace EvaluationService with:
var client = new AmazonBedrockRuntimeClient(region);
var response = await client.InvokeModelAsync(new InvokeModelRequest {
    ModelId = "anthropic.claude-3-5-sonnet-20241022-v2:0",
    Body = // ... traces
});
```

---

## 🎓 Educational Value

This demo teaches:

**Architecture:**
- Three-stage quality monitoring pattern
- How to instrument agents with OpenTelemetry
- How to integrate with CI/CD pipelines
- How to set up production monitoring

**Implementation:**
- Real C# code (not pseudocode)
- Actual class structure and design patterns
- Configuration management (appsettings.json)
- Error handling and validation

**Operations:**
- Quality gate thresholds and why they matter
- Sampling strategies and cost optimization
- On-call runbooks and incident response
- Metrics that matter

**Business:**
- Cost-benefit analysis
- ROI calculation
- Risk mitigation through monitoring

---

## ❓ Frequently Asked Questions

**Q: Do I need AWS credentials to run the demo?**
A: No! The demo uses simulated Bedrock evaluation. No AWS account needed.

**Q: Can I run this on Mac/Linux?**
A: Yes! .NET 8.0 runs on all platforms. Use `run-demo.sh` on Mac/Linux.

**Q: How long is the first run?**
A: ~10-15 seconds (first-time compilation). Subsequent runs: ~1-2 seconds.

**Q: Can I customize the demo?**
A: Yes! Edit `appsettings.json` to change thresholds, or edit `Program.cs` to add more conversions.

**Q: How do I connect real Bedrock?**
A: Replace `EvaluationService` with real AWS SDK calls. Full instructions in `Demo-README.md`.

**Q: Where are the output files?**
A: `traces/` and `metrics/` folders (auto-created at runtime).

---

## 📚 Presentation Tips

### For Maximum Impact:
1. **Run Mode 1 first** - Shows interactive feedback (developers love this)
2. **Point out the traces** - OpenTelemetry spans are the "magic"
3. **Highlight the alert** - Drift detection is concrete and powerful
4. **Emphasize cost savings** - $105/month prevents $18K+ incidents
5. **Show the files** - Metrics are concrete proof of what works

### Common Mistakes to Avoid:
- ❌ Don't skip Mode 2 (CI/CD gates are critical)
- ❌ Don't rush Mode 3 (drift detection is the "aha moment")
- ❌ Don't forget to explain sampling (people ask about cost)
- ❌ Don't skip the playbook (on-call workflow is practical)

### Good Things to Emphasize:
- ✅ "No crashes, no errors, just wrong answers" (the problem)
- ✅ "Three overlapping stages catch different issues" (the solution)
- ✅ "Framework-agnostic pattern works with any agent" (the portability)
- ✅ "$18K prevented per incident vs $105/month cost" (the ROI)

---

## 🔗 Related Files in Parent Directory

The parent directory contains presentation materials:

```
C:\Users\user\Downloads\Net Africa\
├── Continuous_Quality_Monitoring_Final.pptx    # 31-slide presentation
├── Demo-README.md                               # This demo's README
├── Demo/                                        # THIS FOLDER (the actual demo)
│   ├── Program.cs
│   ├── ... (demo files)
│   └── RUNNING-THE-DEMO.md
```

The **presentation** covers theory and architecture.  
The **demo** shows it working in practice.  
Together: Complete 1-hour session

---

## ✅ Ready to Present?

1. **Read:** `RUNNING-THE-DEMO.md` (detailed speaker notes)
2. **Test:** Run `dotnet run` and try all 4 modes once
3. **Practice:** Do a dry run with timing
4. **Present:** Follow the script, point out key ideas
5. **Success:** Audience understands three-stage pattern and can apply to their agents

**Time to prepare:** ~30 minutes (reading + test run)

---

## 📞 Support & Customization

**Questions about the demo?**
- Check `RUNNING-THE-DEMO.md` for detailed answers
- Check `Demo-README.md` for architecture details
- Check `QUICK-START.md` for quick help

**Want to extend it?**
- Edit `Program.cs` to add more tools/agents
- Edit `EvaluationService` to customize scoring logic
- Edit `appsettings.json` to change thresholds
- Add real AWS Bedrock (instructions in README)

**Want to use for your own agent?**
- Copy the trace instrumentation pattern
- Copy the evaluation logic
- Adapt tool registry to your tools
- Replace evaluation with real Bedrock

---

## 🎬 Let's Begin!

```bash
cd "C:\Users\user\Downloads\Net Africa\Demo"
dotnet run
```

Select a mode and follow `RUNNING-THE-DEMO.md` for complete speaker notes!

Good luck with your presentation! 🚀
