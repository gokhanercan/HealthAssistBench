# HealthAssistBench

HealthAssistBench is a schema-first benchmark scaffold for assistive health chatbots working with chronic patients. It generates structured patient dialogues from persona and scenario configs, annotates each patient turn with dual-sided tags, attaches gold assistant actions, and can score assistant responses against that gold contract.

The current repository is an early vertical slice rather than a finished benchmark. It already supports:

- versioned tag taxonomy in YAML
- persona and scenario configs in YAML
- deterministic dialogue generation from hidden state
- optional live assistant responses through a local Ollama chat endpoint
- gold-action objects attached to patient turns
- a lightweight rule-based judge for quick scoring
- JSON and human-readable text outputs

## Current Scope

Implemented starter conditions:

- Parkinson's disease
- Alzheimer's disease

Implemented core concepts:

- patient-side tags such as `MEMORY-RECALL`, `TOOL-CALENDAR`, `NOISE-COGNITIVE`
- assistant-side expected tags such as `ASSIST-EMPATHY`, `ASSIST-CLARIFY`, `ASSIST-CONFIRM-ACTION`
- per-step `gold_action` objects with required phrases, forbidden phrases, tool actions, memory requirements, and safety flags

## Repository Layout

```text
configs/
  personas/            Persona YAML files
  scenarios/           Scenario YAML files
  taxonomy/            Versioned tag taxonomy YAML
src/healthassistbench/
  adapters/            Chatbot adapters, including Ollama
  evaluator/           Lightweight judge and score aggregation entry points
  rendering/           Human-readable dialogue rendering
  dialogue.py          Dialogue engine
  loader.py            YAML loaders
  schemas.py           Pydantic contracts for the benchmark
run_demo.py            Local demo runner
requirements.txt       Minimal Python dependencies
```

## Quick Start

Python 3.11 is recommended.

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Set `PYTHONPATH` to `src` before running the demo.

### Run Without a Live Model

This generates only the patient-side dialogue structure and writes outputs to `outputs/`.

```bash
PYTHONPATH=src python run_demo.py
```

On PowerShell:

```powershell
$env:PYTHONPATH = "src"
python run_demo.py
```

### Run With Ollama

Start Ollama locally and ensure a chat model is available, for example `gemma4:latest`.

```powershell
$env:PYTHONPATH = "src"
python run_demo.py --ollama-model gemma4:latest --score
```

You can also choose a different persona and scenario:

```powershell
$env:PYTHONPATH = "src"
python run_demo.py `
  --persona configs/personas/alzheimers_former_engineer.yaml `
  --scenario configs/scenarios/alzheimers_evening_confusion.yaml `
  --ollama-model gemma4:latest `
  --score
```

## Outputs

Each run writes two files under `outputs/`:

- `*.json`: canonical structured dialogue log
- `*.txt`: readable rendering with tags and gold actions

The JSON log is the source of truth for later benchmark evaluation.

## What the Judge Does Right Now

The current scorer in `src/healthassistbench/evaluator/judge.py` is intentionally simple. It is a scaffold for later LLM-as-judge evaluation and currently checks:

- required phrase presence
- forbidden phrase absence
- rough tool-use signals
- simple memory matching
- simple empathy heuristics
- simple safety heuristics

This is useful for wiring and quick regression checks, but it is not yet the final evaluation design.

## Extension Points

The next likely extensions are:

- add more personas per condition
- add more day scenarios per persona
- replace the heuristic judge with an LLM-backed judge adapter
- generate patient surface text with a richer LLM pipeline while keeping hidden state rule-driven
- add more conditions and source-grounded biography banks

## Notes for Collaborators

- Keep the tag taxonomy versioned in `configs/taxonomy/`.
- Prefer extending schemas before expanding generation logic.
- Treat the JSON dialogue log as the benchmark contract.
- Do not commit `outputs/`, local virtual environments, or editor-local folders.
