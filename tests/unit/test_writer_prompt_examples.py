"""The worked examples of the writer prompt (resources/prompts/extract-claims) are valid writer
outputs, and they follow the ending rule of the E007 ending round: an ending is written only as a
negative stance with `ends` whose quote names the old value, never also as a negative claim."""

import json
import re
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from grace.context.pipeline.update.patch import parse_patch
from grace.context.pipeline.update.validate import content_words

ROOT = Path(__file__).resolve().parents[2]
SYSTEM = ROOT / "resources" / "prompts" / "extract-claims" / "system.txt"
SCHEMA = ROOT / "resources" / "schemas" / "llm" / "extract-claims.json"


def examples() -> list[tuple[dict[str, str], int, str]]:
    """(known claims by handle, number of new messages, answer text) per example."""
    text = SYSTEM.read_text(encoding="utf-8")
    out = []
    for block in text.split("Example. ")[1:]:
        known = dict(re.findall(r"^(k\d+): (.+)$", block, flags=re.M))
        n = len(re.findall(r"^\[\d+\] ", block, flags=re.M))
        answer = block.split("Answer:\n", 1)[1].split("\n", 1)[0]
        out.append((known, n, answer))
    return out


class WriterPromptExamplesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = Draft202012Validator(json.loads(SCHEMA.read_text(encoding="utf-8")))

    def test_examples_parse(self) -> None:
        exs = examples()
        self.assertGreaterEqual(len(exs), 4)
        for _known, n, answer in exs:
            patch, error = parse_patch(answer, self.validator, n)
            self.assertIsNone(error, answer[:80])
            self.assertIsNotNone(patch)

    def test_endings_are_stances_only(self) -> None:
        for known, _n, answer in examples():
            value = json.loads(answer)
            for claim in value["claims"]:
                self.assertNotEqual(claim.get("polarity"), "negative", claim)
            for stance in value["stances"]:
                if not stance.get("ends"):
                    continue
                self.assertEqual(stance.get("polarity"), "negative", stance)
                old = known[stance["claim"]].split(" | ")[2].split(" [")[0].split(" (")[0]
                # the program's ending-evidence test: a shared content word with the old value
                self.assertTrue(content_words(old) & content_words(stance["quote"]),
                                (old, stance["quote"]))


if __name__ == "__main__":
    unittest.main()
