"""
Pydantic models for JustWatch API responses and requests
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class ExternalIds(BaseModel):
    imdb_id: Optional[str] = Field(None, alias="imdbId")
    tmdb_id: Optional[str] = Field(None, alias="tmdbId")


class Genre(BaseModel):
    short_name: str = Field(..., alias="shortName")


class Backdrop(BaseModel):
    backdrop_url: Optional[str] = Field(None, alias="backdropUrl")


class TitleContent(BaseModel):
    title: str
    full_path: Optional[str] = Field(None, alias="fullPath")
    original_release_year: Optional[int] = Field(None, alias="originalReleaseYear")
    original_release_date: Optional[str] = Field(None, alias="originalReleaseDate")
    production_countries: Optional[List[str]] = Field(None, alias="productionCountries")
    runtime: Optional[int] = None
    short_description: Optional[str] = Field(None, alias="shortDescription")
    genres: Optional[List[Genre]] = None
    external_ids: Optional[ExternalIds] = Field(None, alias="externalIds")
    poster_url: Optional[str] = Field(None, alias="posterUrl")
    backdrops: Optional[List[Backdrop]] = None


class TitleNode(BaseModel):
    id: str
    object_id: Optional[int] = Field(None, alias="objectId")
    object_type: Optional[str] = Field(None, alias="objectType")
    content: Optional[TitleContent] = None


class TitleNodeWrapper(BaseModel):
    node: TitleNode


class SearchResult(BaseModel):
    edges: List[TitleNodeWrapper] = Field(default_factory=list)


class SearchTitlesResponse(BaseModel):
    popular_titles: SearchResult = Field(..., alias="popularTitles")


class OfferPackage(BaseModel):
    id: str
    package_id: int = Field(..., alias="packageId")
    clear_name: str = Field(..., alias="clearName")
    technical_name: Optional[str] = Field(None, alias="technicalName")
    icon: Optional[str] = None


class OfferDetails(BaseModel):
    id: str
    presentation_type: Optional[str] = Field(None, alias="presentationType")
    monetization_type: Optional[str] = Field(None, alias="monetizationType")
    retail_price: Optional[str] = Field(None, alias="retailPrice")
    retail_price_value: Optional[float] = Field(None, alias="retailPriceValue")
    currency: Optional[str] = None
    last_change_retail_price_value: Optional[float] = Field(None, alias="lastChangeRetailPriceValue")
    type: Optional[str] = None
    package: Optional[OfferPackage] = None
    standard_web_url: Optional[str] = Field(None, alias="standardWebURL")
    element_count: Optional[int] = Field(None, alias="elementCount")
    available_to: Optional[Any] = Field(None, alias="availableTo")
    deeplink_roku: Optional[str] = Field(None, alias="deeplinkRoku")
    subtitle_languages: Optional[List[str]] = Field(None, alias="subtitleLanguages")
    video_technology: Optional[List[str]] = Field(None, alias="videoTechnology")
    audio_technology: Optional[List[str]] = Field(None, alias="audioTechnology")
    audio_languages: Optional[List[str]] = Field(None, alias="audioLanguages")


class GetOffersResponse(BaseModel):
    node: Dict[str, List[OfferDetails]]


class UrlMetadataResponse(BaseModel):
    id: int
    locale: Optional[str] = None
    object_type: Optional[str] = Field(None, alias="objectType")
    object_id: Optional[int] = Field(None, alias="objectId")
    full_path: Optional[str] = Field(None, alias="fullPath")
    href_lang_tags: Optional[List[Dict[str, Any]]] = Field(None, alias="hrefLangTags")


class TitleOfferViewModel(BaseModel):
    country: str
    package_url: Optional[str] = Field(None, alias="packageUrl")
    package_clear_name: Optional[str] = Field(None, alias="packageClearName")
    retail_price: Optional[str] = Field(None, alias="retailPrice")
    retail_price_value: Optional[float] = Field(None, alias="retailPriceValue")
    normalized_price: float = Field(alias="normalizedPrice")
    presentation_type: Optional[str] = Field(None, alias="presentationType")
    monetization_type: Optional[str] = Field(None, alias="monetizationType")
    subtitle_languages: Optional[str] = Field(None, alias="subtitleLanguages")
    audio_languages: Optional[str] = Field(None, alias="audioLanguages")
    technology: Optional[str] = None
    offer_details: OfferDetails = Field(alias="offerDetails")

    model_config = ConfigDict(populate_by_name=True, by_alias=True)
