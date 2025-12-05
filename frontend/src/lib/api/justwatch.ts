/**
 * API client for JustWatch backend
 */

const API_BASE_URL = 'http://localhost:8000/api/justwatch';

export interface ExternalIds {
	imdbId?: string;
	tmdbId?: string;
}

export interface Genre {
	shortName: string;
}

export interface Backdrop {
	backdropUrl?: string;
}

export interface TitleContent {
	title: string;
	fullPath?: string;
	originalReleaseYear?: number;
	originalReleaseDate?: string;
	productionCountries?: string[];
	runtime?: number;
	shortDescription?: string;
	genres?: Genre[];
	externalIds?: ExternalIds;
	posterUrl?: string;
	backdrops?: Backdrop[];
}

export interface TitleNode {
	id: string;
	objectId?: number;
	objectType?: string;
	content?: TitleContent;
}

export interface TitleNodeWrapper {
	node: TitleNode;
}

export interface SearchResult {
	edges: TitleNodeWrapper[];
}

export interface SearchTitlesResponse {
	popularTitles: SearchResult;
}

export interface OfferPackage {
	id: string;
	packageId: number;
	clearName: string;
	technicalName?: string;
	icon?: string;
}

export interface OfferDetails {
	id: string;
	presentationType?: string;
	monetizationType?: string;
	retailPrice?: string;
	retailPriceValue?: number;
	currency?: string;
	lastChangeRetailPriceValue?: number;
	type?: string;
	package?: OfferPackage;
	standardWebURL?: string;
	elementCount?: number;
	availableTo?: any;
	deeplinkRoku?: string;
	subtitleLanguages?: string[];
	videoTechnology?: string[];
	audioTechnology?: string[];
	audioLanguages?: string[];
}

export interface TitleOfferViewModel {
	country: string;
	packageUrl?: string;
	packageClearName?: string;
	retailPrice?: string;
	retailPriceValue?: number;
	normalizedPrice: number;
	presentationType?: string;
	monetizationType?: string;
	subtitleLanguages?: string;
	audioLanguages?: string;
	technology?: string;
	offerDetails: OfferDetails;
}

class JustWatchAPI {
	private baseUrl: string;

	constructor(baseUrl: string = API_BASE_URL) {
		this.baseUrl = baseUrl;
	}

	async searchTitles(query: string, country: string = 'US'): Promise<SearchTitlesResponse> {
		const response = await fetch(`${this.baseUrl}/search?q=${encodeURIComponent(query)}&country=${country}`);
		if (!response.ok) {
			throw new Error(`Search failed: ${response.statusText}`);
		}
		return response.json();
	}

	async getTitle(nodeId: string): Promise<TitleNode> {
		const response = await fetch(`${this.baseUrl}/title/${nodeId}`);
		if (!response.ok) {
			throw new Error(`Failed to get title: ${response.statusText}`);
		}
		return response.json();
	}

	async getTitleOffers(nodeId: string, path: string): Promise<TitleOfferViewModel[]> {
		const response = await fetch(`${this.baseUrl}/offers/${nodeId}?path=${encodeURIComponent(path)}`);
		if (!response.ok) {
			throw new Error(`Failed to get offers: ${response.statusText}`);
		}
		return response.json();
	}

	async getAvailableLocales(path: string): Promise<string[]> {
		const response = await fetch(`${this.baseUrl}/locales?path=${encodeURIComponent(path)}`);
		if (!response.ok) {
			throw new Error(`Failed to get locales: ${response.statusText}`);
		}
		const data = await response.json();
		return data.locales;
	}
}

export const justWatchAPI = new JustWatchAPI();
