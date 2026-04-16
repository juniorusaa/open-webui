<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import { toast } from 'svelte-sonner';
	import { getSidebarLinks, createSidebarLink, updateSidebarLink, deleteSidebarLink } from '$lib/apis/sidebar-links';
	import Modal from '$lib/components/common/Modal.svelte';

	const i18n = getContext('i18n');

	let links: any[] = [];
	let showModal = false;
	let editingLink: any = null;

	let formTitle = '';
	let formUrl = '';
	let formIcon = '';
	let formSortOrder = 0;

	const loadLinks = async () => {
		const res = await getSidebarLinks(localStorage.token).catch((e) => {
			toast.error(`${e}`);
			return null;
		});
		if (res) links = res;
	};

	const openCreate = () => {
		editingLink = null;
		formTitle = '';
		formUrl = '';
		formIcon = '';
		formSortOrder = links.length;
		showModal = true;
	};

	const openEdit = (link: any) => {
		editingLink = link;
		formTitle = link.title;
		formUrl = link.url;
		formIcon = link.icon || '';
		formSortOrder = link.sort_order;
		showModal = true;
	};

	const handleSubmit = async () => {
		const data = { title: formTitle, url: formUrl, icon: formIcon || null, sort_order: formSortOrder };
		let res;
		if (editingLink) {
			res = await updateSidebarLink(localStorage.token, editingLink.id, data).catch((e) => {
				toast.error(`${e}`);
				return null;
			});
			if (res) toast.success('Link güncellendi');
		} else {
			res = await createSidebarLink(localStorage.token, data).catch((e) => {
				toast.error(`${e}`);
				return null;
			});
			if (res) toast.success('Link eklendi');
		}
		if (res) {
			showModal = false;
			loadLinks();
		}
	};

	const handleDelete = async (id: string) => {
		const res = await deleteSidebarLink(localStorage.token, id).catch((e) => {
			toast.error(`${e}`);
			return null;
		});
		if (res) {
			toast.success('Link silindi');
			loadLinks();
		}
	};

	onMount(() => { loadLinks(); });
</script>

<div class="p-6 max-w-4xl mx-auto">
	<div class="flex items-center justify-between mb-6">
		<h1 class="text-2xl font-bold">🔗 Sidebar Menü Linkleri</h1>
		<button
			class="px-4 py-2 text-sm font-medium bg-blue-500 hover:bg-blue-600 text-white rounded-lg"
			on:click={openCreate}
		>
			+ Yeni Link
		</button>
	</div>

	<p class="text-sm text-gray-500 mb-4">Sidebar'da "Menü" bölümünde görünecek özel linkler. Tıklandığında yeni sekmede açılır.</p>

	<div class="space-y-2">
		{#if links.length === 0}
			<div class="text-center text-gray-400 py-12 border border-dashed border-gray-300 dark:border-gray-700 rounded-lg">
				Henüz link eklenmedi
			</div>
		{/if}

		{#each links as link (link.id)}
			<div class="flex items-center justify-between p-4 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-gray-300 dark:hover:border-gray-600 transition">
				<div class="flex items-center gap-3">
					<span class="text-xl">{link.icon || '🔗'}</span>
					<div>
						<div class="font-medium">{link.title}</div>
						<div class="text-xs text-gray-500 truncate max-w-sm">{link.url}</div>
					</div>
				</div>
				<div class="flex gap-2">
					<button
						class="px-3 py-1 text-xs font-medium text-blue-500 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded"
						on:click={() => openEdit(link)}
					>
						Düzenle
					</button>
					<button
						class="px-3 py-1 text-xs font-medium text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded"
						on:click={() => handleDelete(link.id)}
					>
						Sil
					</button>
				</div>
			</div>
		{/each}
	</div>
</div>

<Modal size="sm" bind:show={showModal}>
	<div class="p-5">
		<h2 class="text-lg font-semibold mb-4">{editingLink ? 'Link Düzenle' : 'Yeni Link Ekle'}</h2>
		<form on:submit|preventDefault={handleSubmit} class="flex flex-col gap-3">
			<div>
				<label class="text-xs text-gray-500 mb-1 block">Başlık</label>
				<input class="w-full text-sm bg-transparent border border-gray-200 dark:border-gray-700 rounded px-3 py-2 outline-hidden" type="text" bind:value={formTitle} placeholder="YouTube" required />
			</div>
			<div>
				<label class="text-xs text-gray-500 mb-1 block">URL</label>
				<input class="w-full text-sm bg-transparent border border-gray-200 dark:border-gray-700 rounded px-3 py-2 outline-hidden" type="url" bind:value={formUrl} placeholder="https://youtube.com" required />
			</div>
			<div class="flex gap-3">
				<div class="flex-1">
					<label class="text-xs text-gray-500 mb-1 block">Emoji İkon (opsiyonel)</label>
					<input class="w-full text-sm bg-transparent border border-gray-200 dark:border-gray-700 rounded px-3 py-2 outline-hidden" type="text" bind:value={formIcon} placeholder="🎬" />
				</div>
				<div class="flex-1">
					<label class="text-xs text-gray-500 mb-1 block">Sıralama</label>
					<input class="w-full text-sm bg-transparent border border-gray-200 dark:border-gray-700 rounded px-3 py-2 outline-hidden" type="number" bind:value={formSortOrder} />
				</div>
			</div>
			<button type="submit" class="mt-2 px-4 py-2 text-sm font-medium bg-blue-500 hover:bg-blue-600 text-white rounded-lg">
				{editingLink ? 'Güncelle' : 'Ekle'}
			</button>
		</form>
	</div>
</Modal>
