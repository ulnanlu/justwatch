<script lang="ts">
	import { onMount } from 'svelte';
	import { Card, Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell, Spinner, Button, Badge, Input } from 'flowbite-svelte';
	import { justWatchAPI, type TitleNode, type TitleOfferViewModel } from '$lib/api/justwatch';
	
	export let nodeId: string;
	export let titleData: TitleNode | null = null;
	
	let title: TitleNode | null = titleData;
	let offers: TitleOfferViewModel[] = [];
	let filteredOffers: TitleOfferViewModel[] = [];
	let loading = false;
	let offersLoading = false;
	
	// Sort state
	let sortColumn: string = '';
	let sortDirection: 'asc' | 'desc' = 'asc';
	
	// Filter state
	let countryFilter: string = '';
	let providerFilter: string = '';
	let typeFilter: string = '';
	
	// Genre mapping from shortName to full name
	const genreMap: Record<string, string> = {
		'act': 'Action',
		'cmy': 'Comedy',
		'drm': 'Drama',
		'hrr': 'Horror',
		'trl': 'Thriller',
		'rma': 'Romance',
		'scf': 'Sci-Fi',
		'fnt': 'Fantasy',
		'crm': 'Crime',
		'wsn': 'Western',
		'war': 'War',
		'doc': 'Documentary',
		'ani': 'Animation',
		'adv': 'Adventure',
		'fml': 'Family',
		'mus': 'Musical',
		'hst': 'History',
		'mys': 'Mystery',
		'bio': 'Biography',
		'spt': 'Sport',
	};
	
	function getGenreName(shortName: string): string {
		return genreMap[shortName] || shortName.toUpperCase();
	}
	
	function formatTechnology(tech: string | undefined): string {
		if (!tech) return '';
		
		return tech
			.split(',')
			.map(t => t.trim()
				.replace(/DOLBY_VISION/g, 'Dolby Vision')
				.replace(/DOLBY_ATMOS/g, 'Dolby Atmos')
				.replace(/DOLBY_5_POINT_1/g, 'Dolby 5.1')
				.replace(/_5_POINT_1/g, '5.1ch')
				.replace(/HDR10_PLUS/g, 'HDR10+')
				.replace(/HDR10/g, 'HDR10')
				.replace(/HDR/g, 'HDR')
				.replace(/_/g, ' ')
			)
			.join(', ');
	}
	
	function sortOffers(column: string) {
		if (sortColumn === column) {
			sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
		} else {
			sortColumn = column;
			sortDirection = 'asc';
		}
		
		filteredOffers = [...filteredOffers].sort((a, b) => {
			let aVal: any, bVal: any;
			
			switch(column) {
				case 'country':
					aVal = a.country;
					bVal = b.country;
					break;
				case 'provider':
					aVal = a.packageClearName || '';
					bVal = b.packageClearName || '';
					break;
				case 'type':
					aVal = a.monetizationType || '';
					bVal = b.monetizationType || '';
					break;
				case 'priceLocal':
					aVal = a.retailPriceValue || 0;
					bVal = b.retailPriceValue || 0;
					break;
				case 'priceUSD':
					aVal = a.normalizedPrice || 0;
					bVal = b.normalizedPrice || 0;
					break;
				case 'quality':
					aVal = a.presentationType || '';
					bVal = b.presentationType || '';
					break;
				default:
					return 0;
			}
			
			if (aVal < bVal) return sortDirection === 'asc' ? -1 : 1;
			if (aVal > bVal) return sortDirection === 'asc' ? 1 : -1;
			return 0;
		});
	}
	
	function applyFilters() {
		filteredOffers = offers.filter(offer => {
			// Filter out cinema/theatrical releases
			if (offer.monetizationType === 'CINEMA') return false;
			
			const matchCountry = !countryFilter || offer.country.toLowerCase().includes(countryFilter.toLowerCase());
			const matchProvider = !providerFilter || (offer.packageClearName?.toLowerCase().includes(providerFilter.toLowerCase()) ?? false);
			const matchType = !typeFilter || (offer.monetizationType?.toLowerCase().includes(typeFilter.toLowerCase()) ?? false);
			
			return matchCountry && matchProvider && matchType;
		});
	}
	
	$: {
		countryFilter;
		providerFilter;
		typeFilter;
		applyFilters();
	}
	
	onMount(async () => {
		if (!title && nodeId) {
			loading = true;
			try {
				title = await justWatchAPI.getTitle(nodeId);
			} catch (error) {
				console.error('Failed to load title:', error);
			} finally {
				loading = false;
			}
		}
		
		if (title?.content?.fullPath) {
			offersLoading = true;
			try {
				offers = await justWatchAPI.getTitleOffers(title.id, title.content.fullPath);
				filteredOffers = offers;
				
				// Log unique monetization types for debugging
				const types = new Set(offers.map(o => o.monetizationType).filter(Boolean));
				console.log('Available monetization types:', Array.from(types));
			} catch (error) {
				console.error('Failed to load offers:', error);
			} finally {
				offersLoading = false;
			}
		}
	});
	
	function goBack() {
		window.history.back();
	}
</script>


<div class="container mx-auto p-6 w-full">
	<div class="mb-6">
		<a href="/search" class="inline-flex items-center gap-2 text-blue-400 hover:text-blue-300 transition-colors">
			<span class="text-xl">←</span>
			<span>Back to Search</span>
		</a>
	</div>
	
	{#if loading}
		<div class="flex justify-center items-center py-12">
			<Spinner size="12" />
		</div>
	{:else if title && title.content}
		<!-- Title Header Card -->
		<div class="title-card mb-8">
			<div class="flex flex-col lg:flex-row gap-8">
				<!-- Poster -->
				{#if title.content.posterUrl}
					<div class="shrink-0">
						<img
							src="https://images.justwatch.com/{title.content.posterUrl}"
							alt={title.content.title}
							class="rounded-xl shadow-2xl w-full lg:w-80 object-cover"
						/>
					</div>
				{/if}
				
				<!-- Title Info -->
				<div class="flex-1 space-y-6">
					<div>
						<div class="flex items-center gap-3 mb-2">
							{#if title.objectType === 'MOVIE'}
								<Badge color="purple" class="text-sm font-semibold">🎬 Movie</Badge>
							{:else if title.objectType === 'SHOW'}
								<Badge color="pink" class="text-sm font-semibold">📺 TV Show</Badge>
							{/if}
						</div>
						<h1 class="text-4xl lg:text-5xl font-bold text-white mb-2">
							{title.content.title}
						</h1>
						{#if title.content.originalReleaseYear}
							<p class="text-2xl text-gray-300">
								{title.content.originalReleaseYear}
							</p>
						{/if}
					</div>

					{#if title.content.shortDescription}
						<p class="text-lg text-gray-200 leading-relaxed">
							{title.content.shortDescription}
						</p>
					{/if}

					<!-- Metadata Grid -->
					<div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4">
						{#if title.content.genres && title.content.genres.length > 0}
							<div>
								<h3 class="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-2">Genres</h3>
								<div class="flex flex-wrap gap-2">
									{#each title.content.genres as genre}
										<Badge color="indigo" class="text-sm">{getGenreName(genre.shortName)}</Badge>
									{/each}
								</div>
							</div>
						{/if}

						{#if title.content.runtime}
							<div>
								<h3 class="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-2">Runtime</h3>
								<p class="text-white text-lg">{title.content.runtime} minutes</p>
							</div>
						{/if}

						{#if title.content.productionCountries && title.content.productionCountries.length > 0}
							<div>
								<h3 class="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-2">Countries</h3>
								<p class="text-white text-lg">{title.content.productionCountries.join(', ')}</p>
							</div>
						{/if}

						{#if title.content.externalIds}
							<div>
								<h3 class="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-2">External Links</h3>
								<div class="flex gap-4">
									{#if title.content.externalIds.imdbId}
										<a
											href="https://www.imdb.com/title/{title.content.externalIds.imdbId}"
											target="_blank"
											rel="noopener noreferrer"
											class="px-4 py-2 bg-yellow-600 hover:bg-yellow-700 text-white rounded-lg font-semibold transition-colors"
										>
											IMDb
										</a>
									{/if}
									{#if title.content.externalIds.tmdbId}
										<a
											href="https://www.themoviedb.org/{title.objectType?.toLowerCase().replace('show', 'tv')}/{title.content.externalIds.tmdbId}"
											target="_blank"
											rel="noopener noreferrer"
											class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold transition-colors"
										>
											TMDb
										</a>
									{/if}
								</div>
							</div>
						{/if}
					</div>
				</div>
			</div>
		</div>
		
		<!-- Offers Section -->
		<div class="offers-section w-full">
			<h2 class="text-3xl font-bold mb-6 text-white flex items-center gap-3">
				<span class="text-4xl">🎬</span>
				Where to Watch
			</h2>
			
			{#if offersLoading}
				<div class="flex justify-center items-center py-12">
					<Spinner size="12" />
				</div>
			{:else if offers.length > 0}
				<!-- Filter inputs -->
				<div class="mb-4 grid grid-cols-1 md:grid-cols-3 gap-4">
					<Input
						type="text"
						placeholder="Filter by country..."
						bind:value={countryFilter}
						class="bg-gray-800 text-white border-gray-600"
					/>
					<Input
						type="text"
						placeholder="Filter by provider..."
						bind:value={providerFilter}
						class="bg-gray-800 text-white border-gray-600"
					/>
					<Input
						type="text"
						placeholder="Filter by type..."
						bind:value={typeFilter}
						class="bg-gray-800 text-white border-gray-600"
					/>
				</div>
				
				<div class="w-full overflow-x-auto rounded-xl">
					<Table striped={true} hoverable={true} class="dark-table w-full">
						<TableHead class="dark-table-head">
							<TableHeadCell>
								<button on:click={() => sortOffers('country')} class="flex items-center gap-2 hover:text-blue-400">
									Country
									{#if sortColumn === 'country'}
										<span>{sortDirection === 'asc' ? '↑' : '↓'}</span>
									{/if}
								</button>
							</TableHeadCell>
							<TableHeadCell>
								<button on:click={() => sortOffers('provider')} class="flex items-center gap-2 hover:text-blue-400">
									Provider
									{#if sortColumn === 'provider'}
										<span>{sortDirection === 'asc' ? '↑' : '↓'}</span>
									{/if}
								</button>
							</TableHeadCell>
							<TableHeadCell>
								<button on:click={() => sortOffers('type')} class="flex items-center gap-2 hover:text-blue-400">
									Type
									{#if sortColumn === 'type'}
										<span>{sortDirection === 'asc' ? '↑' : '↓'}</span>
									{/if}
								</button>
							</TableHeadCell>
							<TableHeadCell>
								<button on:click={() => sortOffers('priceLocal')} class="flex items-center gap-2 hover:text-blue-400">
									Price (Local)
									{#if sortColumn === 'priceLocal'}
										<span>{sortDirection === 'asc' ? '↑' : '↓'}</span>
									{/if}
								</button>
							</TableHeadCell>
							<TableHeadCell>
								<button on:click={() => sortOffers('priceUSD')} class="flex items-center gap-2 hover:text-blue-400">
									Price (USD)
									{#if sortColumn === 'priceUSD'}
										<span>{sortDirection === 'asc' ? '↑' : '↓'}</span>
									{/if}
								</button>
							</TableHeadCell>
							<TableHeadCell>
								<button on:click={() => sortOffers('quality')} class="flex items-center gap-2 hover:text-blue-400">
									Quality
									{#if sortColumn === 'quality'}
										<span>{sortDirection === 'asc' ? '↑' : '↓'}</span>
									{/if}
								</button>
							</TableHeadCell>
							<TableHeadCell>Languages</TableHeadCell>
							<TableHeadCell>Link</TableHeadCell>
						</TableHead>
						<TableBody class="dark-table-body">
							{#each filteredOffers as offer}
								<TableBodyRow class="dark-table-row">
								<TableBodyCell>
									<Badge color="gray">{offer.country}</Badge>
								</TableBodyCell>
									<TableBodyCell>{offer.packageClearName || 'N/A'}</TableBodyCell>
									<TableBodyCell>
										<Badge color={offer.monetizationType === 'BUY' ? 'blue' : offer.monetizationType === 'RENT' ? 'yellow' : 'green'}>
											{offer.monetizationType || 'N/A'}
										</Badge>
									</TableBodyCell>
									<TableBodyCell>{offer.retailPrice || 'N/A'}</TableBodyCell>
									<TableBodyCell>
										{#if offer.normalizedPrice && offer.normalizedPrice !== 999}
											${offer.normalizedPrice.toFixed(2)}
										{:else if offer.normalizedPrice === 0}
											Free
										{:else}
											N/A
										{/if}
									</TableBodyCell>
									<TableBodyCell>
										<div class="text-xs">
											{offer.presentationType?.replace('_4K', '4K') || 'N/A'}
											{#if offer.technology}
												<br /><span class="text-gray-400">{formatTechnology(offer.technology)}</span>
											{/if}
										</div>
									</TableBodyCell>
									<TableBodyCell>
										<div class="text-xs min-w-[150px] max-w-[200px] whitespace-normal break-words">
											{#if offer.audioLanguages}
												<div class="mb-1">🔊 {offer.audioLanguages}</div>
											{/if}
											{#if offer.subtitleLanguages}
												<div>📝 {offer.subtitleLanguages}</div>
											{/if}
										</div>
									</TableBodyCell>
									<TableBodyCell>
										{#if offer.packageUrl}
											<Button
												size="xs"
												color="blue"
												href={offer.packageUrl}
												target="_blank"
												rel="noopener noreferrer"
											>
												Watch
											</Button>
										{:else}
											N/A
										{/if}
									</TableBodyCell>
								</TableBodyRow>
							{/each}
						</TableBody>
					</Table>
				</div>
			{:else}
				<div class="no-offers-card">
					<div class="text-center py-12">
						<span class="text-6xl mb-4 block">🎭</span>
						<p class="text-xl text-gray-300">
							No streaming offers available for this title.
						</p>
					</div>
				</div>
			{/if}
		</div>
	{/if}
</div>

<style>
	:global(body) {
		background: linear-gradient(180deg, rgb(5, 39, 103) 0%, #3a0647 70%);
		min-height: 100vh;
	}

	.title-card {
		background: rgba(17, 24, 39, 0.95);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 1rem;
		padding: 2rem;
		box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
	}

	.offers-section {
		background: rgba(17, 24, 39, 0.8);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 1rem;
		padding: 2rem;
	}

	.no-offers-card {
		background: rgba(31, 41, 55, 0.5);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 1rem;
		padding: 2rem;
	}

	:global(.dark-table) {
		background-color: rgba(17, 24, 39, 0.95) !important;
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 0.5rem;
		overflow: hidden;
	}

	:global(.dark-table-head) {
		background-color: rgba(31, 41, 55, 0.95) !important;
	}

	:global(.dark-table-head th) {
		color: rgba(255, 255, 255, 0.95) !important;
		font-weight: 600 !important;
		border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
	}

	:global(.dark-table-body td) {
		color: rgba(255, 255, 255, 0.9) !important;
		border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
	}

	:global(.dark-table-row) {
		background-color: rgba(17, 24, 39, 0.5) !important;
	}

	:global(.dark-table-row:hover) {
		background-color: rgba(31, 41, 55, 0.7) !important;
	}

	:global(.dark-table-row:nth-child(even)) {
		background-color: rgba(31, 41, 55, 0.3) !important;
	}

	:global(.dark-table-row:nth-child(even):hover) {
		background-color: rgba(31, 41, 55, 0.7) !important;
	}
</style>
