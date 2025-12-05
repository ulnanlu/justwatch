<script lang="ts">
	import TitleDetail from '$lib/components/TitleDetail.svelte';
	import { page } from '$app/stores';
	
	$: nodeId = $page.params.id || '';
</script>

<svelte:head>
	<title>Title Details - JustWatch Search</title>
</svelte:head>

{#if nodeId}
	<TitleDetail {nodeId} />
{/if}
