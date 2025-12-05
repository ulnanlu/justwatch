"""
JustWatch API service - handles GraphQL queries to JustWatch
"""
import httpx
from typing import List, Optional
from app.models.justwatch_models import (
    SearchTitlesResponse,
    TitleNode,
    GetOffersResponse,
    UrlMetadataResponse,
    TitleOfferViewModel,
    TitleNodeWrapper
)
from app.services.currency_converter import CurrencyConverter
from urllib.parse import urlparse, parse_qs


class JustWatchService:
    def __init__(self, currency_converter: CurrencyConverter):
        self.base_url = "https://apis.justwatch.com"
        self.graphql_url = f"{self.base_url}/graphql"
        self.currency_converter = currency_converter

    async def search_titles(self, query: str, country: str = "US") -> SearchTitlesResponse:
        """Search for titles using GraphQL query"""
        graphql_query = {
            "operationName": "GetSearchTitles",
            "query": """
                query GetSearchTitles(
                    $searchTitlesFilter: TitleFilter!,
                    $country: Country!,
                    $language: Language!,
                    $first: Int!,
                    $formatPoster: ImageFormat,
                    $profile: PosterProfile,
                    $backdropProfile: BackdropProfile
                ) {
                    popularTitles(
                        country: $country
                        filter: $searchTitlesFilter
                        first: $first
                        sortBy: POPULAR
                        sortRandomSeed: 0
                    ) {
                        edges {
                            ...SearchTitleGraphql
                            __typename
                        }
                        __typename
                    }
                }
                
                fragment SearchTitleGraphql on PopularTitlesEdge {
                    node {
                        id
                        objectId
                        objectType
                        content(country: $country, language: $language) {
                            title
                            fullPath
                            originalReleaseYear
                            originalReleaseDate
                            productionCountries
                            runtime
                            shortDescription
                            genres {
                                shortName
                                __typename
                            }
                            externalIds {
                                imdbId
                                tmdbId
                                __typename
                            }
                            posterUrl(profile: $profile, format: $formatPoster)
                            backdrops(profile: $backdropProfile, format: $formatPoster) {
                                backdropUrl
                                __typename
                            }
                            __typename
                        }
                        __typename
                    }
                    __typename
                }
            """,
            "variables": {
                "searchTitlesFilter": {
                    "searchQuery": query,
                    "includeTitlesWithoutUrl": True
                },
                "country": country,
                "language": "en",
                "first": 20,
                "formatPoster": "JPG",
                "formatOfferIcon": "PNG",
                "profile": "S718",
                "backdropProfile": "S1920"
            }
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(self.graphql_url, json=graphql_query)
            response.raise_for_status()
            data = response.json()
            return SearchTitlesResponse(**data["data"])

    async def get_title(self, node_id: str) -> Optional[TitleNode]:
        """Get title details by node ID"""
        graphql_query = {
            "operationName": "GetTitleNode",
            "query": """
                query GetTitleNode(
                    $nodeId: ID!,
                    $language: Language!,
                    $country: Country!,
                    $formatPoster: ImageFormat,
                    $profile: PosterProfile,
                    $backdropProfile: BackdropProfile
                ) {
                    node(id: $nodeId) {
                        ... on MovieOrShow {
                            id
                            objectId
                            objectType
                            content(country: $country, language: $language) {
                                title
                                fullPath
                                originalReleaseYear
                                originalReleaseDate
                                productionCountries
                                runtime
                                shortDescription
                                genres {
                                    shortName
                                    __typename
                                }
                                externalIds {
                                    imdbId
                                    tmdbId
                                    __typename
                                }
                                posterUrl(profile: $profile, format: $formatPoster)
                                backdrops(profile: $backdropProfile, format: $formatPoster) {
                                    backdropUrl
                                    __typename
                                }
                                __typename
                            }
                            __typename
                        }
                    }
                }
            """,
            "variables": {
                "nodeId": node_id,
                "country": "US",
                "language": "en",
                "formatPoster": "JPG",
                "profile": "S718",
                "backdropProfile": "S1920"
            }
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(self.graphql_url, json=graphql_query)
            response.raise_for_status()
            data = response.json()
            node_data = data["data"]["node"]
            if node_data:
                wrapper = TitleNodeWrapper(node=TitleNode(**node_data))
                return wrapper.node
            return None

    async def get_url_metadata(self, path: str) -> Optional[UrlMetadataResponse]:
        """Get URL metadata for a title path"""
        from urllib.parse import quote
        url = f"{self.base_url}/content/urls?path={quote(path)}"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return UrlMetadataResponse(**data)

    async def get_available_locales(self, path: str) -> List[str]:
        """Get available locales for a title"""
        metadata = await self.get_url_metadata(path)
        if metadata and metadata.href_lang_tags:
            return [tag["locale"] for tag in metadata.href_lang_tags if "locale" in tag]
        return []

    async def get_title_offers(self, node_id: str, countries: List[str]) -> Optional[GetOffersResponse]:
        """Get offers for a title in multiple countries"""
        # Build dynamic variables and query for all countries
        variables = {
            "nodeId": node_id,
            "language": "en",
            "filterBuy": {},
            "platform": "WEB"
        }
        
        # Build dynamic GraphQL query for all countries - each country is hardcoded in the query
        country_queries = []
        for country in countries:
            country_lower = country.lower()
            country_queries.append(f"""
                {country_lower}: offers(country: {country.upper()}, platform: $platform, filter: $filterBuy) {{
                    ...TitleOffer
                    __typename
                }}
            """)
        
        query_body = "\n".join(country_queries)
        
        graphql_query = {
            "operationName": "GetTitleOffers",
            "query": f"""
                query GetTitleOffers($nodeId: ID!, $language: Language!, $filterBuy: OfferFilter!, $platform: Platform!) {{
                    node(id: $nodeId) {{
                        ... on MovieOrShowOrSeasonOrEpisode {{
                            {query_body}
                        }}
                    }}
                }}
                
                fragment TitleOffer on Offer {{
                    id
                    presentationType
                    monetizationType
                    retailPrice(language: $language)
                    retailPriceValue
                    currency
                    lastChangeRetailPriceValue
                    type
                    package {{
                        id
                        packageId
                        clearName
                        technicalName
                        icon(profile: S100)
                        __typename
                    }}
                    standardWebURL
                    elementCount
                    availableTo
                    deeplinkRoku: deeplinkURL(platform: ROKU_OS)
                    subtitleLanguages
                    videoTechnology
                    audioTechnology
                    audioLanguages
                    __typename
                }}
            """,
            "variables": variables
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(self.graphql_url, json=graphql_query)
            response.raise_for_status()
            data = response.json()
            return GetOffersResponse(**data["data"])

    def _clean_package_url(self, package_url: Optional[str]) -> Optional[str]:
        """Clean package URL by removing tracking parameters"""
        if not package_url:
            return None
            
        # Handle Disney+ bn5x.net redirects
        if "bn5x.net" in package_url and "www.disneyplus.com" in package_url:
            try:
                parsed = urlparse(package_url)
                query_params = parse_qs(parsed.query)
                clean_url = query_params.get("u", [None])[0]
                if clean_url:
                    return clean_url
            except Exception:
                pass
        
        # Strip query params from specific domains
        domains = ["tv.apple.com", "watch.plex.tv", "play.max.com", "therokuchannel.roku.com"]
        if any(domain in package_url for domain in domains):
            try:
                parsed = urlparse(package_url)
                return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            except Exception:
                pass
        
        return package_url

    def _format_languages(self, languages: Optional[List[str]]) -> Optional[str]:
        """Format language list"""
        if not languages:
            return None
        return ", ".join(languages)

    def _format_technology(self, video_tech: Optional[List[str]], audio_tech: Optional[List[str]]) -> Optional[str]:
        """Format technology information"""
        tech_parts = []
        if video_tech:
            tech_parts.extend([t for t in video_tech if t])  # Filter out empty strings
        if audio_tech:
            tech_parts.extend([t for t in audio_tech if t])  # Filter out empty strings
        return ", ".join(tech_parts) if tech_parts else None

    async def get_all_offers(self, node_id: str, path: str) -> List[TitleOfferViewModel]:
        """Get all offers for a title across all available countries"""
        # Initialize currency converter
        await self.currency_converter.initialize()
        
        # Try to get available locales, but fall back to common countries if that fails
        locales = await self.get_available_locales(path)
        if locales:
            countries = [locale.split("_")[-1] for locale in locales]
        else:
            # Fallback to major countries where streaming services are available
            countries = [
                "US", "GB", "CA", "AU", "DE", "FR", "ES", "IT", "JP", "BR", 
                "MX", "AR", "IN", "NL", "SE", "NO", "DK", "FI", "IE", "NZ",
                "AT", "CH", "BE", "PT", "PL", "CZ", "GR", "TR", "ZA", "KR"
            ]
        
        # Get offers
        offers_response = await self.get_title_offers(node_id, countries)
        if not offers_response:
            return []
        
        # Convert to view models
        result = []
        for country, offers in offers_response.node.items():
            for offer in offers:
                usd_price = self.currency_converter.convert_to_usd(
                    offer.currency,
                    offer.retail_price_value or 0
                )
                
                view_model = TitleOfferViewModel(
                    country=country.upper(),
                    package_url=self._clean_package_url(offer.standard_web_url),
                    package_clear_name=offer.package.clear_name if offer.package else None,
                    retail_price=offer.retail_price,
                    retail_price_value=offer.retail_price_value,
                    normalized_price=usd_price,
                    presentation_type=offer.presentation_type,
                    monetization_type=offer.monetization_type,
                    subtitle_languages=self._format_languages(offer.subtitle_languages),
                    audio_languages=self._format_languages(offer.audio_languages),
                    technology=self._format_technology(offer.video_technology, offer.audio_technology),
                    offer_details=offer
                )
                result.append(view_model)
        
        return result
