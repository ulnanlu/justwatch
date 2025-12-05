"""
API routes for JustWatch functionality
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.models.justwatch_models import (
    SearchTitlesResponse,
    TitleNode,
    TitleOfferViewModel
)
from app.services.justwatch_service import JustWatchService
from app.services.currency_converter import CurrencyConverter

router = APIRouter(prefix="/api/justwatch", tags=["justwatch"])

# Initialize services
currency_converter = CurrencyConverter()
justwatch_service = JustWatchService(currency_converter)


@router.get("/search", response_model=SearchTitlesResponse)
async def search_titles(
    q: str = Query(..., description="Search query"),
    country: str = Query("US", description="Country code")
):
    """Search for movies and TV shows"""
    try:
        return await justwatch_service.search_titles(q, country)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/title/{node_id}", response_model=TitleNode)
async def get_title(node_id: str):
    """Get title details by node ID"""
    try:
        title = await justwatch_service.get_title(node_id)
        if not title:
            raise HTTPException(status_code=404, detail="Title not found")
        return title
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/offers/{node_id}", response_model=List[TitleOfferViewModel])
async def get_title_offers(
    node_id: str,
    path: str = Query(..., description="Full path of the title")
):
    """Get all offers for a title across all countries"""
    try:
        offers = await justwatch_service.get_all_offers(node_id, path)
        return offers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/locales")
async def get_available_locales(path: str = Query(..., description="Full path of the title")):
    """Get available locales for a title"""
    try:
        locales = await justwatch_service.get_available_locales(path)
        return {"locales": locales}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
