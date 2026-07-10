from typing import Literal

from pydantic import BaseModel, Field, field_validator

from .settings import settings


class AnalyzeRequest(BaseModel):
    source_code: str = Field(...)
    include_tokens: bool = Field(default=True)

    @field_validator("source_code")
    @classmethod
    def validate_source_code(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("El campo 'source_code' no puede estar vacio.")
        if len(value) > settings.max_source_code_size:
            raise ValueError(
                f"El campo 'source_code' supera el límite de {settings.max_source_code_size} caracteres."
            )
        return value


class TokenInfoResponse(BaseModel):
    type: str
    lexeme: str
    line: int
    column: int


class AnalysisErrorResponse(BaseModel):
    phase: Literal["lexical", "syntactic", "semantic"]
    message: str
    line: int
    code: str


class AnalysisMetaResponse(BaseModel):
    elapsed_ms: int
    source_length: int
    analyzer_version: str


class AnalyzeResponse(BaseModel):
    status: Literal["success", "syntax_error", "semantic_error", "mixed_error"]
    tokens: list[TokenInfoResponse]
    syntactic_errors: list[AnalysisErrorResponse]
    semantic_errors: list[AnalysisErrorResponse]
    semantic_skipped: bool
    meta: AnalysisMetaResponse


class HealthResponse(BaseModel):
    status: Literal["ok"]
