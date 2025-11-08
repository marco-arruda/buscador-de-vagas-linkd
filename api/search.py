from typing import List, Optional, Tuple

from time import time
from collections import OrderedDict
from threading import Lock

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel

from buscador_vagas import LinkedInJobScraper


class SearchRequest(BaseModel):
    query: Optional[str] = ""
    location: Optional[str] = "Caruaru, Pernambuco, Brasil"
    num_pages: int = 1


class Job(BaseModel):
    titulo: str
    empresa: str
    localizacao: str
    link: str
    data_postagem: str


app = FastAPI(title="Buscador de Vagas - API", version="0.1")


# Simple in-memory LRU cache with TTL
# Key: tuple (query, location, num_pages)
# Value: (timestamp, data)
_CACHE: OrderedDict = OrderedDict()
_CACHE_LOCK = Lock()
CACHE_TTL_SECONDS = 300  # 5 minutes default
CACHE_MAX_ENTRIES = 128


def _cache_key(req: SearchRequest) -> Tuple[str, str, int]:
    return (str(req.query or "").strip().lower(), str(req.location or "").strip().lower(), int(req.num_pages))


def _get_from_cache(key: Tuple[str, str, int]):
    now = time()
    with _CACHE_LOCK:
        entry = _CACHE.get(key)
        if not entry:
            return None
        ts, data = entry
        if now - ts > CACHE_TTL_SECONDS:
            # expired
            _CACHE.pop(key, None)
            return None
        # refresh LRU position
        _CACHE.move_to_end(key)
        return data


def _set_cache(key: Tuple[str, str, int], data):
    with _CACHE_LOCK:
        _CACHE[key] = (time(), data)
        _CACHE.move_to_end(key)
        # evict oldest if over capacity
        while len(_CACHE) > CACHE_MAX_ENTRIES:
            _CACHE.popitem(last=False)


@app.post("/", response_model=List[Job])
def search(request: SearchRequest, response: Response):
    """Endpoint para buscar vagas.

    Serve requisições de busca. Implementa cache em memória (LRU + TTL).
    Retorna um header `X-Cache: HIT|MISS` para indicar se o resultado veio do cache.
    """
    key = _cache_key(request)

    # checar cache
    cached = _get_from_cache(key)
    if cached is not None:
        response.headers["X-Cache"] = "HIT"
        return cached

    # cache miss
    response.headers["X-Cache"] = "MISS"
    try:
        scraper = LinkedInJobScraper()
        vagas = scraper.buscar_vagas(
            keywords=request.query,
            location=request.location,
            num_paginas=max(1, int(request.num_pages)),
        )

        # Garantir que os itens retornados podem ser serializados pelo Pydantic
        sanitized = []
        for v in vagas:
            sanitized.append({
                'titulo': v.get('titulo', 'N/A'),
                'empresa': v.get('empresa', 'N/A'),
                'localizacao': v.get('localizacao', 'N/A'),
                'link': v.get('link', 'N/A'),
                'data_postagem': v.get('data_postagem', 'N/A'),
            })

        # armazenar no cache
        _set_cache(key, sanitized)

        return sanitized

    except Exception as e:
        # Em ambiente de produção talvez queiramos esconder detalhes do erro
        raise HTTPException(status_code=500, detail=str(e))
