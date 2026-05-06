1. Project Structure (Sprint 0)
Start by creating this minimal directory layout. You’ll flesh it out over time.

text
patient_simulator/
├── configs/
│   ├── personas/
│   │   └── alzheimer_mild.yaml
│   ├── goals/
│   │   └── report_symptom.yaml
│   ├── scenarios/
│   │   └── diabetes_day.yaml
│   └── noise_models/
│       ├── motor_noise.yaml
│       └── cognitive_distortions.yaml
├── src/
│   ├── personae.py
│   ├── state.py
│   ├── goals.py
│   ├── scenario.py
│   ├── dialogue_engine.py
│   ├── noise_pipeline.py
│   ├── utterance_generator.py
│   ├── turn_object.py
│   ├── chatbot_interface.py
│   └── evaluator/
│       ├── judge_llm.py
│       └── metrics.py
├── outputs/
│   └── dialogues/
├── tests/
│   └── ...
├── requirements.txt
└── README.md
Initial prompt for your AI assistant:

“Create the directory structure above. Write a basic requirements.txt with pyyaml, pydantic, openai, numpy. Write a minimal README.md explaining the project.”

2. Sprint 1 – Single Persona, One Turn, Labeled Output (Days 1–2)
Goal: Generate a single patient utterance and its ground‑truth annotation.

Step 1: Define the core data classes with Pydantic
Prompt:

“Create src/personae.py: define a Pydantic model Persona with all the fields we discussed (diagnosis, cognitive_profile as a nested model, language_model, motor_model, emotional_profile, health_state, tool_prefs, personal_facts: list[str]). Include a class method from_yaml(path). Add src/state.py with a DialogueState model holding working_memory (list), mood (float), physiological_state (dict), and active_goals (list).”

Step 2: Goal schema
Prompt:

“Create src/goals.py: define a Pydantic model GoalSchema with fields id, description, gold_action_rules (action_type, expected_response_contains: list[str], forbidden_content: list[str], safety_flag: bool). Add a from_yaml class method.”

Step 3: Turn object
Prompt:

“Create src/turn_object.py: define a Pydantic model TurnObject with fields turn_index, timestamp, persona_id, user_utterance, state_snapshot (DialogueState before utterance), active_goal_id, gold_labels (a dict containing gold_action and evaluation_criteria).”

Step 4: First utterance generation (minimal)
Prompt:

“Write src/utterance_generator.py with a function generate_turn(persona: Persona, state: DialogueState, goal: GoalSchema) -> TurnObject. For now, just create a simple utterance from the goal description without any noise, e.g., a string like ‘I feel dizzy’. Fill the TurnObject with dummy state_snapshot and the goal’s gold action rules as labels.”

Step 5: Config files and a run script
Prompt:

“Create configs/personas/alzheimer_mild.yaml with realistic values for a mild Alzheimer’s persona. Create configs/goals/report_symptom.yaml. Write a script run_single_turn.py that loads a persona and a goal, initializes a state, and prints the TurnObject as JSON.”

Test this with your AI assistant: run the script and verify a JSON output. Now you have a tiny benchmark label generator.

3. Sprint 2 – Dialogue Engine: Linear Scenario and Dummy Chatbot (Days 3–4)
Goal: Produce a multi‑turn conversation between your simulator and a placeholder chatbot.

Step 1: Scenario state machine
Prompt:

“Create configs/scenarios/simple_day.yaml with a list of ‘events’ (time, situation_name, goal_id, transition_condition). Write src/scenario.py to load this YAML and return a list of ScenarioStep objects. Each step activates a goal and updates DialogueState (e.g., blood_glucose changes based on meal events).”

Step 2: Dialogue manager
Prompt:

“Create src/dialogue_engine.py with a class DialogueEngine that takes a persona, a scenario, and a ChatbotInterface. It runs through each scenario step, calls the utterance generator for a user turn, passes it to the chatbot, records the response, updates the state (simple rule: if chatbot says expected phrase, goal completed and move to next step), and stores all TurnObjects. Include a method run_full_dialogue() that returns a list of turns with chatbot responses attached.”

Step 3: Dummy chatbot
Prompt:

“Create src/chatbot_interface.py with a class DummyChatbot that implements a method respond(user_text) -> str. It could just echo ‘I understand. Let me help.’. Later we’ll plug in real chatbots.”

Run a full dialogue; output the conversation plus turn objects. You now have a continuous dialogue producer.

4. Sprint 3 – The Noise Pipeline: Making It Unpredictable and Realistic (Days 5–7)
This is where the clinical texture enters. All distortions are rule‑based and configurable, so you can improve realism later just by editing YAML files.

Step 1: Motor noise from config
Prompt:

“In configs/noise_models/motor_noise.yaml, define parameters: tremor_prob, letter_repetition_max, missing_space_prob, random_caps_prob. Write src/noise_pipeline.py with function apply_motor_noise(text, persona) that reads persona.motor_model and the config, then applies those distortions using random choices (seeded for reproducibility).”

Step 2: Cognitive distortions
Prompt:

“Add configs/noise_models/cognitive_distortions.yaml with word_substitution_prob, circumlocution_prob, pause_insertion_prob, telegraphic_style. Write apply_cognitive_distortion(text, persona) that:

Replaces words with ‘thing’ or ‘that stuff’ occasionally.

Inserts ‘…’ for pauses.

Strips articles if telegraphic style.
All based on persona’s language_model.”

Step 3: Affective wrapping and off-topic injection
Prompt:

“Implement add_emotional_prefix(text, persona, current_mood) that prepends a phrase like ‘I’m feeling really low today…’ if mood is low. Also implement inject_off_topic(persona, probability=0.2) that randomly selects a fact from persona.personal_facts and inserts it into the utterance (or separates with a period). These functions go into utterance_generator.py, which now chains: goal template filling → affective wrap → cognitive distortion → motor noise → off‑topic injection.”

Step 4: Update TurnObject labels accordingly
The gold labels remain unchanged; they come from the goal. Even though the surface is distorted, the ground truth (what the chatbot must infer) is still the original intent. The evaluation will later test robustness to this noisy surface.

Now run a dialogue with noise and see the messy, authentic-looking user inputs.

5. Sprint 4 – Goal Library & Scenario Variety (Week 2)
Goal: Expand to multiple conditions and more complex daily stories.

Step 1: Add the rest of the persona configs
Prompt:

“Create YAML files for the other 4 conditions (2‑3 personas each) under configs/personas/ using the same schema as the Alzheimer’s one. Fill them with plausible values based on brief clinical summaries I’ll provide in comments.”

Step 2: Build out the goal ontology
Prompt:

“Create goal YAML files for request_reminder, express_emotional_distress, memory_repetition, off_topic_share, medication_uncertainty, symptom_report_red_flag etc. Each should contain pre‑written gold action rules as in our schema.”

Step 3: Write richer scenario scripts
Prompt:

“For each condition, design a _day.yaml scenario that mixes high‑stakes medical goals with casual chatter and includes state changes (e.g., Alzheimer’s sundowning event in the evening). Use the same scenario format.”

At this point you have a wide coverage matrix. You can generate diverse dialogues automatically.

6. Sprint 5 – LLM‑as‑Judge Evaluation (Week 3)
Goal: Automatically score chatbot responses against the gold labels.

Step 1: Judge prompt template
Prompt:

“Create src/evaluator/judge_llm.py with a function evaluate_turn(turn: TurnObject, chatbot_response: str) -> dict that:

Loads a prompt template from configs/judge_prompt.txt.

Fills in the dialogue history, current user utterance, chatbot response, and gold labels (expected contains, forbidden contains, action type).

Calls an OpenAI‑compatible API (with model name from config).

Returns a JSON with scores (safety_correct: 0/1, info_accuracy: 0‑2, empathy: 0‑2, goal_completion: 0/1) and reasoning.”

Step 2: Prompt template
Prompt:

“Write configs/judge_prompt.txt using a chain‑of‑thought format:
‘You are a clinical evaluator. Here is the hidden patient state and the gold standard for this turn. Rate the chatbot’s response...’”

Step 3: Calibration set preparation
Even without patients, you can manually create 20‑30 turns with perfect and flawed chatbot responses, then have two different LLMs score them to check inter‑judge reliability.

Prompt:

“Write a script scripts/calibrate_judge.py that runs the evaluator on a hand‑written CSV of turns and responses, then computes Cohen’s kappa between two judge models. Report the result.”

This validates your automated metric.

7. Sprint 6 – Full Benchmark Run & Reporting (Week 4)
Goal: Run a complete benchmark, generate scores, and produce a report.

Step 1: Orchestration script
Prompt:

“Write run_benchmark.py that loops over all persona YAMLs and scenario YAMLs, creates a DialogueEngine with the DummyChatbot (or a real API‑connected bot), runs the dialogue, and saves the full turn log to outputs/dialogues/{persona}_{scenario}.json.”

Step 2: Scoring and aggregation
Prompt:

“Write src/evaluator/metrics.py that loads all dialogue logs, runs the judge on each turn, and computes per‑condition and per‑ability composite scores. Output a results_summary.json.”

Now you have a working, fully automated health chatbot benchmark.

How to Instruct AI Assistants Effectively
Give focused, single‑responsibility prompts. Instead of “build the engine,” say “Create a Pydantic model Persona with these fields...”.

Provide the data structures explicitly in your prompt. Copy the skeleton from the plan.

Ask for tests immediately: “After writing the class, also write a Pytest test that loads a YAML and checks the fields are populated.”

Iterate within a sprint: If the generated code isn’t quite right, refine the prompt: “Now modify the apply_motor_noise function so it respects the persona’s tremor_type field, and only applies repetitions if tremor_type is ‘resting’.”

Use configs as a “realism dial.” Tell the AI: “The realism comes from the YAML files. Make the pipeline read all distortion parameters from configs/noise_models/*.yaml – do not hardcode them.”

Adding Realism Later (the “Content” Phase)
Once the engine is solid, you can progressively enhance believability by editing only the YAML files and the content banks (no code changes). For example:

Expand personal_facts with hundreds of off‑topic lines.

Add more symptom_phrases for each condition.

Refine noise model probabilities based on real speech‑language pathology data.

Include drug‑interaction knowledge in the gold action rules.

You can even use LLMs to generate these content banks