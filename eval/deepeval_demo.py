"""
eval/deepeval_demo.py
A hands-on look at DeepEval: scores a REAL tone_fixer.fix_tone() call
with an LLM-as-judge metric. Makes live Anthropic API calls (costs money,
non-deterministic) - not part of the fast mocked pytest suite.

Run: python eval/deepeval_demo.py
"""

import sys
sys.path.insert(0, ".")

from deepeval.metrics import GEval
from deepeval.models import AnthropicModel
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

from config import LLM_MODEL
from services.tone_fixer import fix_tone

email = "hey we need that contract signed today, you're holding up the whole deal"
target_tone = "professional"

result = fix_tone(email=email, target_tone=target_tone)

print(f"Original:  {email}")
print(f"Rewritten: {result.rewritten_email}")
print(f"Confidence reported by fix_tone: {result.confidence}\n")

test_case = LLMTestCase(
    input=f"Rewrite this email in a '{target_tone}' tone:\n{email}",
    actual_output=result.rewritten_email,
)

tone_match = GEval(
    name="Tone Match",
    criteria=(
        f"Determine whether the actual_output is written in a '{target_tone}' tone "
        "and preserves the original request/meaning from the input email."
    ),
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model=AnthropicModel(model=LLM_MODEL),
)

tone_match.measure(test_case)

print(f"GEval score:  {tone_match.score:.2f} (threshold {tone_match.threshold})")
print(f"GEval passed: {tone_match.is_successful()}")
print(f"GEval reason: {tone_match.reason}")
