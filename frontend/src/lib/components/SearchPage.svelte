<script lang="ts">
	import { Input, Button, Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell, Spinner, Badge } from 'flowbite-svelte';
	import { SearchOutline } from 'flowbite-svelte-icons';
	import { justWatchAPI, type SearchTitlesResponse, type TitleNode } from '$lib/api/justwatch';
	import { onMount } from 'svelte';
	
	let searchQuery = '';
	let searchResponse: SearchTitlesResponse | null = null;
	let loading = false;
	
	onMount(() => {
		searchMovies('');
	});
	
	let debounceTimer: ReturnType<typeof setTimeout>;
	
	function handleInput() {
		clearTimeout(debounceTimer);
		debounceTimer = setTimeout(() => {
			searchMovies(searchQuery);
		}, 300);
	}
	
	async function searchMovies(query: string) {
		loading = true;
		try {
			searchResponse = await justWatchAPI.searchTitles(query, 'US');
		} catch (error) {
			console.error('Search failed:', error);
		} finally {
			loading = false;
		}
	}
</script>

<div class="container mx-auto p-6">
	<h1 class="text-3xl font-bold mb-6 text-white">JustWatch Search</h1>
	
	<div class="mb-6">
		<Input
			bind:value={searchQuery}
			oninput={handleInput}
			placeholder="Enter movie/show title..."
			size="lg"
			class="mb-4"
		/>
	</div>
	
	{#if loading}
		<div class="flex justify-center items-center py-12">
			<Spinner size="12" />
		</div>
	{:else if searchResponse}
		<div class="overflow-x-auto">
			<Table striped={true} hoverable={true} color="custom" class="dark-table">
				<TableHead class="dark-table-head">
					<TableHeadCell>Type</TableHeadCell>
					<TableHeadCell>Title</TableHeadCell>
					<TableHeadCell>Release</TableHeadCell>
					<TableHeadCell>Countries</TableHeadCell>
					<TableHeadCell>IMDB</TableHeadCell>
					<TableHeadCell>TMDB</TableHeadCell>
					<TableHeadCell>Actions</TableHeadCell>
				</TableHead>
				<TableBody class="dark-table-body">
					{#each searchResponse.popularTitles.edges as { node }}
						<TableBodyRow class="dark-table-row">
							<TableBodyCell>
								<Badge color={node.objectType === 'MOVIE' ? 'blue' : 'green'}>
									{node.objectType}
								</Badge>
							</TableBodyCell>
							<TableBodyCell>{node.content?.title || 'N/A'}</TableBodyCell>
							<TableBodyCell>{node.content?.originalReleaseYear || 'N/A'}</TableBodyCell>
							<TableBodyCell>
								{node.content?.productionCountries?.join(', ') || 'N/A'}
							</TableBodyCell>
							<TableBodyCell>
								{#if node.content?.externalIds?.imdbId}
									<a
										href="https://www.imdb.com/title/{node.content.externalIds.imdbId}"
										target="_blank"
										rel="noopener noreferrer"
										class="text-blue-400 hover:text-blue-300 hover:underline"
									>
										{node.content.externalIds.imdbId}
									</a>
								{:else}
									N/A
								{/if}
							</TableBodyCell>
							<TableBodyCell>
								{#if node.content?.externalIds?.tmdbId}
									<a
										href="https://www.themoviedb.org/{node.objectType?.toLowerCase().replace('show', 'tv')}/{node.content.externalIds.tmdbId}"
										target="_blank"
										rel="noopener noreferrer"
										class="text-blue-400 hover:text-blue-300 hover:underline"
									>
										{node.content.externalIds.tmdbId}
									</a>
								{:else}
									N/A
								{/if}
							</TableBodyCell>
							<TableBodyCell>
							<div class="flex gap-2">
								{#if node.content?.fullPath}
									<a href="/title/{node.id}" class="inline-block">
										<Button size="sm" color="blue">
											View Offers
										</Button>
									</a>
								{:else}
									<Button size="sm" color="blue" disabled>
										No Offers
									</Button>
								{/if}
									{#if node.content?.fullPath}
										<Button
											size="sm"
											color="light"
											href="https://justwatch.com{node.content.fullPath}"
											target="_blank"
										>
											JustWatch
										</Button>
									{/if}
								</div>
							</TableBodyCell>
						</TableBodyRow>
					{/each}
				</TableBody>
			</Table>
		</div>
	{/if}
</div>

<style>
	:global(body) {
		background: linear-gradient(180deg, rgb(5, 39, 103) 0%, #3a0647 70%);
		min-height: 100vh;
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
