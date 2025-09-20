# NetOps Multi-Agent Triage (Agents 4/7/8 + Orchestrator)

This repo wires a Slack bot to a small fleet of agents for network triage:
- **Agent-8** (Triage): proposes/dispatches per-host show commands.
- **Agent-4** (Capture): runs the shows and writes `show_logs/*.md`.
- **Agent-7** (Analyze): parses logs → facts → summaries for Slack.
- **Orchestrator**: Slack app that glues it all together.

### Purpose of each Agent

* Agent-4 → Does capture only (spawns runner, saves logs under 2-capture/).
* Agent-7 → Splits, parses, builds facts, runs LLM analysis, produces Slack JSON.
* Agent-8 → Orchestrates triage per host: prepares INIs, dispatches to Agent-4, kicks off Agent-7 analysis.
* Orchestrator → Slack-facing bot; wires user commands to Agents 4/7/8 and posts results.

## Why it exists
To get from “problem on router X” → “focused capture + scoped analysis” in a single Slack thread, fast and reproducibly.

## Golden path (local)
1. `cp .env.example .env` and fill in tokens (Slack, OpenAI if used).
2. `docker compose up -d --build`
3. In Slack, invite the bot and post: `@agent a7-run configs.5 task-18.bfd`
4. Start triage from the analysis card → run a command (e.g., `show ip bgp summary`).
5. Watch the thread for captured snippets and the host-scoped analysis.


# ai_agents

Multi-agent solution 

