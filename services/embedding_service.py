"""Embedding service abstraction supporting Local (HuggingFace) and Google Gemini embeddings.

Isolated here so VectorStoreService does not need provider-specific logic.
"""
from __future__ import annotations

import os
from config.settings import (
    GEMINI_API_KEY,
    GEMINI_EMBEDDING_MODEL,
    EMBEDDING_PROVIDER,
    LOCAL_EMBEDDING_MODEL,
)
from services.llm_service import MissingCredentialsError


class GeminiEmbeddingService:
    """Embeddings via langchain-google-genai GoogleGenerativeAIEmbeddings."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or GEMINI_API_KEY
        self.model_name = model or GEMINI_EMBEDDING_MODEL
        if not self.api_key:
            raise MissingCredentialsError(
                "GEMINI_API_KEY (or GOOGLE_API_KEY) is not set; cannot construct "
                "the Gemini embedding client. Ingestion and retrieval require valid credentials "
                "when EMBEDDING_PROVIDER=gemini."
            )
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        self._client = GoogleGenerativeAIEmbeddings(
            model=self.model_name,
            google_api_key=self.api_key,
        )

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._client.embed_documents(list(texts))

    def embed_query(self, text: str) -> list[float]:
        return self._client.embed_query(text)

    @property
    def langchain_embeddings(self):
        """Exposes the underlying LangChain Embeddings instance."""
        return self._client


class LocalEmbeddingService:
    """Local offline embeddings using sentence-transformers via langchain-huggingface."""

    def __init__(self, model: str | None = None):
        self.model_name = model or LOCAL_EMBEDDING_MODEL
        # Prevent hanging on huggingface.co connection retries when running in
        # sandboxed, offline, or air-gapped environments
        os.environ.setdefault("HF_HUB_OFFLINE", "1")
        from langchain_huggingface import HuggingFaceEmbeddings

        model_kwargs = {"local_files_only": True}
        try:
            self._client = HuggingFaceEmbeddings(
                model_name=self.model_name,
                model_kwargs=model_kwargs,
                encode_kwargs={"normalize_embeddings": True},
            )
        except Exception:
            # Fallback in case model is not pre-cached locally
            self._client = HuggingFaceEmbeddings(
                model_name=self.model_name,
                encode_kwargs={"normalize_embeddings": True},
            )

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._client.embed_documents(list(texts))

    def embed_query(self, text: str) -> list[float]:
        return self._client.embed_query(text)

    @property
    def langchain_embeddings(self):
        return self._client


def get_embedding_service():
    """Factory to retrieve configured embedding service ('local' or 'gemini')."""
    provider = (EMBEDDING_PROVIDER or "local").strip().lower()
    if provider == "local":
        return LocalEmbeddingService()
    if provider == "gemini":
        return GeminiEmbeddingService()
    raise ValueError(f"Unknown EMBEDDING_PROVIDER '{provider}'. Supported: 'local', 'gemini'.")
