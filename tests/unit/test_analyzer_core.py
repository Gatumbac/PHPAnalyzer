import unittest
from pathlib import Path

from packages.analyzer import analyze_php


ROOT = Path(__file__).resolve().parents[2]


class AnalyzerCoreTests(unittest.TestCase):
    def test_tokenization_happy_path_darwin(self):
        source = (ROOT / "tests" / "algorithm_darwin.php").read_text(encoding="utf-8")
        result = analyze_php(source, include_tokens=True)

        self.assertGreater(len(result.tokens), 0)
        self.assertTrue(any(token.type == "PHP_OPEN" for token in result.tokens))
        self.assertEqual(result.status, "success")

    def test_tokenization_happy_path_gabriel(self):
        source = (ROOT / "tests" / "algorithm_gabriel.php").read_text(encoding="utf-8")
        result = analyze_php(source, include_tokens=True)

        self.assertGreater(len(result.tokens), 0)
        self.assertTrue(any(token.type == "POST" for token in result.tokens))
        self.assertEqual(result.status, "semantic_error")

    def test_syntax_error_detection(self):
        source = """<?php
if ($edad >= 18 {
    echo "Mayor";
}
?>"""
        result = analyze_php(source, include_tokens=False)

        self.assertGreater(len(result.syntactic_errors), 0)
        self.assertEqual(result.status, "syntax_error")
        self.assertEqual(result.syntactic_errors[0].phase, "syntactic")

    def test_semantic_type_compatibility_detection(self):
        source = """<?php
$nombre = "Juan";
$numero = 5;
$resultado = $nombre * $numero;
?>"""
        result = analyze_php(source, include_tokens=False)

        self.assertEqual(result.status, "semantic_error")
        self.assertTrue(
            any(err.code == "SEM_INCOMPATIBLE_ARITHMETIC_TYPES" for err in result.semantic_errors)
        )

    def test_state_resets_between_runs(self):
        first_source = """<?php
function validar() {
    return 1;
}
?>"""
        second_source = """<?php
function validar() {
    return 2;
}
?>"""

        first = analyze_php(first_source, include_tokens=False)
        second = analyze_php(second_source, include_tokens=False)

        self.assertEqual(first.status, "success")
        self.assertEqual(second.status, "success")
        self.assertFalse(any(err.code == "SEM_FUNCTION_REDECLARATION" for err in second.semantic_errors))

    def test_result_contract_shape(self):
        source = "<?php $x = 10; ?>"
        result = analyze_php(source, include_tokens=True)

        self.assertIsInstance(result.status, str)
        self.assertIsInstance(result.tokens, list)
        self.assertIsInstance(result.syntactic_errors, list)
        self.assertIsInstance(result.semantic_errors, list)
        self.assertIsInstance(result.meta.elapsed_ms, int)
        self.assertEqual(result.meta.source_length, len(source))
        self.assertEqual(result.meta.analyzer_version, "1.0.0")


if __name__ == "__main__":
    unittest.main()
