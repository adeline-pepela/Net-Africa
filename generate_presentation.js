const PptxGen = require('pptxgenjs');

const pres = new PptxGen();
pres.defineLayout({ name: 'LAYOUT_16x9', width: 10, height: 5.625 });
pres.layout = 'LAYOUT_16x9';

// Theme definition
const THEME = {
  name: "Bedrock Quality",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1a1a1a",    // dark gray
    lt1: "ffffff",    // white
    dk2: "2c3e50",    // slate
    lt2: "ecf0f1",    // light gray
    accent1: "ff9500", // orange
    accent2: "3498db", // blue
    accent3: "2ecc71", // green
    accent4: "e74c3c", // red
    accent5: "9b59b6", // purple
    accent6: "1abc9c", // turquoise
    hlink: "3498db",
    folHlink: "2980b9"
  }
};

pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };

const C = pres.SchemeColor;

// Helper function to add a title-content slide
function addContentSlide(title, content, sectionTitle) {
  const slide = pres.addSlide();
  slide.sectionTitle = sectionTitle;

  // Background
  slide.background = { color: "ffffff" };

  // Top accent bar
  slide.addShape("rect", {
    x: 0, y: 0, w: 10, h: 0.08,
    fill: { color: THEME.colors.accent1 },
    line: { type: "none" }
  });

  // Title
  slide.addText(title, {
    x: 0.5, y: 0.25, w: 9, h: 0.6,
    fontSize: 40,
    bold: true,
    color: THEME.colors.dk1,
    fontFace: THEME.headFontFace,
    align: "left"
  });

  // Content area
  if (Array.isArray(content)) {
    let yPos = 1.1;
    content.forEach((item, idx) => {
      slide.addText(item, {
        x: 0.7, y: yPos, w: 8.6, h: 0.5,
        fontSize: item.includes("•") ? 16 : 18,
        color: THEME.colors.dk2,
        fontFace: THEME.bodyFontFace,
        align: "left"
      });
      yPos += 0.65;
    });
  } else {
    slide.addText(content, {
      x: 0.7, y: 1.1, w: 8.6, h: 4,
      fontSize: 16,
      color: THEME.colors.dk2,
      fontFace: THEME.bodyFontFace,
      align: "left"
    });
  }

  return slide;
}

// Slide 1: Title Slide
(() => {
  const slide = pres.addSlide();
  slide.background = { color: THEME.colors.dk1 };

  // Accent stripe
  slide.addShape("rect", {
    x: 0, y: 0, w: 3, h: 5.625,
    fill: { color: THEME.colors.accent1 },
    line: { type: "none" }
  });

  // Main title
  slide.addText("Continuous Quality Monitoring", {
    x: 3.5, y: 1.2, w: 6, h: 0.8,
    fontSize: 44,
    bold: true,
    color: THEME.colors.lt1,
    fontFace: THEME.headFontFace,
    align: "left"
  });

  slide.addText("for .NET AI Agents with Amazon Bedrock", {
    x: 3.5, y: 2.1, w: 6, h: 0.6,
    fontSize: 28,
    color: THEME.colors.accent1,
    fontFace: THEME.bodyFontFace,
    align: "left"
  });

  // Subtitle
  slide.addText("Building Robust Evaluation Pipelines with OpenTelemetry", {
    x: 3.5, y: 3.0, w: 6, h: 0.5,
    fontSize: 16,
    color: THEME.colors.lt2,
    fontFace: THEME.bodyFontFace,
    align: "left"
  });

  // Footer
  slide.addText("60-Minute Technical Talk", {
    x: 3.5, y: 5.0, w: 6, h: 0.4,
    fontSize: 12,
    color: THEME.colors.lt2,
    fontFace: THEME.bodyFontFace,
    align: "left"
  });

  slide.addNotes("Opening slide. Set the stage: Testing AI agents is hard. They fail silently. No crashes, no errors—just wrong answers. This talk covers how to catch those failures before users do.");
})();

// Slide 2: Agenda Overview
(() => {
  const slide = pres.addSlide();
  slide.sectionTitle = "Introduction";
  slide.background = { color: "ffffff" };

  // Title bar
  slide.addShape("rect", {
    x: 0, y: 0, w: 10, h: 0.08,
    fill: { color: THEME.colors.accent1 }
  });

  slide.addText("Today's Agenda", {
    x: 0.5, y: 0.2, w: 9, h: 0.6,
    fontSize: 40, bold: true, color: THEME.colors.dk1,
    fontFace: THEME.headFontFace
  });

  const items = [
    "🎯 The Problem: Why Monitoring Matters",
    "📊 Amazon Bedrock AgentCore Evaluations",
    "🔍 OpenTelemetry Instrumentation",
    "🚀 Three Live Demos (Pre-deploy, CI/CD, Production)",
    "🛠️ Implementation Patterns & Best Practices",
    "📈 Real-World Scaling Considerations"
  ];

  let yPos = 1.1;
  items.forEach(item => {
    slide.addText(item, {
      x: 0.8, y: yPos, w: 8.4, h: 0.55,
      fontSize: 18, color: THEME.colors.dk2,
      fontFace: THEME.bodyFontFace
    });
    yPos += 0.65;
  });

  slide.addNotes("Six major sections. Walk through quickly—we'll dive deep into each.");
})();

// Slide 3: The Problem - Silent Failures
addContentSlide("The Problem: Silent Failures", [
  "🔴 Scenario: A team ships an AI agent after testing it manually",
  "",
  "They ask it a few questions, it seems fine, and they deploy it.",
  "",
  "Then: Someone changes the prompt, or swaps the model, or edits a tool definition.",
  "",
  "❌ The agent starts picking the wrong tool. Giving confidently wrong answers.",
  "",
  "🔇 Nothing crashes. No error gets logged.",
  "",
  "⏰ Three days later: A support ticket arrives."
], "The Problem");

(() => {
  const slide = pres.slides[pres.slides.length - 1];
  slide.addNotes("This is the core problem. AI agents are hard to test. Bugs are subtle. No stack traces. This is what we're solving.");
})();

// Slide 4: Why Traditional Testing Fails
addContentSlide("Why Traditional Testing Fails", [
  "✓ Unit tests: Verify functions work in isolation",
  "✓ Integration tests: Verify components talk to each other",
  "✗ Tool-use tests: Hard to verify the agent picked the RIGHT tool",
  "",
  "✗ Semantic tests: 'Did the answer make sense?' is not a pass/fail",
  "",
  "✗ Regression detection: How do you know quality DROPPED?",
  "",
  "✗ Production drift: Agent works in staging, breaks in prod with real traffic"
], "The Problem");

(() => {
  const slide = pres.slides[pres.slides.length - 1];
  slide.addNotes("Traditional testing assumes deterministic outcomes. AI agents are probabilistic. A test that passes today might fail tomorrow with the same code.");
})();

// Slide 5: Real-World Failure Scenarios
addContentSlide("Real-World Failure Scenarios", [
  "📌 Scenario 1: Prompt Edit",
  "  One word changes in the system prompt → agent uses wrong tools",
  "",
  "📌 Scenario 2: Model Swap",
  "  Claude 3.5 Sonnet → newer model, trained differently → different behavior",
  "",
  "📌 Scenario 3: Tool Drift",
  "  API endpoint returns different data → agent gives stale answers",
  "",
  "📌 Scenario 4: Traffic Pattern Shift",
  "  Works on test data, breaks when real users ask edge-case questions"
], "The Problem");

(() => {
  const slide = pres.slides[pres.slides.length - 1];
  slide.addNotes("All real. All happened. All undetected until users complained.");
})();

// Slide 6: The Cost of Undetected Regressions
addContentSlide("The Cost of Undetected Regressions", [
  "💰 Direct Costs:",
  "  • Support tickets and escalations",
  "  • Developer time debugging in production",
  "  • Customer churn and reputation damage",
  "",
  "⏰ Indirect Costs:",
  "  • Delayed feature work (firefighting)",
  "  • Lost trust in the agent system",
  "  • Post-mortem analysis and remediation"
], "Why It Matters");

(() => {
  const slide = pres.slides[pres.slides.length - 1];
  slide.addNotes("A 2-hour support incident can cost $10K+. Months of customer trust loss. Prevention is cheap.");
})();

// Slide 7: The Challenge of Detecting Subtle Failures
addContentSlide("The Challenge of Detecting Subtle Failures", [
  "💭 What does 'correctness' even mean?",
  "  • Did the agent pick the best tool? Or just a reasonable one?",
  "  • Was the answer helpful? To whom?",
  "  • Did it follow the instructions? All of them?",
  "",
  "🎯 How do you score subjective qualities?",
  "",
  "⚡ How do you measure at scale?",
  "  (Thousands of requests per day, each needs evaluation)"
], "Why It Matters");

(() => {
  const slide = pres.slides[pres.slides.length - 1];
  slide.addNotes("Manual QA doesn't scale. You need automated evaluation.");
})();

// Slide 8: Amazon Bedrock AgentCore Evaluations - Overview
addContentSlide("Amazon Bedrock AgentCore Evaluations", [
  "✨ What it is:",
  "  • Automated evaluation framework for AI agents",
  "  • Scores agent behavior on multiple dimensions",
  "  • Uses Claude as the evaluator (meta!)",
  "",
  "🔧 How it works:",
  "  • Pass OpenTelemetry traces to the evaluation API",
  "  • Bedrock analyzes tool calls, prompts, and outputs",
  "  • Returns scores (0-1) for each evaluation dimension"
], "Bedrock Evaluations");

(() => {
  const slide = pres.slides[pres.slides.length - 1];
  slide.addNotes("Framework-agnostic. Works with any agent that emits OpenTelemetry traces. Not vendor-locked to Bedrock SDK.");
})();

// Slide 9: Built-in Evaluators
addContentSlide("Built-in Evaluators", [
  "📋 Correctness:",
  "  Did the agent give a factually correct answer?",
  "",
  "👍 Helpfulness:",
  "  Was the answer useful to the user?",
  "",
  "🔧 Tool Use Accuracy:",
  "  Did the agent pick the right tool for the job?",
  "",
  "✅ Instruction Following:",
  "  Did the agent respect constraints and guidelines?"
], "Bedrock Evaluations");

(() => {
  const slide = pres.slides[pres.slides.length - 1];
  slide.addNotes("Each evaluator is a Claude prompt. You can also define custom evaluators.");
})();

// Slide 10: How Bedrock Evaluations Works
(() => {
  const slide = pres.addSlide();
  slide.sectionTitle = "Bedrock Evaluations";
  slide.background = { color: "ffffff" };

  slide.addShape("rect", {
    x: 0, y: 0, w: 10, h: 0.08,
    fill: { color: THEME.colors.accent1 }
  });

  slide.addText("How Bedrock Evaluations Works", {
    x: 0.5, y: 0.2, w: 9, h: 0.6,
    fontSize: 40, bold: true, color: THEME.colors.dk1,
    fontFace: THEME.headFontFace
  });

  // Flow diagram with text-based arrows
  const flowText = "Agent Runs  →  OTel Traces  →  Bedrock API  →  Claude Evaluates  →  Scores (0-1)";

  slide.addText(flowText, {
    x: 0.5, y: 2.0, w: 9, h: 0.6,
    fontSize: 14, bold: true, color: THEME.colors.dk2,
    align: "center", fontFace: THEME.bodyFontFace
  });

  // Color-coded explanation boxes
  const boxes = [
    { x: 0.7, label: "Agent Runs", color: THEME.colors.accent2 },
    { x: 2.8, label: "OTel Traces", color: THEME.colors.accent3 },
    { x: 4.8, label: "Bedrock API", color: THEME.colors.accent1 },
    { x: 6.9, label: "Evaluate", color: THEME.colors.accent5 },
    { x: 8.5, label: "Scores", color: THEME.colors.accent4 }
  ];

  boxes.forEach(box => {
    slide.addShape("round-rect", {
      x: box.x, y: 2.8, w: 1.3, h: 0.4,
      fill: { color: box.color, transparency: 40 },
      line: { color: box.color, width: 1 }
    });

    slide.addText(box.label, {
      x: box.x, y: 2.8, w: 1.3, h: 0.4,
      fontSize: 10, bold: true, color: THEME.colors.dk1,
      align: "center", valign: "middle"
    });
  });

  // Key insight
  slide.addText("Key insight: Framework-agnostic. Works off traces, not SDK-specific calls.", {
    x: 0.7, y: 3.2, w: 8.6, h: 0.6,
    fontSize: 14, italic: true, color: THEME.colors.accent2,
    fontFace: THEME.bodyFontFace
  });

  slide.addNotes("The trace format is standardized. You can use any agent framework. This is a big deal for portability.");
})();

// Slide 11: Why OpenTelemetry?
addContentSlide("Why OpenTelemetry for .NET Agents?", [
  "🌐 Standard: OASIS standard for observability (not vendor-specific)",
  "",
  "🔌 Pluggable: Swap backends without changing code",
  "",
  "📦 Lightweight: Minimal overhead for trace collection",
  "",
  "🎯 Semantic conventions: Standard way to record agent behavior",
  "  • Tool calls, parameters, results",
  "  • LLM prompts and completions",
  "  • Chain-of-thought reasoning"
], "OpenTelemetry");

(() => {
  const slide = pres.slides[pres.slides.length - 1];
  slide.addNotes("OTel is the industry standard. Your traces work with Bedrock, Datadog, New Relic, etc.");
})();

// Slide 12: Instrumentation Patterns
(() => {
  const slide = pres.addSlide();
  slide.sectionTitle = "OpenTelemetry";
  slide.background = { color: "ffffff" };

  slide.addShape("rect", {
    x: 0, y: 0, w: 10, h: 0.08,
    fill: { color: THEME.colors.accent1 }
  });

  slide.addText("OpenTelemetry Instrumentation Patterns", {
    x: 0.5, y: 0.2, w: 9, h: 0.6,
    fontSize: 40, bold: true, color: THEME.colors.dk1,
    fontFace: THEME.headFontFace
  });

  const codeBlock = `// .NET Example with OpenTelemetry
var activity = Activity.Current;

// Record LLM call
var span = tracer.StartActivity("llm.call");
span?.SetAttribute("llm.model", "claude-3.5-sonnet");
span?.SetAttribute("llm.prompts", systemPrompt);

// Record tool invocation
using var toolSpan = tracer.StartActivity("agent.tool_use");
toolSpan?.SetAttribute("agent.tool.name", "SearchAPI");
toolSpan?.SetAttribute("agent.tool.arguments", args);

// Record completion
span?.SetAttribute("llm.completions", response);`;

  slide.addText(codeBlock, {
    x: 0.5, y: 1.1, w: 9, h: 3.7,
    fontSize: 11, fontFace: "Courier New",
    color: THEME.colors.dk2,
    fill: { color: THEME.colors.lt2 },
    margin: 10
  });

  slide.addNotes("Show how to instrument a .NET agent. Emphasis: spans capture context, tool calls, and results.");
})();

// Slide 13: Key Metrics to Track
addContentSlide("Key Metrics to Track", [
  "📊 Agent Metrics:",
  "  • Span duration (how long each step takes)",
  "  • Tool invocation count (how many tools called)",
  "  • Error rate (when tools fail)",
  "",
  "🧠 LLM Metrics:",
  "  • Token usage (input + output)",
  "  • Model latency",
  "",
  "✅ Quality Metrics (from Bedrock):",
  "  • Correctness score",
  "  • Helpfulness score",
  "  • Tool-use accuracy"
], "OpenTelemetry");

(() => {
  const slide = pres.slides[pres.slides.length - 1];
  slide.addNotes("Metrics inform both performance (speed/cost) and quality (correctness).");
})();

// Slide 14: Demo 1 - Scoring a Session (Setup)
addContentSlide("Demo 1: Scoring a Session (Setup)", [
  "📌 What we'll do:",
  "  • Run an agent through a conversation",
  "  • Collect OpenTelemetry traces",
  "  • Send traces to Bedrock for evaluation",
  "  • See scores for correctness, helpfulness, tool-use",
  "",
  "⏱️ Duration: ~5 minutes live"
], "Demos");

(() => {
  const slide = pres.slides[pres.slides.length - 1];
  slide.addNotes("First demo is straightforward: run → trace → evaluate → show results. This is the fundamental capability.");
})();

// Slide 15: Demo 1 - Live Walkthrough
(() => {
  const slide = pres.addSlide();
  slide.sectionTitle = "Demos";
  slide.background = { color: "ffffff" };

  slide.addShape("rect", {
    x: 0, y: 0, w: 10, h: 0.08,
    fill: { color: THEME.colors.accent1 }
  });

  slide.addText("Demo 1: Live Session Evaluation", {
    x: 0.5, y: 0.2, w: 9, h: 0.6,
    fontSize: 40, bold: true, color: THEME.colors.dk1,
    fontFace: THEME.headFontFace
  });

  // Sample results
  slide.addText("Sample Evaluation Results", {
    x: 0.5, y: 1.0, w: 9, h: 0.4,
    fontSize: 18, bold: true, color: THEME.colors.dk2,
    fontFace: THEME.bodyFontFace
  });

  const results = [
    { label: "Correctness", score: 0.92, color: THEME.colors.accent3 },
    { label: "Helpfulness", score: 0.88, color: THEME.colors.accent2 },
    { label: "Tool Use Accuracy", score: 0.95, color: THEME.colors.accent5 }
  ];

  let yPos = 1.6;
  results.forEach(result => {
    // Label
    slide.addText(result.label, {
      x: 0.7, y: yPos, w: 2.5, h: 0.35,
      fontSize: 14, color: THEME.colors.dk1,
      fontFace: THEME.bodyFontFace
    });

    // Score
    slide.addText((result.score * 100).toFixed(0) + "%", {
      x: 3.3, y: yPos, w: 1, h: 0.35,
      fontSize: 14, bold: true, color: result.color,
      fontFace: THEME.bodyFontFace
    });

    // Bar
    const barWidth = result.score * 4.5;
    slide.addShape("rect", {
      x: 4.5, y: yPos + 0.05, w: barWidth, h: 0.25,
      fill: { color: result.color, transparency: 30 },
      line: { color: result.color, width: 1 }
    });

    yPos += 0.55;
  });

  slide.addText("Interpretation: Agent is strong on correctness and tool selection. Room for improvement on detailed helpfulness.", {
    x: 0.7, y: 3.5, w: 8.6, h: 1.2,
    fontSize: 13, color: THEME.colors.dk2,
    fontFace: THEME.bodyFontFace
  });

  slide.addNotes("Show real scoring output. Explain what each score means. Note: A single session gives one data point. Patterns emerge across many sessions.");
})();

// Slide 16: Demo 2 - GitHub Actions Integration (Setup)
addContentSlide("Demo 2: CI/CD Integration (Setup)", [
  "📌 What we'll do:",
  "  • Show a GitHub Actions workflow",
  "  • Run agent evaluation on every PR",
  "  • Fail the build if quality drops",
  "  • Show PR status checks",
  "",
  "⏱️ Duration: ~5 minutes live"
], "Demos");

(() => {
  const slide = pres.slides[pres.slides.length - 1];
  slide.addNotes("Demo 2 moves into the delivery pipeline. This is where quality gates prevent regressions from merging.");
})();

// Slide 17: Demo 2 - CI/CD Workflow
(() => {
  const slide = pres.addSlide();
  slide.sectionTitle = "Demos";
  slide.background = { color: "ffffff" };

  slide.addShape("rect", {
    x: 0, y: 0, w: 10, h: 0.08,
    fill: { color: THEME.colors.accent1 }
  });

  slide.addText("Demo 2: GitHub Actions Quality Gate", {
    x: 0.5, y: 0.2, w: 9, h: 0.6,
    fontSize: 40, bold: true, color: THEME.colors.dk1,
    fontFace: THEME.headFontFace
  });

  const yamlCode = `# .github/workflows/agent-quality.yml
on: [pull_request]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run agent tests
        run: dotnet test
      - name: Evaluate agent quality
        run: |
          ./scripts/run-evals.sh
          ./scripts/check-quality-gate.sh
      - name: Comment PR
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              body: \`⚠️ Quality evaluation failed.\`
            })`;

  slide.addText(yamlCode, {
    x: 0.5, y: 1.1, w: 9, h: 3.8,
    fontSize: 10, fontFace: "Courier New",
    color: THEME.colors.dk2,
    fill: { color: THEME.colors.lt2 },
    margin: 8
  });

  slide.addNotes("Walk through the workflow. Emphasize: Tests run automatically. Quality gate prevents bad merges. PR feedback is immediate.");
})();

// Slide 18: Demo 3 - Production Monitoring (Setup)
addContentSlide("Demo 3: Production Monitoring (Setup)", [
  "📌 What we'll do:",
  "  • Show real-time evaluation of production traffic",
  "  • Detect quality drift after release",
  "  • Alert when scores drop",
  "",
  "⏱️ Duration: ~5 minutes live"
], "Demos");

(() => {
  const slide = pres.slides[pres.slides.length - 1];
  slide.addNotes("Demo 3 is about catching drift AFTER release. This is crucial—staging data is never perfect.");
})();

// Slide 19: Demo 3 - Production Metrics
(() => {
  const slide = pres.addSlide();
  slide.sectionTitle = "Demos";
  slide.background = { color: "ffffff" };

  slide.addShape("rect", {
    x: 0, y: 0, w: 10, h: 0.08,
    fill: { color: THEME.colors.accent1 }
  });

  slide.addText("Demo 3: Production Quality Dashboard", {
    x: 0.5, y: 0.2, w: 9, h: 0.6,
    fontSize: 40, bold: true, color: THEME.colors.dk1,
    fontFace: THEME.headFontFace
  });

  // Dashboard mock
  const metrics = [
    { label: "Today's Avg Correctness", value: "0.89", color: THEME.colors.accent3, sparkline: "↘" },
    { label: "7-Day Trend", value: "−2%", color: THEME.colors.accent4, sparkline: "📉" },
    { label: "Tool Accuracy", value: "0.93", color: THEME.colors.accent2, sparkline: "→" },
    { label: "Evaluation Lag", value: "<2min", color: THEME.colors.accent5, sparkline: "✓" }
  ];

  let yPos = 1.2;
  metrics.forEach(metric => {
    // Metric box
    slide.addShape("round-rect", {
      x: 0.5, y: yPos, w: 9, h: 0.6,
      fill: { color: metric.color, transparency: 85 },
      line: { color: metric.color, width: 1 }
    });

    slide.addText(metric.label, {
      x: 0.8, y: yPos + 0.05, w: 4, h: 0.5,
      fontSize: 13, color: THEME.colors.dk2,
      valign: "middle"
    });

    slide.addText(metric.value + " " + metric.sparkline, {
      x: 7.5, y: yPos + 0.05, w: 1.8, h: 0.5,
      fontSize: 16, bold: true, color: metric.color,
      align: "right", valign: "middle"
    });

    yPos += 0.75;
  });

  slide.addText("Alert triggered: Correctness dropped 2% in last 7 days. Check recent deployments.", {
    x: 0.7, y: 4.2, w: 8.6, h: 0.8,
    fontSize: 12, italic: true, color: THEME.colors.accent4,
    fontFace: THEME.bodyFontFace
  });

  slide.addNotes("Show metrics trending. Explain threshold (e.g., alert if score drops >1%). Demonstrate how fast detection is: <2 min from call to evaluation.");
})();

// Slide 20: Building Blocks - Overview
addContentSlide("Building Blocks: What You Need", [
  "🔧 Infrastructure:",
  "  • OpenTelemetry SDK (.NET)",
  "  • Trace collector (e.g., Jaeger, Datadog)",
  "",
  "☁️ Bedrock:",
  "  • AWS account with Bedrock access",
  "  • Agent model (Claude 3.5 Sonnet, etc.)",
  "",
  "📊 Observability:",
  "  • Dashboard for viewing metrics",
  "  • Alerting rules for quality drops"
], "Building Blocks");

(() => {
  const slide = pres.slides[pres.slides.length - 1];
  slide.addNotes("Minimal set of pieces. Not complex. Most .NET shops already have OTel infrastructure.");
})();

// Slide 21: Code Patterns
(() => {
  const slide = pres.addSlide();
  slide.sectionTitle = "Building Blocks";
  slide.background = { color: "ffffff" };

  slide.addShape("rect", {
    x: 0, y: 0, w: 10, h: 0.08,
    fill: { color: THEME.colors.accent1 }
  });

  slide.addText("Code Pattern: Agent Loop with Tracing", {
    x: 0.5, y: 0.2, w: 9, h: 0.6,
    fontSize: 40, bold: true, color: THEME.colors.dk1,
    fontFace: THEME.headFontFace
  });

  const pattern = `public async Task<AgentResponse> RunAgent(
    AgentRequest request)
{
  using var span = tracer.StartActivity("agent.run");
  span?.SetAttribute("user.query", request.Query);

  var response = await agent.Chat(request.Query);

  span?.SetAttribute("agent.response", response);
  span?.SetAttribute("agent.tool_calls",
    response.ToolCalls.Count);

  return response;
}

// Later: Send span to Bedrock Evaluations
var evaluation = await bedrock.EvaluateAsync(span);`;

  slide.addText(pattern, {
    x: 0.5, y: 1.1, w: 9, h: 4,
    fontSize: 10, fontFace: "Courier New",
    color: THEME.colors.dk2,
    fill: { color: THEME.colors.lt2 },
    margin: 8
  });

  slide.addNotes("This is the skeleton. Wrap your agent logic with tracing. Bedrock API consumes the span.");
})();

// Slide 22: Best Practices
addContentSlide("Best Practices for Evaluation", [
  "✅ Baseline Before Gating:",
  "  Collect scores for a week before using them to fail builds",
  "",
  "✅ Tier Your Quality Gates:",
  "  Correctness: ≥0.85 | Helpfulness: ≥0.80 | Tool Accuracy: ≥0.90",
  "",
  "✅ Sample Smart:",
  "  Evaluate a representative sample, not every request (cost)",
  "",
  "✅ Monitor Lag:",
  "  Track time from agent completion to evaluation result",
  "",
  "✅ Version Your Evaluators:",
  "  Changes to eval criteria are changes to your SLO"
], "Building Blocks");

(() => {
  const slide = pres.slides[pres.slides.length - 1];
  slide.addNotes("All learned from real deployments. These save you from gotchas.");
})();

// Slide 23: Implementation Patterns
(() => {
  const slide = pres.addSlide();
  slide.sectionTitle = "Implementation";
  slide.background = { color: "ffffff" };

  slide.addShape("rect", {
    x: 0, y: 0, w: 10, h: 0.08,
    fill: { color: THEME.colors.accent1 }
  });

  slide.addText("Step-by-Step Implementation", {
    x: 0.5, y: 0.2, w: 9, h: 0.6,
    fontSize: 40, bold: true, color: THEME.colors.dk1,
    fontFace: THEME.headFontFace
  });

  const steps = [
    { num: "1", label: "Initialize OpenTelemetry", desc: "Add SDK, configure exporters" },
    { num: "2", label: "Instrument Agent Runs", desc: "Wrap logic with spans" },
    { num: "3", label: "Baseline Evaluations", desc: "Run evals for 1 week, gather stats" },
    { num: "4", label: "Set Quality Gates", desc: "Define thresholds per metric" },
    { num: "5", label: "Wire into CI/CD", desc: "Add GitHub Actions workflow" },
    { num: "6", label: "Monitor Production", desc: "Set up alerts, dashboards" }
  ];

  let yPos = 1.1;
  steps.forEach(step => {
    // Step number
    slide.addShape("ellipse", {
      x: 0.6, y: yPos + 0.05, w: 0.4, h: 0.4,
      fill: { color: THEME.colors.accent1 },
      line: { type: "none" }
    });

    slide.addText(step.num, {
      x: 0.6, y: yPos + 0.05, w: 0.4, h: 0.4,
      fontSize: 16, bold: true, color: THEME.colors.lt1,
      align: "center", valign: "middle"
    });

    // Label
    slide.addText(step.label, {
      x: 1.2, y: yPos + 0.05, w: 3, h: 0.2,
      fontSize: 13, bold: true, color: THEME.colors.dk1
    });

    // Description
    slide.addText(step.desc, {
      x: 1.2, y: yPos + 0.27, w: 3, h: 0.2,
      fontSize: 11, color: THEME.colors.dk2,
      italic: true
    });

    yPos += 0.58;
  });

  slide.addNotes("This is the roadmap. Each step is 1-2 hours of work. Total: ~1 day to full production setup.");
})();

// Slide 24: Extensibility Points
addContentSlide("Extensibility: Go Beyond Built-ins", [
  "🎨 Custom Evaluators:",
  "  Write your own scoring logic with Claude",
  "",
  "📊 Multi-Turn Evaluation:",
  "  Score entire conversations, not just single turns",
  "",
  "🔄 A/B Testing:",
  "  Compare agent versions in parallel, score both",
  "",
  "🧠 Domain-Specific Scoring:",
  "  Add evaluators for your specific use case"
], "Implementation");

(() => {
  const slide = pres.slides[pres.slides.length - 1];
  slide.addNotes("Bedrock Evaluations is extensible. You're not limited to the four built-in evaluators.");
})();

// Slide 25: Scaling Evaluations
addContentSlide("Real-World: Scaling Evaluations", [
  "💰 Cost Considerations:",
  "  ~$0.01-0.05 per evaluation (depends on trace size)",
  "  Sample 10% of prod traffic = manageable cost",
  "",
  "⚡ Performance:",
  "  Evaluation latency: 1-3 minutes typical",
  "  Use for async scoring, not real-time gates",
  "",
  "🎯 Sampling Strategy:",
  "  Stratified: Sample across time and user cohorts",
  "  Biased toward edge cases and rare queries"
], "Real-World");

(() => {
  const slide = pres.slides[pres.slides.length - 1];
  slide.addNotes("At scale, you can't evaluate everything. Sample smartly. Focus on queries that are most likely to expose bugs.");
})();

// Slide 26: Cost Optimization
addContentSlide("Cost Optimization Tips", [
  "💡 Reduce Trace Verbosity:",
  "  Only record what's needed (output tokens, not full logs)",
  "",
  "💡 Batch Evaluations:",
  "  Group traces, send once a day (cheaper than per-call)",
  "",
  "💡 Tiered Evaluation:",
  "  Fast correctness check first, detailed eval if it fails",
  "",
  "💡 Caching:",
  "  Same agent behavior = same evaluation (cache results)"
], "Real-World");

(() => {
  const slide = pres.slides[pres.slides.length - 1];
  slide.addNotes("With these tricks, cost is negligible vs. the cost of a single support incident.");
})();

// Slide 27: Team Workflows
addContentSlide("Team Workflows with Evaluation Gates", [
  "👩‍💻 Developer:",
  "  Write code, open PR → evaluations run automatically",
  "",
  "👀 Reviewer:",
  "  See quality delta in PR checks → decide to merge",
  "",
  "📊 On-Call Engineer:",
  "  Monitor prod dashboard → alerted on regressions",
  "",
  "📈 Product Manager:",
  "  Track quality trends → feature launch readiness"
], "Real-World");

(() => {
  const slide = pres.slides[pres.slides.length - 1];
  slide.addNotes("Evaluation integrates naturally into existing workflows. Everyone gets data.");
})();

// Slide 28: What Works
addContentSlide("Key Takeaways: What Works", [
  "✅ OpenTelemetry traces are the right abstraction",
  "  (Framework-agnostic, standardized, portable)",
  "",
  "✅ Three-stage approach catches different types of bugs",
  "  Pre-deploy (dev), CI/CD (integration), Prod (drift)",
  "",
  "✅ Automated evaluation scales QA beyond manual testing",
  "",
  "✅ Quality gates prevent regressions from shipping"
], "Takeaways");

(() => {
  const slide = pres.slides[pres.slides.length - 1];
  slide.addNotes("Summarize the big wins. These are the architectural decisions that matter.");
})();

// Slide 29: What to Watch For
addContentSlide("What to Watch For", [
  "⚠️ Evaluation lag: 1-3 min is OK, >5 min is a problem",
  "",
  "⚠️ Threshold drift: Scores improve over time (data effects)",
  "  Re-baseline quarterly",
  "",
  "⚠️ Sampling bias: Edge cases differ from typical traffic",
  "  Validate on stratified samples",
  "",
  "⚠️ Evaluator quality: Claude is good but not perfect",
  "  Spot-check and challenge low/high outliers"
], "Takeaways");

(() => {
  const slide = pres.slides[pres.slides.length - 1];
  slide.addNotes("These are the gotchas. Knowing them in advance saves debugging later.");
})();

// Slide 30: Resources & Next Steps
(() => {
  const slide = pres.addSlide();
  slide.sectionTitle = "Takeaways";
  slide.background = { color: "ffffff" };

  slide.addShape("rect", {
    x: 0, y: 0, w: 10, h: 0.08,
    fill: { color: THEME.colors.accent1 }
  });

  slide.addText("Resources & Next Steps", {
    x: 0.5, y: 0.2, w: 9, h: 0.6,
    fontSize: 40, bold: true, color: THEME.colors.dk1,
    fontFace: THEME.headFontFace
  });

  slide.addText("📚 Documentation:", {
    x: 0.7, y: 1.1, w: 8.6, h: 0.3,
    fontSize: 16, bold: true, color: THEME.colors.dk1
  });

  slide.addText("• AWS Bedrock AgentCore Evaluations: docs.aws.amazon.com/bedrock/evaluations\n• OpenTelemetry for .NET: github.com/open-telemetry/opentelemetry-dotnet\n• Semantic Conventions (Agents): opentelemetry.io/docs/specs/semconv/gen-ai/", {
    x: 0.7, y: 1.45, w: 8.6, h: 1.0,
    fontSize: 12, color: THEME.colors.dk2,
    fontFace: THEME.bodyFontFace
  });

  slide.addText("🚀 Getting Started:", {
    x: 0.7, y: 2.6, w: 8.6, h: 0.3,
    fontSize: 16, bold: true, color: THEME.colors.dk1
  });

  slide.addText("1. Clone the sample repo\n2. Follow the README to instrument your agent\n3. Run local evals first, then wire into your pipeline\n4. Set your first quality gate", {
    x: 0.7, y: 2.95, w: 8.6, h: 0.95,
    fontSize: 12, color: THEME.colors.dk2,
    fontFace: THEME.bodyFontFace
  });

  slide.addNotes("Point to resources. Make it easy to follow up. Offer to help setup.");
})();

// Slide 31: Thank You & Q&A
(() => {
  const slide = pres.addSlide();
  slide.background = { color: THEME.colors.dk1 };

  // Accent stripe
  slide.addShape("rect", {
    x: 0, y: 0, w: 3, h: 5.625,
    fill: { color: THEME.colors.accent1 },
    line: { type: "none" }
  });

  slide.addText("Thank You!", {
    x: 3.5, y: 1.8, w: 6, h: 1,
    fontSize: 56, bold: true, color: THEME.colors.lt1,
    fontFace: THEME.headFontFace
  });

  slide.addText("Questions?", {
    x: 3.5, y: 2.9, w: 6, h: 0.6,
    fontSize: 28, color: THEME.colors.accent1,
    fontFace: THEME.bodyFontFace
  });

  slide.addText("Let's catch regressions before they catch users.", {
    x: 3.5, y: 3.7, w: 6, h: 0.5,
    fontSize: 14, italic: true, color: THEME.colors.lt2,
    fontFace: THEME.bodyFontFace
  });

  slide.addNotes("Final thought. Open discussion. Be ready for questions on cost, latency, and integration complexity.");
})();

// Write the presentation
pres.writeFile({ fileName: "C:\\Users\\user\\Downloads\\Net Africa\\Continuous_Quality_Monitoring_Presentation.pptx" })
  .then(() => {
    console.log("✅ Presentation created successfully!");
    console.log("📁 File: C:\\Users\\user\\Downloads\\Net Africa\\Continuous_Quality_Monitoring_Presentation.pptx");
  })
  .catch(err => {
    console.error("❌ Error creating presentation:", err);
    process.exit(1);
  });
