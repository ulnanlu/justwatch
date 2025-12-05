<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<div class="app">
	<nav class="navbar">
		<div class="container">
			<a href="/" class="brand">
				<span class="logo">🎬</span>
				JustWatch Search
			</a>
			<div class="nav-items">
				<a href="/search" class="nav-link">Search</a>
			</div>
		</div>
	</nav>

	<main>
		{@render children()}
	</main>
</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}

	.navbar {
		background: rgba(17, 24, 39, 0.95);
		backdrop-filter: blur(10px);
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
		padding: 1rem 0;
		position: sticky;
		top: 0;
		z-index: 1000;
	}

	.container {
		max-width: 1400px;
		margin: 0 auto;
		padding: 0 1.5rem;
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

	.brand {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		font-size: 1.5rem;
		font-weight: 700;
		color: white;
		text-decoration: none;
		transition: opacity 0.2s;
	}

	.brand:hover {
		opacity: 0.8;
	}

	.logo {
		font-size: 2rem;
	}

	.nav-items {
		display: flex;
		align-items: center;
		gap: 2rem;
	}

	.nav-link {
		color: rgba(255, 255, 255, 0.9);
		text-decoration: none;
		font-weight: 500;
		transition: color 0.2s;
		font-size: 1rem;
	}

	.nav-link:hover {
		color: white;
	}

	main {
		flex: 1;
	}

	@media (max-width: 768px) {
		.container {
			flex-direction: column;
			gap: 1rem;
		}

		.nav-items {
			width: 100%;
			justify-content: center;
			gap: 1rem;
		}

		.brand {
			font-size: 1.25rem;
		}
	}
</style>
