#!/usr/bin/env python3
"""
Rebuild the PowerPoint presentation with properly aligned content
following the exact agenda structure and timing.
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

def clear_and_update_slide(slide_path, title, bullet_points):
    """Clear slide content and add new content."""
    tree = etree.parse(slide_path)
    root = tree.getroot()

    ns = {
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    }

    # Find all text bodies and clear them
    txBodies = root.findall('.//p:txBody', ns)

    # Process title (first text body)
    if len(txBodies) > 0:
        title_body = txBodies[0]
        # Clear all paragraphs except keep structure
        paragraphs = title_body.findall('.//a:p', ns)
        for para in paragraphs:
            para.clear()

        # Add title paragraph
        if paragraphs:
            para = paragraphs[0]
        else:
            para = etree.SubElement(title_body, '{http://schemas.openxmlformats.org/drawingml/2006/main}p')

        r = etree.SubElement(para, '{http://schemas.openxmlformats.org/drawingml/2006/main}r')
        rPr = etree.SubElement(r, '{http://schemas.openxmlformats.org/drawingml/2006/main}rPr')
        rPr.set('lang', 'en-US')
        rPr.set('dirty', '0')
        rPr.set('sz', '4400')
        rPr.set('b', '1')
        t = etree.SubElement(r, '{http://schemas.openxmlformats.org/drawingml/2006/main}t')
        t.text = title

    # Process content (second text body)
    if len(txBodies) > 1:
        content_body = txBodies[1]
        paragraphs = content_body.findall('.//a:p', ns)

        # Clear content paragraphs
        for para in paragraphs[1:]:
            content_body.remove(para)

        # Add bullet points
        for bullet in bullet_points:
            para = etree.SubElement(content_body, '{http://schemas.openxmlformats.org/drawingml/2006/main}p')

            # Set indentation based on bullet type
            pPr = etree.SubElement(para, '{http://schemas.openxmlformats.org/drawingml/2006/main}pPr')
            indent_level = 0
            if bullet.startswith("  •"):
                indent_level = 1
                bullet = bullet.replace("  •", "•")
            elif bullet.startswith("    •"):
                indent_level = 2
                bullet = bullet.replace("    •", "•")
            pPr.set('lvl', str(indent_level))

            # Add text
            r = etree.SubElement(para, '{http://schemas.openxmlformats.org/drawingml/2006/main}r')
            rPr = etree.SubElement(r, '{http://schemas.openxmlformats.org/drawingml/2006/main}rPr')
            rPr.set('lang', 'en-US')
            rPr.set('dirty', '0')
            rPr.set('sz', '2400')
            t = etree.SubElement(r, '{http://schemas.openxmlformats.org/drawingml/2006/main}t')
            t.text = bullet.strip()

    tree.write(slide_path, encoding='UTF-8', xml_declaration=True, standalone=True)

# Presentation structure: Slide number -> (title, bullet_points)
SLIDES = {
    1: {
        "title": "Continuous Quality Monitoring for .NET AI Agents with Amazon Bedrock",
        "bullets": [
            "Building Robust Evaluation Pipelines with OpenTelemetry",
            "",
            "Framework-agnostic quality gates for AI agents",
            "",
            "Catch regressions before they reach users"
        ]
    },
    2: {
        "title": "Session Objectives",
        "bullets": [
            "Equip you with practical skills to evaluate AI agent quality",
            "",
            "Integrate monitoring into your CI/CD pipeline",
            "",
            "Detect and respond to agent behavior drift in production",
            "",
            "Apply OpenTelemetry instrumentation patterns to any .NET agent",
            "",
            "Use Amazon Bedrock AgentCore Evaluations for automated quality scoring"
        ]
    },
    3: {
        "title": "Agenda (60-minute technical session)",
        "bullets": [
            "Introduction & The Problem (5 min)",
            "Building & Instrumenting a .NET AI Agent (10 min)",
            "Live Demo 1: Evaluating Agent Quality (15 min)",
            "Live Demo 2: Automated Quality Gates with GitHub Actions (12 min)",
            "Live Demo 3: Production Monitoring & Drift Detection (10 min)",
            "Practical Takeaways & Implementation Pattern (5 min)",
            "Q&A and Closing (3 min)"
        ]
    },
    4: {
        "title": "The Silent Failure Problem",
        "bullets": [
            "Traditional Testing Gap",
            "  Unit/integration tests verify functionality, not semantic correctness",
            "  AI agents fail in ways tests can't catch",
            "",
            "No Visible Errors",
            "  No stack traces. No error logs.",
            "  Agent gives wrong answer with high confidence",
            "",
            "Real Cost",
            "  Support tickets days later",
            "  Damaged customer trust",
            "  Firefighting instead of feature work"
        ]
    },
    5: {
        "title": "Failure Scenarios Without Monitoring",
        "bullets": [
            "Prompt Modification",
            "  One word change in system prompt → wrong tool selection",
            "",
            "Model Version Drift",
            "  New Claude version behaves differently on edge cases",
            "",
            "Tool API Changes",
            "  Underlying service schema changes → stale/incorrect results",
            "",
            "Real-world Impact",
            "  5% of production requests fail silently",
            "  Users complain before you know there's a problem"
        ]
    },
    6: {
        "title": "Building a Simple .NET AI Agent",
        "bullets": [
            "Core Components",
            "  LLM Client (Anthropic SDK for Claude)",
            "  Tool Registry (available tools with schemas)",
            "  Execution Loop (agent decides when to call tools)",
            "",
            "Example: Customer Support Agent",
            "  Tools: SearchKnowledgeBase, GetCustomerHistory, CreateTicket",
            "  Goal: Answer questions or escalate to human",
            "",
            "Key Challenge",
            "  How do we know if it picked the RIGHT tool?",
            "  How do we catch when tool results are wrong?"
        ]
    },
    7: {
        "title": "Introducing OpenTelemetry Instrumentation",
        "bullets": [
            "Standard Observability Framework",
            "  OASIS standard (vendor-neutral, not AWS-specific)",
            "",
            "What We'll Capture",
            "  Agent execution flow (start → end)",
            "  Tool invocations (which tool, with what parameters)",
            "  LLM calls (prompts, responses, token usage)",
            "  Decisions and reasoning steps",
            "",
            "Why This Matters",
            "  Machine-readable record of what agent did",
            "  Foundation for automated evaluation"
        ]
    },
    8: {
        "title": "Instrumenting Agent Execution - Code Pattern",
        "bullets": [
            "Initialize OpenTelemetry in Program.cs",
            "  dotnet add package OpenTelemetry",
            "  var tracer = new TracerProvider().GetTracer(\"MyAgent\");",
            "",
            "Wrap Agent Execution in Spans",
            "  using var span = tracer.StartActivity(\"agent.run\");",
            "  span?.SetAttribute(\"user.query\", userQuery);",
            "  var response = await agent.Process(userQuery);",
            "  span?.SetAttribute(\"tool_calls_count\", response.ToolCalls.Count);",
            "",
            "Export Traces",
            "  OpenTelemetry.Exporter.Jaeger or HTTP endpoint"
        ]
    },
    9: {
        "title": "Recording Tool Invocations",
        "bullets": [
            "Capture Each Tool Call",
            "  using var toolSpan = tracer.StartActivity(\"agent.tool_use\");",
            "  toolSpan?.SetAttribute(\"tool.name\", toolName);",
            "  toolSpan?.SetAttribute(\"tool.input\", inputParams);",
            "",
            "Record Results",
            "  toolSpan?.SetAttribute(\"tool.output\", result);",
            "  toolSpan?.SetAttribute(\"tool.success\", !hasError);",
            "",
            "Track LLM Calls Within Tools",
            "  If tool calls LLM, create nested span",
            "  Gives full picture of agent reasoning"
        ]
    },
    10: {
        "title": "Recording LLM Calls with Token Tracking",
        "bullets": [
            "Capture Every LLM Invocation",
            "  using var llmSpan = tracer.StartActivity(\"llm.call\");",
            "  llmSpan?.SetAttribute(\"llm.model\", \"claude-3.5-sonnet\");",
            "",
            "Track Tokens (Cost & Performance)",
            "  llmSpan?.SetAttribute(\"llm.usage.input_tokens\", inputTokens);",
            "  llmSpan?.SetAttribute(\"llm.usage.output_tokens\", outputTokens);",
            "",
            "Preserve Context",
            "  System prompt, user message, tool descriptions",
            "  These are analyzed by evaluators"
        ]
    },
    11: {
        "title": "Demo 1: Live Agent Evaluation Setup",
        "bullets": [
            "What We'll Demonstrate",
            "  Run an agent conversation",
            "  Collect OpenTelemetry traces",
            "  Send traces to Amazon Bedrock AgentCore Evaluations",
            "  View evaluation scores and analysis",
            "",
            "Test Scenario",
            "  Customer asks: \"I lost my password. How do I reset it?\"",
            "  Agent should: Use SearchKnowledgeBase tool, return instructions",
            "",
            "Evaluation Focus",
            "  Did agent pick correct tool? (Tool Use Accuracy)",
            "  Is answer factually correct? (Correctness)",
            "  Does it help the customer? (Helpfulness)"
        ]
    },
    12: {
        "title": "Amazon Bedrock AgentCore Evaluations",
        "bullets": [
            "What It Does",
            "  Takes OpenTelemetry traces as input",
            "  Claude (LLM) analyzes agent behavior",
            "  Returns scores on multiple dimensions",
            "",
            "Built-in Evaluators",
            "  Correctness: Is the answer factually accurate?",
            "  Helpfulness: Does it address user's need?",
            "  Tool Use Accuracy: Right tool, correct parameters?",
            "  Instruction Following: Respects constraints and guidelines?",
            "",
            "Key Insight",
            "  Framework-agnostic (works with any agent framework)"
        ]
    },
    13: {
        "title": "Demo 1: Evaluation Results Interpretation",
        "bullets": [
            "Sample Evaluation Output",
            "  Correctness Score: 0.92 (92/100)",
            "    ✓ Correct password reset procedure",
            "    ✗ Missing link to support contact",
            "",
            "  Tool Use Accuracy: 0.95 (95/100)",
            "    ✓ SearchKnowledgeBase was correct choice",
            "    ✓ Search parameters well-formed",
            "",
            "  Helpfulness: 0.88 (88/100)",
            "    ✓ Clear step-by-step instructions",
            "    ✗ Could mention support options",
            "",
            "Overall: Strong agent, minor improvements available"
        ]
    },
    14: {
        "title": "Demo 2: Integrating into GitHub Actions",
        "bullets": [
            "Goal: Prevent Quality Regressions",
            "  Every PR → automatic quality evaluation",
            "  Build FAILS if quality drops below threshold",
            "  Blocks merge until fixed",
            "",
            "Workflow Stages",
            "  1. Build and unit tests",
            "  2. Integration tests (hit real services)",
            "  3. Quality evaluation (NEW)",
            "  4. Quality gate check",
            "  5. Report results to PR"
        ]
    },
    15: {
        "title": "GitHub Actions Workflow Structure",
        "bullets": [
            "Trigger: Pull Request Event",
            "  on: [pull_request]",
            "",
            "Jobs",
            "  Build agent code",
            "  Run existing test suite",
            "  Execute ./scripts/run-evals.sh",
            "  Check scores against thresholds",
            "  Comment PR with results",
            "",
            "Quality Gates (Example Thresholds)",
            "  Correctness >= 0.85",
            "  Tool Accuracy >= 0.90",
            "  Helpfulness >= 0.80"
        ]
    },
    16: {
        "title": "Demo 2: PR Quality Check in Action",
        "bullets": [
            "Scenario: Developer modifies agent prompt",
            "",
            "GitHub Actions Output",
            "  ✓ Build successful",
            "  ✓ Tests passed",
            "  ✓ Running quality evaluation...",
            "  ✗ Correctness dropped to 0.78 (was 0.92, threshold 0.85)",
            "",
            "Result",
            "  ✗ Check failed. PR blocked from merge.",
            "  Comment on PR: 'Quality gate failed for Correctness'",
            "",
            "Developer Action",
            "  Revises prompt, pushes new commit",
            "  Evaluation runs again automatically"
        ]
    },
    17: {
        "title": "Demo 2: Resolving Quality Issues",
        "bullets": [
            "After Developer Fix",
            "  New Correctness score: 0.91 ✓",
            "  Tool Accuracy: 0.94 ✓",
            "  Helpfulness: 0.87 ✓",
            "",
            "GitHub Actions Result",
            "  ✓ All checks passed",
            "  PR now mergeable",
            "",
            "Key Benefit",
            "  Quality regression caught before reaching production",
            "  No support tickets",
            "  Immediate feedback to developer"
        ]
    },
    18: {
        "title": "Demo 3: Production Monitoring Setup",
        "bullets": [
            "Continuous Evaluation in Production",
            "  Agent emits traces to OpenTelemetry collector",
            "  Batch collect 100 traces or every 10 minutes",
            "  Send batch to Bedrock Evaluations API",
            "  Store scores in metrics database",
            "",
            "Sampling Strategy (Cost Optimization)",
            "  Evaluate 10% of production traffic",
            "  Stratified: across time and user cohorts",
            "  Over-sample edge cases and errors",
            "",
            "Near-real-time Feedback Loop",
            "  <5 minutes from agent call to evaluation score"
        ]
    },
    19: {
        "title": "Production Monitoring Dashboard",
        "bullets": [
            "Real-time Metrics (Last 24 Hours)",
            "",
            "Correctness Trend",
            "  24h Avg: 0.89 | 7d Avg: 0.87 | Change: +2%",
            "",
            "Tool Accuracy Trend",
            "  24h Avg: 0.92 | 7d Avg: 0.91 | Change: +1.1%",
            "",
            "Helpfulness Trend",
            "  24h Avg: 0.84 | 7d Avg: 0.82 | Change: +2.4%",
            "",
            "Evaluation Performance",
            "  Avg latency: 2-3 seconds per evaluation",
            "  Cost: ~$0.02-0.05 per evaluation"
        ]
    },
    20: {
        "title": "Demo 3: Detecting Quality Drift",
        "bullets": [
            "Alert Scenario",
            "  Alert triggered: Correctness dropped >2% in 4 hours",
            "  Current: 0.86 | Baseline: 0.89",
            "",
            "Investigation Steps",
            "  Dashboard shows: 45 conversations affected",
            "  Time range: 2:00 PM - 6:00 PM UTC",
            "  Common pattern: All queries using SearchAPI tool",
            "",
            "Root Cause Discovery",
            "  SearchAPI service returned malformed schema",
            "  Agent couldn't parse results properly",
            "",
            "Response",
            "  Immediate: Revert agent prompt change (rollback)",
            "  Correctness restored to 0.89 within 5 minutes"
        ]
    },
    21: {
        "title": "Setting Up Production Alerts",
        "bullets": [
            "Alert Thresholds",
            "  IF Correctness drops >2% in last 4 hours → Page on-call",
            "  IF Tool Accuracy drops >3% → Create incident",
            "  IF Helpfulness stays <0.75 for 1 hour → Warning alert",
            "",
            "Notification Channels",
            "  PagerDuty: For high-severity alerts",
            "  Slack: Real-time updates to #agent-incidents",
            "  Email: Daily quality reports",
            "",
            "Playbook",
            "  Alert received → Dashboards show affected users",
            "  Check recent deployments for root cause",
            "  Rollback or hotfix as needed"
        ]
    },
    22: {
        "title": "Implementation Pattern: Three Stages",
        "bullets": [
            "Stage 1: LOCAL DEVELOPMENT",
            "  Evaluate agent locally before committing",
            "  Quick feedback loop",
            "",
            "Stage 2: CI/CD PIPELINE",
            "  Evaluate on every PR",
            "  Quality gates prevent regressions",
            "  Blocks merge if quality drops",
            "",
            "Stage 3: PRODUCTION",
            "  Continuous monitoring of real traffic",
            "  Detect drift after deployment",
            "  Alert and investigate anomalies"
        ]
    },
    23: {
        "title": "Why This Pattern Works",
        "bullets": [
            "Catches Different Problem Types",
            "  Local: Logic errors before commit",
            "  CI/CD: Regressions before production",
            "  Production: Real-world behavior drift",
            "",
            "Framework-Agnostic Foundation",
            "  Built on OpenTelemetry traces (standard)",
            "  Not tied to Bedrock SDK",
            "  Works with any agent framework (.NET, Python, JS, etc.)",
            "",
            "Automated & Scalable",
            "  No manual QA testing",
            "  Scales to thousands of requests/day"
        ]
    },
    24: {
        "title": "Cost & Performance Considerations",
        "bullets": [
            "Cost Analysis",
            "  Bedrock Evaluations: ~$0.02-0.05 per evaluation",
            "  At 10% sampling: ~$100-250/month",
            "  ROI: Prevents one incident = pays for months of monitoring",
            "",
            "Evaluation Latency",
            "  Processing time: 2-10 seconds per trace",
            "  Use for async scoring, not real-time blocking",
            "",
            "Optimization Strategies",
            "  Sample smart (not random)",
            "  Batch evaluations together",
            "  Cache results for identical agent behavior"
        ]
    },
    25: {
        "title": "Infrastructure Requirements",
        "bullets": [
            "Observability Stack",
            "  OpenTelemetry SDK (.NET)",
            "  Trace collector (Jaeger, Datadog, or HTTP exporter)",
            "  Metrics storage (Prometheus, CloudWatch)",
            "",
            "Cloud Services",
            "  AWS Bedrock (AgentCore Evaluations API)",
            "  AWS CloudWatch or similar for dashboards",
            "",
            "Application Level",
            "  OpenTelemetry instrumentation in agent code",
            "  Async evaluation queue (background job)",
            "  GitHub Actions workflows"
        ]
    },
    26: {
        "title": "Implementation Checklist",
        "bullets": [
            "Week 1: Foundation",
            "  ✓ Install OpenTelemetry packages",
            "  ✓ Instrument agent execution, tool calls, LLM calls",
            "  ✓ Setup trace collection to local Jaeger",
            "",
            "Week 2: Evaluation Setup",
            "  ✓ Get AWS Bedrock access",
            "  ✓ Test Bedrock Evaluations API",
            "  ✓ Baseline evaluation scores for 100 conversations",
            "",
            "Week 3: CI/CD Integration",
            "  ✓ Create GitHub Actions workflow",
            "  ✓ Set quality gate thresholds",
            "  ✓ Test on sample PRs",
            "",
            "Week 4: Production Deployment",
            "  ✓ Deploy to production",
            "  ✓ Setup monitoring dashboards",
            "  ✓ Configure alerts"
        ]
    },
    27: {
        "title": "Best Practices & Lessons Learned",
        "bullets": [
            "Start with Baselines",
            "  Collect evaluation scores for 1 week before enforcing gates",
            "  Avoid false positives on initial deployment",
            "",
            "Monitor the Monitors",
            "  Track evaluation latency and API errors",
            "  Claude-based evaluations aren't perfect (spot-check results)",
            "",
            "Instrument Early",
            "  Add OpenTelemetry to new agents from day one",
            "  Retrofitting complex agents is much harder",
            "",
            "Team Alignment",
            "  Educate developers on quality gates",
            "  On-call engineers need dashboard access",
            "  Product managers should see quality trends"
        ]
    },
    28: {
        "title": "Extending the Pattern",
        "bullets": [
            "Custom Evaluators",
            "  Write domain-specific evaluation logic",
            "  Claude analyzes traces using custom criteria",
            "",
            "Multi-turn Conversations",
            "  Evaluate entire conversation, not just single turn",
            "  Score consistency and coherence across turns",
            "",
            "A/B Testing with Evaluations",
            "  Compare two agent versions in parallel",
            "  Score both, pick winner based on metrics",
            "",
            "Integration with Other Tools",
            "  Feed evaluation data to your BI platform",
            "  Correlate with business metrics (CSAT, resolution rate)"
        ]
    },
    29: {
        "title": "Practical Takeaways",
        "bullets": [
            "Key Insight",
            "  Quality monitoring for AI agents is like testing for traditional software",
            "  but evaluation replaces some manual testing",
            "",
            "The Three-Stage Approach Wins Because It",
            "  Catches different problem types at different stages",
            "  Uses framework-agnostic observability (OpenTelemetry)",
            "  Automates what would be manual QA effort",
            "",
            "You Can Apply This To",
            "  Any .NET agent (not just Bedrock agents)",
            "  Any LLM (Claude, GPT, etc.)",
            "  Any agent framework"
        ]
    },
    30: {
        "title": "Reusable Implementation Pattern",
        "bullets": [
            "Template You Can Clone",
            "  GitHub repo with working example",
            "  Sample .NET agent with full instrumentation",
            "  GitHub Actions workflow ready to adapt",
            "  Bedrock Evaluations integration code",
            "",
            "Customization Points",
            "  Your tools and schemas",
            "  Your evaluation thresholds",
            "  Your alert channels (Slack, PagerDuty, etc.)",
            "",
            "Time to Implement",
            "  Start → First evaluation: 2-4 hours",
            "  Start → Production monitoring: 2-3 days"
        ]
    },
    31: {
        "title": "Questions & Resources",
        "bullets": [
            "Documentation",
            "  AWS Bedrock AgentCore Evaluations docs",
            "  OpenTelemetry .NET getting started guide",
            "  Sample code repository (GitHub link in chat)",
            "",
            "Next Steps",
            "  1. Clone sample repo",
            "  2. Follow README to instrument your agent",
            "  3. Run local evaluations first",
            "  4. Wire into your CI/CD pipeline",
            "",
            "Questions?",
            "  Ask now or follow up in GitHub discussions"
        ]
    }
}

def main():
    template_file = r"C:\Users\user\Downloads\Net Africa\template.pptx"
    extract_dir = "template_rebuild"
    output_file = r"C:\Users\user\Downloads\Net Africa\Continuous_Quality_Monitoring_Final.pptx"

    print("=" * 70)
    print("REBUILDING PRESENTATION WITH ALIGNED CONTENT")
    print("=" * 70)

    print("\nStep 1: Extracting template...")
    extract_pptx(template_file, extract_dir)

    print("\nStep 2: Updating 31 slides with aligned content...\n")
    slides_dir = os.path.join(extract_dir, "ppt", "slides")

    for slide_num in sorted(SLIDES.keys()):
        slide_data = SLIDES[slide_num]
        slide_file = os.path.join(slides_dir, f"slide{slide_num}.xml")

        if os.path.exists(slide_file):
            try:
                clear_and_update_slide(
                    slide_file,
                    slide_data["title"],
                    slide_data["bullets"]
                )
                print(f"  Slide {slide_num:2d}: {slide_data['title'][:55]:<55}")
            except Exception as e:
                print(f"  Slide {slide_num:2d}: ERROR - {str(e)[:40]}")

    print("\nStep 3: Packing presentation...")
    pack_pptx(extract_dir, output_file)

    print("\n" + "=" * 70)
    print("SUCCESS!")
    print("=" * 70)
    print(f"\nPresentation: {output_file}")
    print("\nContent Structure:")
    print("  1. Introduction & Session Objectives (slides 1-3)")
    print("  2. The Problem Statement (slides 4-5)")
    print("  3. Building & Instrumenting .NET Agent (slides 6-10)")
    print("  4. Demo 1: Evaluating Agent Quality (slides 11-13)")
    print("  5. Demo 2: GitHub Actions Quality Gates (slides 14-17)")
    print("  6. Demo 3: Production Monitoring & Drift (slides 18-21)")
    print("  7. Implementation Pattern & Best Practices (slides 22-28)")
    print("  8. Practical Takeaways & Closing (slides 29-31)")
    print("\nTotal slides: 31")
    print("Total timing: 60 minutes (5+10+15+12+10+5+3)")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
