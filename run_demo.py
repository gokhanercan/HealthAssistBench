from __future__ import annotations

import argparse
from pathlib import Path

from healthassistbench.adapters.ollama import OllamaChatAdapter
from healthassistbench.dialogue import DialogueEngine
from healthassistbench.evaluator.judge import score_dialogue_log
from healthassistbench.loader import load_persona, load_scenario, load_tag_taxonomy
from healthassistbench.rendering.text import render_dialogue


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a HealthAssistBench demo dialogue.")
    parser.add_argument(
        "--persona",
        default="configs/personas/parkinsons_retired_teacher.yaml",
        help="Path to persona YAML.",
    )
    parser.add_argument(
        "--scenario",
        default="configs/scenarios/parkinsons_morning_checkin.yaml",
        help="Path to scenario YAML.",
    )
    parser.add_argument(
        "--taxonomy",
        default="configs/taxonomy/tag_schema_v0_1_0.yaml",
        help="Path to tag taxonomy YAML.",
    )
    parser.add_argument(
        "--ollama-model",
        default=None,
        help="Optional Ollama model name. If omitted, no live assistant call is made.",
    )
    parser.add_argument(
        "--ollama-host",
        default="http://localhost:11434",
        help="Ollama host URL.",
    )
    parser.add_argument(
        "--score",
        action="store_true",
        help="Score assistant turns against scenario gold actions.",
    )
    return parser.parse_args()


def trace(msg: str) -> None:
    print(f"[trace] {msg}")


def main() -> None:
    args = parse_args()
    trace(f"args: persona={args.persona} scenario={args.scenario} taxonomy={args.taxonomy} "
          f"ollama_model={args.ollama_model} score={args.score}")

    trace("loading persona YAML -> Persona model")
    persona = load_persona(args.persona)
    trace(f"persona loaded: id={persona.persona_id} diagnosis={persona.diagnosis} "
          f"meds={persona.health_state.medications}")

    trace("loading scenario YAML -> Scenario model")
    scenario = load_scenario(args.scenario)
    trace(f"scenario loaded: id={scenario.scenario_id} condition={scenario.condition} "
          f"steps={len(scenario.steps)} opening_mode={scenario.opening_mode}")
    for i, step in enumerate(scenario.steps):
        trace(f"  step[{i}] id={step.step_id} goal={step.goal_id} "
              f"bot_initiated={'yes' if step.bot_initiated_prompt else 'no'}")

    trace("loading tag taxonomy YAML")
    taxonomy = load_tag_taxonomy(args.taxonomy)
    trace(f"taxonomy loaded: schema_version={taxonomy.tag_schema_version}")

    adapter = None
    if args.ollama_model:
        trace(f"creating OllamaChatAdapter model={args.ollama_model} host={args.ollama_host}")
        adapter = OllamaChatAdapter(
            model=args.ollama_model,
            host=args.ollama_host,
            system_prompt=(
                "You are an assistive health chatbot helping a chronic patient. "
                "Respond supportively, safely, and briefly."
            ),
        )
    else:
        trace("no --ollama-model: skipping live assistant calls (assistant turns come from scenario only)")

    trace("constructing DialogueEngine")
    engine = DialogueEngine(
        persona=persona,
        scenario=scenario,
        tag_schema_version=taxonomy.tag_schema_version,
        assistant_adapter=adapter,
    )

    trace("running dialogue: engine iterates scenario.steps, emitting turns "
          "(bot_initiated_prompt -> patient_template -> optional adapter response)")
    log = engine.run()
    trace(f"dialogue done: {len(log.turns)} turns; "
          f"speakers={[t.speaker for t in log.turns]}")

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    stem = f"{persona.persona_id}_{scenario.scenario_id}"
    json_path = output_dir / f"{stem}.json"
    txt_path = output_dir / f"{stem}.txt"
    trace(f"writing log JSON -> {json_path}")
    json_path.write_text(log.model_dump_json(indent=2), encoding="utf-8")
    trace(f"writing rendered transcript -> {txt_path}")
    txt_path.write_text(render_dialogue(log), encoding="utf-8")

    trace("rendered dialogue:")
    print(render_dialogue(log))
    if args.score:
        trace("scoring dialogue against scenario gold actions")
        print()
        print(score_dialogue_log(log).model_dump_json(indent=2))
    else:
        trace("--score not set: skipping judge scoring")


if __name__ == "__main__":
    main()
