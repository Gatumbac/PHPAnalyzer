from time import perf_counter

from .lexer import PhpLexer
from .models import AnalysisError, AnalysisMeta, AnalysisResult, TokenInfo
from .parser import PhpParser


def _line_starts(text: str) -> list[int]:
    starts = [0]
    for idx, char in enumerate(text):
        if char == "\n":
            starts.append(idx + 1)
    return starts


def _get_column(lexpos: int, lineno: int, starts: list[int]) -> int:
    line_index = max(0, min(lineno - 1, len(starts) - 1))
    return lexpos - starts[line_index] + 1


def _collect_tokens(source_code: str) -> tuple[list[TokenInfo], list[AnalysisError]]:
    lexer = PhpLexer()
    lexer.input(source_code)
    starts = _line_starts(source_code)

    tokens: list[TokenInfo] = []
    lexical_errors: list[AnalysisError] = []
    while True:
        tok = lexer.token()
        if tok is None:
            break

        lexeme = str(tok.value)
        token_info = TokenInfo(
            type=tok.type,
            lexeme=lexeme,
            line=tok.lineno,
            column=_get_column(tok.lexpos, tok.lineno, starts),
        )
        tokens.append(token_info)

        if tok.type == "ERROR":
            lexical_errors.append(
                AnalysisError(
                    phase="lexical",
                    line=tok.lineno,
                    code="LEX_ILLEGAL_CHARACTER",
                    message=f"Error léxico en línea {tok.lineno}: carácter ilegal '{lexeme}'.",
                )
            )

    return tokens, lexical_errors


def _derive_status(syntactic_errors: list[AnalysisError], semantic_errors: list[AnalysisError]) -> str:
    if syntactic_errors and semantic_errors:
        return "mixed_error"
    if syntactic_errors:
        return "syntax_error"
    if semantic_errors:
        return "semantic_error"
    return "success"


def analyze_php(source_code: str, include_tokens: bool = True) -> AnalysisResult:
    started = perf_counter()

    collected_tokens, lexical_errors = _collect_tokens(source_code)
    lexical_tokens = collected_tokens if include_tokens else []

    parser = PhpParser()
    syntactic_errors, semantic_errors = parser.parse(source_code)
    all_syntactic_errors = [*lexical_errors, *syntactic_errors]
    semantic_skipped = bool(all_syntactic_errors)

    if semantic_skipped:
        semantic_errors = []

    status = _derive_status(all_syntactic_errors, semantic_errors)
    elapsed_ms = int((perf_counter() - started) * 1000)

    return AnalysisResult(
        status=status,
        tokens=lexical_tokens,
        syntactic_errors=all_syntactic_errors,
        semantic_errors=semantic_errors,
        semantic_skipped=semantic_skipped,
        meta=AnalysisMeta(elapsed_ms=elapsed_ms, source_length=len(source_code)),
    )
