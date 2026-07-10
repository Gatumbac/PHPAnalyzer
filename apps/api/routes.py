import logging
from dataclasses import asdict
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from packages.analyzer import analyze_php

from .schemas import AnalyzeRequest, AnalyzeResponse, HealthResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
    try:
        result = analyze_php(
            source_code=payload.source_code,
            include_tokens=payload.include_tokens,
        )
        return AnalyzeResponse.model_validate(asdict(result))
    except Exception as exc:
        request_id = str(uuid4())
        logger.exception("Error interno en /analyze [request_id=%s]: %s", request_id, exc)
        raise HTTPException(
            status_code=500,
            detail=f"Error interno durante el analisis. request_id={request_id}",
        ) from exc
