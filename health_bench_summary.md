
A reference paper https://openai.com/index/healthbench/
We would like to do something similar. But without using expert clinicians do evaluation. 

Main Methodology of HealthBench
HealthBench is an open-source, rubric-based benchmark evaluating LLMs on realistic healthcare conversations. The methodology centers on three core components:

1. Conversation-Based Evaluation Framework
5,000 multi-turn conversations between a model and either an individual user or healthcare professional

Conversations average 2.6 turns (range 1–19) and 668 characters

Task: The LLM must respond to the final user message in each conversation

Conversations span 7 themes (emergency referrals, global health, interpreting health data, context-seeking, responding under uncertainty, response depth, and health professional vs. non-professional users)

2. Physician-Written Rubrics (The Core Innovation)
Rubric structure: Each conversation has a unique rubric containing 2–48 specific criteria (median 11, total 48,562 unique criteria across all examples)

Criterion properties:

Each criterion has a point value between -10 and +10 (non-zero)

Positive points = desired behaviors (e.g., "mentions medication dosage")

Negative points = undesirable behaviors (e.g., "provides dangerous advice")

Criteria are objective and self-contained (e.g., "response includes clear emergency referral in first 2 sentences")

Scoring process:

Model-based grader evaluates each criterion independently (met/not met)

Sum points for all met criteria (positive + negative penalties)

Divide by maximum possible positive points for that conversation

Clip final score to [0, 1] range

Overall model score = mean across all 5,000 examples

3. Two Specialized Variants
HealthBench Consensus: 34 pre-defined criteria validated by multiple physicians (appear 8,053 times across conversations) — higher precision, lower recall

HealthBench Hard: Subset of 1,000 difficult examples where top models score ≤32%

4. Physician Cohort (262 physicians)
Practiced in 60 countries, 26 specialties, 49 languages

Created rubrics, categorized conversations, and wrote ideal responses

Multi-step vetting: 1,021 applicants → 262 selected → filtered for quality

5. Trustworthiness Validation
Meta-evaluation: Compare model-based grader against physician grades on 60,896 "meta-examples"

GPT-4.1 achieves macro F1 of 0.709 (comparable to physician-physician agreement of 0.726)

Low score variability (standard deviation ~0.002 across runs)

Key Differentiators from Prior Benchmarks
Realistic, open-ended (not multiple-choice or short-answer)

Physician-validated (not automated metrics)

Unsaturated (top model scores 60%; hardest subset 32%)

Multi-dimensional: Evaluates 5 axes (Accuracy, Completeness, Communication Quality, Context Awareness, Instruction Following)