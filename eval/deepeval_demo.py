"""
eval/deepeval_demo.py
A hands-on look at DeepEval: scores REAL tone_fixer.fix_tone() calls
with an LLM-as-judge metric, and writes a local HTML report - no
Confident AI account/login involved. Makes live Anthropic API calls
(costs money, non-deterministic) - not part of the fast mocked pytest suite.

Run: python eval/deepeval_demo.py
Report written to: eval/deepeval_report/*.html
"""

import sys
sys.path.insert(0, ".")

from deepeval import evaluate
from deepeval.evaluate.configs import AsyncConfig, DisplayConfig
from deepeval.metrics import GEval
from deepeval.models import AnthropicModel
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

from config import LLM_MODEL
from services.tone_fixer import fix_tone

CASES = [
    {
        "email": "hey we need that contract signed today, you're holding up the whole deal",
        "target_tone": "professional",
    },
    {
        "email": "your report was late again and honestly it's getting annoying",
        "target_tone": "empathetic",
    },
]

judge = AnthropicModel(model=LLM_MODEL)

test_cases = []
for case in CASES:
    result = fix_tone(email=case["email"], target_tone=case["target_tone"])
    print(f"[{case['target_tone']}] {case['email']!r} -> {result.rewritten_email!r}")
    test_cases.append(
        LLMTestCase(
            input=f"Rewrite this email in a '{case['target_tone']}' tone:\n{case['email']}",
            actual_output=result.rewritten_email,
        )
    )

tone_match = GEval(
    name="Tone Match",
    criteria=(
        "Determine whether the actual_output matches the tone requested in the input "
        "and preserves the original request/meaning from the input email."
    ),
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model=judge,
)

evaluate(
    test_cases=test_cases,
    metrics=[tone_match],
    display_config=DisplayConfig(
        file_type="html",
        file_output_dir="eval/deepeval_report",
        inspect_after_run=False,
    ),
    async_config=AsyncConfig(run_async=False),
)
