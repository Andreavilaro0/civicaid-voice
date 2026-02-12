# Phase 2 Evidence-Based Audit Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Verify that every Phase 2 claim is real, reproducible, aligned across tools, and attributable.

**Architecture:** 6-agent parallel audit with strict scope boundaries. Lead coordinates only. Each agent produces an Evidence Pack with commands + outputs.

**Tech Stack:** Git, pytest, Docker, Notion MCP, filesystem, curl

---

## Audit Gates

| ID | Gate | Agent | Acceptance |
|----|------|-------|------------|
| A1 | Repo inventory | REPO-FORENSICS | All required files exist, tree matches docs |
| A2 | Required files present | REPO-FORENSICS | git clean, remote configured, history exists |
| B1 | Clean venv install | TESTING-REPRO | pip install succeeds, no PEP668 breakage |
| B2 | pytest run | TESTING-REPRO | All tests pass in clean venv |
| B3 | Docker build/run | DOCKER-CI-AUDITOR | Build succeeds, /health returns 200 OK |
| C1 | CI alignment | DOCKER-CI-AUDITOR | Workflow matches repo reality |
| D1 | Notion DB schemas | NOTION-AUDITOR | DBs exist, properties match docs |
| D2 | Notion rows & statuses | NOTION-AUDITOR | Counts match, statuses align with PHASE-STATUS.md |
| E1 | Claims-to-evidence | AUTHORSHIP-LEGITIMACY | Every major claim has supporting evidence |
| F1 | Secret scan | REPO-FORENSICS | Zero real secrets in tracked files |

## Agent Assignments

### 1. REPO-FORENSICS (Tasks: A1, A2, F1)
- `git status --short` + `git log --oneline -10` + `git remote -v`
- File inventory: `find docs scripts src tests -maxdepth 2 -type f | sort`
- Check required files: README.md, pyproject.toml, Dockerfile, render.yaml, .dockerignore, all scripts
- Secret scan: grep for ntn_, TWILIO_, AIza, sk-, OPENAPI_MCP_HEADERS (redact values)
- Verify .gitignore covers .env, secrets/, *.pem, *.key

### 2. TESTING-REPRO (Tasks: B1, B2)
- Create clean venv: `python -m venv .auditvenv`
- Install deps: `pip install -r requirements.txt`
- Document whisper situation (stubbed vs real)
- Run: `pytest tests/ -v --tb=short`
- Record exact output

### 3. DOCKER-CI-AUDITOR (Tasks: B3, C1)
- Docker build: `docker build -t civicaid-voice:audit .`
- Docker run + health check
- Read .github/workflows/ci.yml and verify alignment with pyproject.toml
- Check Python version, pip steps, test commands

### 4. NOTION-AUDITOR (Tasks: D1, D2)
- Query Backlog DB (304c5a0f-372a-81de-92a8-f54c03b391c0): schema + row count
- Query Testing DB (304c5a0f-372a-810d-8767-d77efbd46bb2): schema + row count
- Query KB Tramites DB (304c5a0f-372a-81ff-9d45-c785e69f7335): schema + row count
- Find Phase 2 page, verify sections
- Cross-check counts with PHASE-STATUS.md

### 5. DEPLOY-REALITY (Task: part of B3/C1)
- Read render.yaml and verify start command, port, health check
- Read RENDER-DEPLOY.md and cross-check with render.yaml
- If Render URL in docs: safe GET /health
- Local webhook test: curl POST with sample payload

### 6. AUTHORSHIP-LEGITIMACY (Task: E1)
- Read all evidence files, check every claim has command output
- Cross-check ports, commands, env vars across docs
- Build Legitimacy Matrix: Claim -> Evidence -> Verdict
- Flag unsupported assertions

## Output
Final Audit Report with PASS/PARTIAL/FAIL per gate, evidence index, findings, fix list, confidence scores.
