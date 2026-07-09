from dataclasses import dataclass, field
from typing import Literal

AnalysisStatus = Literal["success", "syntax_error", "semantic_error", "mixed_error"]


@dataclass(slots=True)
class TokenInfo:
    type: str
    lexeme: str
    line: int
    column: int


@dataclass(slots=True)
class AnalysisError:
    phase: Literal["lexical", "syntactic", "semantic"]
    message: str
    line: int
    code: str


@dataclass(slots=True)
class AnalysisMeta:
    elapsed_ms: int
    source_length: int
    analyzer_version: str = "1.0.0"


@dataclass(slots=True)
class AnalysisResult:
    status: AnalysisStatus
    tokens: list[TokenInfo] = field(default_factory=list)
    syntactic_errors: list[AnalysisError] = field(default_factory=list)
    semantic_errors: list[AnalysisError] = field(default_factory=list)
    meta: AnalysisMeta = field(default_factory=lambda: AnalysisMeta(elapsed_ms=0, source_length=0))
