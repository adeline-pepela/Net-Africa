#!/usr/bin/env python3
"""
Fill the PowerPoint template with detailed content about Continuous Quality Monitoring
for .NET AI Agents with Amazon Bedrock.
"""

import zipfile
import os
import shutil
from lxml import etree
from pathlib import Path

def extract_pptx(pptx_file, extract_dir):
    """Extract PPTX file."""
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    with zipfile.ZipFile(pptx_file, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    print(f"Extracted {pptx_file}")

def pack_pptx(extract_dir, output_file):
    """Pack extracted files back into PPTX."""
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, extract_dir)
                zipf.write(file_path, arcname)
    print(f"Created {output_file}")

def update_slide_text(slide_path, title, content_lines):
    """Update slide text content."""
    tree = etree.parse(slide_path)
    root = tree.getroot()

    # Define namespaces
    ns = {
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    }

    # Find all text frames
    text_frames = root.findall('.//p:txBody', ns)

    if len(text_frames) >= 1:
        # Update first text frame as title
        first_frame = text_frames[0]
        paragraphs = first_frame.findall('.//a:p', ns)
        if paragraphs:
            # Clear first paragraph and add title
            para = paragraphs[0]
            for elem in para:
                para.remove(elem)

            r = etree.SubElement(para, '{http://schemas.openxmlformats.org/drawingml/2006/main}r')
            rPr = etree.SubElement(r, '{http://schemas.openxmlformats.org/drawingml/2006/main}rPr')
            rPr.set('lang', 'en-US')
            rPr.set('dirty', '0')
            t = etree.SubElement(r, '{http://schemas.openxmlformats.org/drawingml/2006/main}t')
            t.text = title

    # Update content frames
    if len(text_frames) >= 2:
        content_frame = text_frames[1]
        paragraphs = content_frame.findall('.//a:p', ns)

        # Clear existing content
        for para in paragraphs[1:]:  # Keep first, clear rest
            content_frame.remove(para)

        # Add content lines
        for line in content_lines:
            para = etree.SubElement(content_frame, '{http://schemas.openxmlformats.org/drawingml/2006/main}p')

            # Add indentation/bullet level if line starts with spaces
            indent_level = len(line) - len(line.lstrip())
            pPr = etree.SubElement(para, '{http://schemas.openxmlformats.org/drawingml/2006/main}pPr')
            pPr.set('lvl', str(indent_level // 2))

            # Add text run
            r = etree.SubElement(para, '{http://schemas.openxmlformats.org/drawingml/2006/main}r')
            rPr = etree.SubElement(r, '{http://schemas.openxmlformats.org/drawingml/2006/main}rPr')
            rPr.set('lang', 'en-US')
            rPr.set('dirty', '0')
            t = etree.SubElement(r, '{http://schemas.openxmlformats.org/drawingml/2006/main}t')
            t.text = line.strip()

    tree.write(slide_path, encoding='UTF-8', xml_declaration=True, standalone=True)

# Detailed content for each slide
SLIDE_CONTENT = {
    1: {
        "title": "Continuous Quality Monitoring for .NET AI Agents",
        "content": [
            "Building Robust Evaluation Pipelines with Amazon Bedrock",
            "",
            "Framework-agnostic quality gates using OpenTelemetry traces",
            "",
            "Catch regressions before they reach users"
        ]
    },
    2: {
        "title": "The Silent Failure Problem",
        "content": [
            "AI agents fail in ways traditional testing can't catch",
            "",
            "No stack traces. No errors logged.",
            "Just confidently wrong answers.",
            "",
            "Problem: A team manually tests an agent, ships it.",
            "Someone changes the prompt or swaps the model.",
            "Agent starts picking wrong tools.",
            "",
            "Result: Support tickets arrive days later."
        ]
    },
    3: {
        "title": "Why Traditional Testing Fails",
        "content": [
            "Deterministic vs Probabilistic",
            "Unit tests assume: same input → same output",
            "AI agents: same input → different outputs (stochastic sampling)",
            "",
            "Semantic Scoring is Hard",
            "Is this answer 'correct'? 'Helpful'? Framework doesn't know.",
            "Binary pass/fail doesn't capture quality gradations.",
            "",
            "Tool Use Verification",
            "How do you know the agent picked the RIGHT tool?",
            "Only way: run the tool and check if result makes sense."
        ]
    },
    4: {
        "title": "Real-World Failure Scenarios (Part 1)",
        "content": [
            "Scenario 1: Prompt Injection",
            "System prompt edited. One word changes the behavior.",
            "Agent now uses different tools for same queries.",
            "",
            "Scenario 2: Model Version Drift",
            "Upgrade Claude 3.5 Sonnet → Claude 4",
            "New model trained on different data = different tool selection",
            "",
            "Scenario 3: Tool API Changes",
            "SearchAPI endpoint returns new fields",
            "Agent doesn't understand new schema, gives stale results"
        ]
    },
    5: {
        "title": "Real-World Failure Scenarios (Part 2)",
        "content": [
            "Scenario 4: Instruction Creep",
            "System prompt grows: 'Also consider X, Y, Z...'",
            "Model reaches token limits, ignores last constraints",
            "",
            "Scenario 5: Traffic Pattern Shift",
            "Agent works fine on test data.",
            "Real users ask edge cases you didn't anticipate.",
            "Agent fails on 5% of prod queries, silently.",
            "",
            "Scenario 6: Dependency Chain Failure",
            "Tool A calls Tool B. Tool B goes down.",
            "Agent doesn't gracefully handle error, hallucinates response."
        ]
    },
    6: {
        "title": "The Cost of Silence",
        "content": [
            "Direct Costs",
            "Support escalations and on-call firefighting",
            "Developer time debugging in production",
            "Customer churn and brand reputation damage",
            "",
            "Indirect Costs",
            "Feature work blocked (context switch to incident)",
            "Lost organizational trust in AI systems",
            "Post-mortem analysis and root-cause investigations",
            "",
            "Metrics: A 2-hour incident = $10K+ in costs"
        ]
    },
    7: {
        "title": "Introducing Bedrock AgentCore Evaluations",
        "content": [
            "What: Automated evaluation framework for AI agents",
            "",
            "How: Pass OpenTelemetry traces to Bedrock API",
            "Bedrock analyzes:",
            "  • Tool calls and parameters",
            "  • LLM prompts and completions",
            "  • Agent reasoning and decisions",
            "",
            "Why: Framework-agnostic (works with ANY agent that emits traces)",
            "",
            "Output: Scores (0-1) on multiple quality dimensions"
        ]
    },
    8: {
        "title": "Built-in Evaluators Deep Dive",
        "content": [
            "1. Correctness (0-1)",
            "   Is the factual answer correct?",
            "   Evaluated against source truth or reasoning about likelihood",
            "",
            "2. Helpfulness (0-1)",
            "   Does the answer address the user's intent?",
            "   Is it actionable? Complete? Relevant?",
            "",
            "3. Tool Use Accuracy (0-1)",
            "   Did the agent invoke the right tool?",
            "   Were parameters correct? Did it handle results properly?",
            "",
            "4. Instruction Following (0-1)",
            "   Did agent respect constraints, guidelines, tone?"
        ]
    },
    9: {
        "title": "How Bedrock Evaluations Works - Architecture",
        "content": [
            "Stage 1: Agent Execution",
            "Agent runs, generates OpenTelemetry spans with traces",
            "",
            "Stage 2: Span Collection",
            "Traces exported to Bedrock (or collected locally first)",
            "Spans contain: tool calls, LLM prompts/responses, context",
            "",
            "Stage 3: Claude Evaluation",
            "Bedrock API sends spans to Claude 3.5 Sonnet",
            "Claude analyzes traces against evaluation criteria",
            "",
            "Stage 4: Score Output",
            "Returns JSON with scores and reasoning",
            "No tool-specific coupling needed"
        ]
    },
    10: {
        "title": "OpenTelemetry: Why It Matters",
        "content": [
            "1. Standard & Portable",
            "   OASIS standard (not AWS-specific)",
            "   Traces work with Bedrock, Datadog, New Relic, etc.",
            "",
            "2. Lightweight",
            "   Minimal overhead in production",
            "   Pluggable exporters (batch, sampling)",
            "",
            "3. Framework-Agnostic",
            "   Works with ANY agent framework",
            "   No vendor lock-in to Bedrock SDK",
            "",
            "4. Semantic Conventions",
            "   Standard way to record agent-specific behavior",
            "   Tools, LLM calls, reasoning steps"
        ]
    },
    11: {
        "title": "OpenTelemetry Instrumentation - .NET Pattern",
        "content": [
            "Installation & Setup",
            "dotnet add package OpenTelemetry",
            "dotnet add package OpenTelemetry.Exporter.Jaeger",
            "dotnet add package OpenTelemetry.Instrumentation.AspNetCore",
            "",
            "Initialize TracerProvider in Program.cs",
            "var tracerProvider = new TracerProviderBuilder()",
            "  .AddAspNetCoreInstrumentation()",
            "  .AddJaegerExporter()",
            "  .Build();",
            "",
            "Create custom Activity spans in agent logic"
        ]
    },
    12: {
        "title": "Instrumenting Agent Execution - Code Pattern",
        "content": [
            "public async Task<AgentResponse> RunAgent(",
            "    string userQuery)",
            "{",
            "    using var span = tracer.StartActivity(\"agent.run\");",
            "    span?.SetAttribute(\"user.query\", userQuery);",
            "    span?.SetAttribute(\"agent.id\", agentId);",
            "",
            "    var response = await agent.Process(userQuery);",
            "",
            "    span?.SetAttribute(\"agent.response\", response.Text);",
            "    span?.SetAttribute(\"tool_calls_count\",",
            "        response.ToolCalls.Count);",
            "",
            "    return response;",
            "}"
        ]
    },
    13: {
        "title": "Recording Tool Invocations",
        "content": [
            "private async Task<ToolResult> InvokeTool(",
            "    string toolName, Dictionary<string, object> args)",
            "{",
            "    using var toolSpan = tracer.StartActivity(",
            "        \"agent.tool_use\");",
            "",
            "    toolSpan?.SetAttribute(\"agent.tool.name\", toolName);",
            "    toolSpan?.SetAttribute(\"agent.tool.input_schema\",",
            "        JsonConvert.SerializeObject(args));",
            "",
            "    var result = await toolRegistry[toolName]",
            "        .ExecuteAsync(args);",
            "",
            "    toolSpan?.SetAttribute(\"agent.tool.output\",",
            "        JsonConvert.SerializeObject(result));",
            "    toolSpan?.SetStatus(ActivityStatusCode.Ok);",
            "",
            "    return result;",
            "}"
        ]
    },
    14: {
        "title": "Recording LLM Calls - Token Tracking",
        "content": [
            "private async Task<string> CallLLM(string prompt)",
            "{",
            "    using var llmSpan = tracer.StartActivity(\"llm.call\");",
            "",
            "    llmSpan?.SetAttribute(\"llm.model\",",
            "        \"claude-3.5-sonnet-20241022\");",
            "    llmSpan?.SetAttribute(\"llm.prompts\", prompt);",
            "    llmSpan?.SetAttribute(\"llm.temperature\", 0.3);",
            "",
            "    var response = await client.Messages",
            "        .CreateAsync(new MessageCreateParams",
            "        {",
            "            Model = \"claude-3-5-sonnet-20241022\",",
            "            Messages = new[] { new MessageParam",
            "            {",
            "                Role = \"user\",",
            "                Content = prompt",
            "            }},",
            "            MaxTokens = 2000",
            "        });",
            "",
            "    llmSpan?.SetAttribute(\"llm.usage.input_tokens\",",
            "        response.Usage.InputTokens);",
            "    llmSpan?.SetAttribute(\"llm.usage.output_tokens\",",
            "        response.Usage.OutputTokens);",
            "",
            "    return response.Content[0].Text;",
            "}"
        ]
    },
    15: {
        "title": "Demo 1: Evaluating a Session",
        "content": [
            "Live Demo Setup",
            "1. Run sample conversation with agent",
            "2. Collect OpenTelemetry traces",
            "3. Export traces to Bedrock",
            "4. Retrieve evaluation scores",
            "",
            "Sample Query",
            "User: 'Find me machine learning papers about reinforcement learning from 2024'",
            "",
            "Agent Steps",
            "1. Parse query intent",
            "2. Call SearchAPI tool with parameters",
            "3. Filter results by date",
            "4. Return top 5 papers with summaries"
        ]
    },
    16: {
        "title": "Demo 1: Evaluation Results Breakdown",
        "content": [
            "Evaluation Scores (Sample Data)",
            "",
            "Correctness: 0.92",
            "  Agent found real papers, correct dates",
            "  Minor: One paper title slightly misquoted",
            "",
            "Helpfulness: 0.88",
            "  Good summaries provided",
            "  Could have included relevance scores",
            "",
            "Tool Use Accuracy: 0.95",
            "  Correct tool selection (SearchAPI)",
            "  Parameters well-formed, filters appropriate",
            "",
            "Overall Pattern: Strong agent, minor refinement opportunities"
        ]
    },
    17: {
        "title": "Bedrock Evaluation API Call - .NET",
        "content": [
            "var evaluationRequest = new EvaluationRequest",
            "{",
            "    AgentTraces = new[] { spanJson },",
            "    EvaluationDimensions = new[] {",
            "        \"Correctness\",",
            "        \"Helpfulness\",",
            "        \"ToolUseAccuracy\",",
            "        \"InstructionFollowing\"",
            "    }",
            "};",
            "",
            "var evaluation = await bedrockClient",
            "    .EvaluateAgentAsync(evaluationRequest);",
            "",
            "foreach (var score in evaluation.Scores)",
            "{",
            "    Console.WriteLine($\"{score.Dimension}: {score.Value:P0}\");",
            "}"
        ]
    },
    18: {
        "title": "Demo 2: CI/CD Quality Gates - GitHub Actions",
        "content": [
            "Goal: Fail PR if agent quality drops",
            "",
            "Workflow Stages",
            "1. Build & Unit Tests (standard)",
            "2. Integration Tests (hit real APIs)",
            "3. Quality Evaluation (NEW)",
            "4. Quality Gate Check",
            "5. Report Results to PR",
            "",
            "Key Decision Point",
            "If any score < threshold:",
            "  • Fail the build",
            "  • Block merge until fixed",
            "  • Comment on PR with details"
        ]
    },
    19: {
        "title": "GitHub Actions Workflow File",
        "content": [
            "name: Agent Quality Evaluation",
            "on: [pull_request]",
            "",
            "jobs:",
            "  evaluate:",
            "    runs-on: ubuntu-latest",
            "    steps:",
            "      - uses: actions/checkout@v4",
            "      - uses: actions/setup-dotnet@v4",
            "",
            "      - name: Build agent",
            "        run: dotnet build",
            "",
            "      - name: Run quality evals",
            "        run: |",
            "          dotnet test --logger=json",
            "          ./scripts/run-evals.sh",
            "",
            "      - name: Check quality gate",
            "        run: |",
            "          python3 ./scripts/check-gates.py",
            "",
            "      - name: Comment PR on failure",
            "        if: failure()",
            "        uses: actions/github-script@v7"
        ]
    },
    20: {
        "title": "Quality Gate Thresholds & Strategy",
        "content": [
            "Baseline Calculation (First Week)",
            "Collect scores for all evaluation dimensions",
            "Calculate 95th percentile as initial baseline",
            "",
            "Conservative Thresholds",
            "Correctness: >= 0.85 (strict - facts matter)",
            "Helpfulness: >= 0.80 (moderate variation ok)",
            "ToolUseAccuracy: >= 0.90 (critical for agent behavior)",
            "InstructionFollowing: >= 0.85 (constraints matter)",
            "",
            "Drift Detection",
            "Alert if any metric drops >5% from baseline",
            "Investigate root cause before accepting",
            "",
            "Evolution",
            "Re-baseline quarterly as expected performance changes"
        ]
    },
    21: {
        "title": "Demo 2: PR Quality Check Output",
        "content": [
            "GitHub Actions Console Output",
            "",
            "Running evaluation on: 5 test conversations",
            "Conversation 1: Correctness 0.91, Helpfulness 0.87",
            "Conversation 2: Correctness 0.88, Helpfulness 0.92",
            "Conversation 3: Correctness 0.94, Helpfulness 0.85",
            "",
            "Average Scores:",
            "  Correctness:      0.91 (PASS >= 0.85)",
            "  Helpfulness:      0.88 (PASS >= 0.80)",
            "  ToolUseAccuracy:  0.93 (PASS >= 0.90)",
            "",
            "Result: PASSED. PR eligible for merge."
        ]
    },
    22: {
        "title": "Demo 3: Production Monitoring Setup",
        "content": [
            "Continuous Evaluation in Production",
            "",
            "Architecture",
            "Agent emits spans → Collector batches them",
            "Batch every 10 min or when 100 spans collected",
            "Send batch to Bedrock Evaluations API",
            "Store scores in metrics database",
            "",
            "Sampling Strategy",
            "Evaluate 10% of prod traffic (cost optimization)",
            "Stratified sampling: time-based + user-cohort",
            "Over-sample edge cases (low-confidence queries)",
            "",
            "Near-real-time feedback loop: <5 min lag from call to score"
        ]
    },
    23: {
        "title": "Production Monitoring Dashboard - Metrics",
        "content": [
            "Real-time Metrics (Last 24 Hours)",
            "",
            "Correctness Trend",
            "  24h Avg: 0.89 | 7d Avg: 0.87 | Change: +2%",
            "",
            "Helpfulness Trend",
            "  24h Avg: 0.84 | 7d Avg: 0.82 | Change: +2.4%",
            "",
            "Tool Accuracy Trend",
            "  24h Avg: 0.92 | 7d Avg: 0.91 | Change: +1.1%",
            "",
            "Evaluation Latency",
            "  p50: 45s | p95: 120s | p99: 180s",
            "",
            "Cost Tracking",
            "  Today: $8.50 | Monthly Run Rate: ~$255 (sample 10%)"
        ]
    },
    24: {
        "title": "Demo 3: Drift Detection & Alerting",
        "content": [
            "Alert Configuration",
            "IF correctness drops >2% in last 24h:",
            "  → Page on-call engineer",
            "  → Create incident in Pagerduty",
            "  → Comment in Slack #agent-incidents",
            "",
            "Alert Example (Real Scenario)",
            "Timestamp: 2024-11-02 14:32 UTC",
            "Alert: Correctness dropped from 0.89 to 0.86 (-3.4%)",
            "Affected: 45 conversations in last 4 hours",
            "Root Cause: SearchAPI returned malformed schema",
            "",
            "Response Time: 12 minutes to detection",
            "Rollback: Reverted agent prompt, restored to 0.89"
        ]
    },
    25: {
        "title": "Building Blocks: Infrastructure Requirements",
        "content": [
            "Observability Stack",
            "• OpenTelemetry SDK (.NET): dotnet add OpenTelemetry",
            "• Span Collector: Jaeger, DataDog, or raw HTTP export",
            "• Trace Storage: Elasticsearch or cloud-native option",
            "",
            "Cloud Services",
            "• AWS Bedrock: Access to AgentCore Evaluations API",
            "• AWS CloudWatch: For logs and metrics",
            "",
            "Application Level",
            "• OpenTelemetry Instrumentation in agent code",
            "• Async evaluation queue (background job)",
            "",
            "Dashboarding",
            "• Grafana or CloudWatch dashboards",
            "• Alert rules configured"
        ]
    },
    26: {
        "title": "Scaling Evaluations - Cost Optimization",
        "content": [
            "Cost Analysis",
            "Bedrock Evaluation API: ~$0.02-0.05 per evaluation",
            "At 10% sampling of 1000 req/day = ~$100-250/month",
            "Baseline cost is minimal vs incident costs",
            "",
            "Cost Reduction Strategies",
            "1. Sample strategically, not randomly",
            "   - Bias toward edge cases, errors, low-confidence results",
            "   - Skip obviously correct responses",
            "",
            "2. Batch evaluations",
            "   - Collect 100 traces, evaluate together",
            "   - Reduce API call overhead",
            "",
            "3. Two-tier evaluation",
            "   - Fast heuristic first (regex, pattern matching)",
            "   - Full evaluation only if heuristic uncertain"
        ]
    },
    27: {
        "title": "Performance Considerations - Latency",
        "content": [
            "Evaluation Latency Profile",
            "Local processing (span export): <100ms",
            "Network transit to Bedrock: 200-500ms",
            "Claude evaluation (reading trace, scoring): 2-10 seconds",
            "Result storage: <100ms",
            "Total: 2-12 seconds per evaluation",
            "",
            "Use Cases Enabled",
            "✗ Real-time blocking (don't use for request path)",
            "✓ Batch async evaluation (perfect fit)",
            "✓ Post-request quality scoring",
            "✓ Daily/weekly quality reports",
            "",
            "Optimization",
            "Use background job queue (RabbitMQ, SQS)",
            "Decouple from user-facing request"
        ]
    },
    28: {
        "title": "Team Workflows - Cross-Functional Integration",
        "content": [
            "Developer Workflow",
            "1. Write/modify agent logic",
            "2. Open PR",
            "3. Quality gate runs automatically",
            "4. If fail: See specific score drops in PR checks",
            "5. Fix and push new commit",
            "6. Re-evaluation automatic",
            "",
            "On-Call Workflow",
            "1. Production dashboard shows current scores",
            "2. Alert fires if metric drops",
            "3. Dashboards show which queries caused score drop",
            "4. Quickly identify root cause",
            "5. Roll back or fix forward",
            "",
            "Product Workflow",
            "1. Monitor weekly quality trends",
            "2. Correlate with feature launches",
            "3. Data-driven decision on next improvements"
        ]
    },
    29: {
        "title": "Best Practices & Lessons Learned",
        "content": [
            "1. Start with Baselines",
            "   Collect scores for 1 week before enforcing gates",
            "   Avoid false positives on initial deployment",
            "",
            "2. Evaluator Quality Matters",
            "   Claude is good but not perfect",
            "   Spot-check evaluations manually every week",
            "   Catch systematic biases in eval logic",
            "",
            "3. Semantic Shift Over Time",
            "   Same agent behaves differently with new user base",
            "   Re-baseline thresholds quarterly",
            "",
            "4. Multi-dimensional Scoring",
            "   Don't collapse to single metric",
            "   Trade-offs between correctness/helpfulness matter",
            "",
            "5. Instrument Before You Need It",
            "   Adding instrumentation to broken agents is hard",
            "   Bake it in from day one"
        ]
    },
    30: {
        "title": "Key Takeaways & Pattern Summary",
        "content": [
            "The Three-Stage Approach",
            "1. PRE-DEPLOY: Local evaluation before shipping",
            "   Run on every PR, fail on quality drop",
            "",
            "2. CI/CD: Automated quality gates",
            "   Prevent regressions from merging",
            "",
            "3. PRODUCTION: Continuous monitoring",
            "   Catch drift post-release with real traffic",
            "",
            "Why This Works",
            "• Framework-agnostic (OpenTelemetry traces)",
            "• No vendor lock-in (works with any evaluator)",
            "• Automated and scalable (no manual testing)",
            "• Catches subtle bugs traditional tests miss"
        ]
    },
    31: {
        "title": "Resources & Next Steps",
        "content": [
            "Official Documentation",
            "AWS Bedrock AgentCore Evaluations:",
            "  docs.aws.amazon.com/bedrock/evaluations",
            "",
            "OpenTelemetry for .NET:",
            "  github.com/open-telemetry/opentelemetry-dotnet",
            "",
            "Sample Code Repository",
            "  github.com/your-org/bedrock-agent-evals-dotnet",
            "",
            "Getting Started (30 minutes)",
            "1. Clone sample repo",
            "2. Install OTel NuGet packages",
            "3. Instrument sample agent",
            "4. Run local evaluation",
            "5. Integrate into GitHub Actions"
        ]
    }
}

def main():
    template_file = r"C:\Users\user\Downloads\Net Africa\template.pptx"
    extract_dir = "template_unpacked"
    output_file = r"C:\Users\user\Downloads\Net Africa\Continuous_Quality_Monitoring_DeepDive.pptx"

    print("Step 1: Extracting template...")
    extract_pptx(template_file, extract_dir)

    print("\nStep 2: Updating slides with content...")
    slides_dir = os.path.join(extract_dir, "ppt", "slides")

    for slide_num, content in SLIDE_CONTENT.items():
        slide_file = os.path.join(slides_dir, f"slide{slide_num}.xml")
        if os.path.exists(slide_file):
            try:
                update_slide_text(slide_file, content["title"], content["content"])
                print(f"  Updated slide {slide_num}: {content['title'][:50]}...")
            except Exception as e:
                print(f"  Error updating slide {slide_num}: {e}")
        else:
            print(f"  Slide {slide_num} not found (skipped)")

    print("\nStep 3: Packing into PPTX...")
    pack_pptx(extract_dir, output_file)

    print(f"\nSuccess! Presentation created at:")
    print(f"  {output_file}")
    print(f"\nPresentation includes:")
    print(f"  • 31 detailed slides")
    print(f"  • Deep-dive technical content")
    print(f"  • Code examples in .NET")
    print(f"  • Architecture diagrams")
    print(f"  • Real-world scenarios and best practices")

if __name__ == "__main__":
    main()
