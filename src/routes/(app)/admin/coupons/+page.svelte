<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import { toast } from 'svelte-sonner';
	import dayjs from 'dayjs';
	import localizedFormat from 'dayjs/plugin/localizedFormat';
	dayjs.extend(localizedFormat);

	import { getCoupons, createCoupon, createBulkCoupons, deleteCoupon } from '$lib/apis/coupons';
	import Modal from '$lib/components/common/Modal.svelte';

	const i18n = getContext('i18n');

	let coupons: any[] = [];
	let showCreateModal = false;
	let showBulkModal = false;

	// Single coupon form
	let newCode = '';
	let newDays = 30;
	let newMaxUsage = 1;
	let newNote = '';

	// Bulk coupon form
	let bulkCount = 10;
	let bulkDays = 30;
	let bulkMaxUsage = 1;
	let bulkPrefix = '';
	let bulkNote = '';

	const loadCoupons = async () => {
		const res = await getCoupons(localStorage.token).catch((e) => {
			toast.error(`${e}`);
			return null;
		});
		if (res) coupons = res;
	};

	const handleCreate = async () => {
		const res = await createCoupon(localStorage.token, {
			code: newCode,
			days: newDays,
			max_usage: newMaxUsage,
			note: newNote
		}).catch((e) => { toast.error(`${e}`); return null; });
		if (res) {
			toast.success('Kupon oluşturuldu');
			showCreateModal = false;
			newCode = ''; newDays = 30; newMaxUsage = 1; newNote = '';
			loadCoupons();
		}
	};

	const handleBulkCreate = async () => {
		const res = await createBulkCoupons(localStorage.token, {
			count: bulkCount,
			days: bulkDays,
			max_usage: bulkMaxUsage,
			prefix: bulkPrefix,
			note: bulkNote
		}).catch((e) => { toast.error(`${e}`); return null; });
		if (res) {
			toast.success(`${res.length} kupon oluşturuldu`);
			showBulkModal = false;
			bulkCount = 10; bulkDays = 30; bulkMaxUsage = 1; bulkPrefix = ''; bulkNote = '';
			loadCoupons();
		}
	};

	const handleDelete = async (id: string) => {
		const res = await deleteCoupon(localStorage.token, id).catch((e) => {
			toast.error(`${e}`);
			return null;
		});
		if (res) {
			toast.success('Kupon silindi');
			loadCoupons();
		}
	};

	onMount(() => { loadCoupons(); });
</script>

<div class="p-6 max-w-6xl mx-auto">
	<div class="flex items-center justify-between mb-6">
		<h1 class="text-2xl font-bold">🎟️ Kupon Yönetimi</h1>
		<div class="flex gap-2">
			<button
				class="px-4 py-2 text-sm font-medium bg-blue-500 hover:bg-blue-600 text-white rounded-lg"
				on:click={() => (showCreateModal = true)}
			>
				+ Tekli Kupon
			</button>
			<button
				class="px-4 py-2 text-sm font-medium bg-purple-500 hover:bg-purple-600 text-white rounded-lg"
				on:click={() => (showBulkModal = true)}
			>
				+ Toplu Kupon
			</button>
		</div>
	</div>

	<div class="overflow-x-auto rounded-lg border border-gray-200 dark:border-gray-700">
		<table class="w-full text-sm text-left">
			<thead class="text-xs uppercase bg-gray-50 dark:bg-gray-800 text-gray-500">
				<tr>
					<th class="px-4 py-3">Kod</th>
					<th class="px-4 py-3">Gün</th>
					<th class="px-4 py-3">Kullanım</th>
					<th class="px-4 py-3">Not</th>
					<th class="px-4 py-3">Oluşturulma</th>
					<th class="px-4 py-3 text-right">İşlem</th>
				</tr>
			</thead>
			<tbody>
				{#if coupons.length === 0}
					<tr>
						<td colspan="6" class="px-4 py-8 text-center text-gray-400">Henüz kupon yok</td>
					</tr>
				{/if}
				{#each coupons as coupon (coupon.id)}
					<tr class="border-t border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-850">
						<td class="px-4 py-3">
							<code class="bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded text-xs font-mono">{coupon.code}</code>
						</td>
						<td class="px-4 py-3 font-medium">{coupon.days}</td>
						<td class="px-4 py-3">
							<span class="{coupon.current_usage >= coupon.max_usage ? 'text-red-500' : 'text-green-500'} font-medium">
								{coupon.current_usage}/{coupon.max_usage}
							</span>
						</td>
						<td class="px-4 py-3 text-gray-500 max-w-48 truncate">{coupon.note || '—'}</td>
						<td class="px-4 py-3 text-gray-500">{dayjs(coupon.created_at * 1000).format('LL')}</td>
						<td class="px-4 py-3 text-right">
							<button
								class="text-red-500 hover:text-red-700 text-xs font-medium"
								on:click={() => handleDelete(coupon.id)}
							>
								Sil
							</button>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>

<!-- Tekli Kupon Modal -->
<Modal size="sm" bind:show={showCreateModal}>
	<div class="p-5">
		<h2 class="text-lg font-semibold mb-4">Tekli Kupon Oluştur</h2>
		<form on:submit|preventDefault={handleCreate} class="flex flex-col gap-3">
			<div>
				<label class="text-xs text-gray-500 mb-1 block">Kupon Kodu</label>
				<input class="w-full text-sm bg-transparent border border-gray-200 dark:border-gray-700 rounded px-3 py-2 outline-hidden" type="text" bind:value={newCode} placeholder="KUPON2024" required />
			</div>
			<div class="flex gap-3">
				<div class="flex-1">
					<label class="text-xs text-gray-500 mb-1 block">Gün Sayısı</label>
					<input class="w-full text-sm bg-transparent border border-gray-200 dark:border-gray-700 rounded px-3 py-2 outline-hidden" type="number" min="1" bind:value={newDays} required />
				</div>
				<div class="flex-1">
					<label class="text-xs text-gray-500 mb-1 block">Max Kullanım</label>
					<input class="w-full text-sm bg-transparent border border-gray-200 dark:border-gray-700 rounded px-3 py-2 outline-hidden" type="number" min="1" bind:value={newMaxUsage} required />
				</div>
			</div>
			<div>
				<label class="text-xs text-gray-500 mb-1 block">Not (opsiyonel)</label>
				<input class="w-full text-sm bg-transparent border border-gray-200 dark:border-gray-700 rounded px-3 py-2 outline-hidden" type="text" bind:value={newNote} placeholder="Açıklama..." />
			</div>
			<button type="submit" class="mt-2 px-4 py-2 text-sm font-medium bg-blue-500 hover:bg-blue-600 text-white rounded-lg">Oluştur</button>
		</form>
	</div>
</Modal>

<!-- Toplu Kupon Modal -->
<Modal size="sm" bind:show={showBulkModal}>
	<div class="p-5">
		<h2 class="text-lg font-semibold mb-4">Toplu Kupon Oluştur</h2>
		<form on:submit|preventDefault={handleBulkCreate} class="flex flex-col gap-3">
			<div class="flex gap-3">
				<div class="flex-1">
					<label class="text-xs text-gray-500 mb-1 block">Adet</label>
					<input class="w-full text-sm bg-transparent border border-gray-200 dark:border-gray-700 rounded px-3 py-2 outline-hidden" type="number" min="1" max="1000" bind:value={bulkCount} required />
				</div>
				<div class="flex-1">
					<label class="text-xs text-gray-500 mb-1 block">Gün Sayısı</label>
					<input class="w-full text-sm bg-transparent border border-gray-200 dark:border-gray-700 rounded px-3 py-2 outline-hidden" type="number" min="1" bind:value={bulkDays} required />
				</div>
			</div>
			<div class="flex gap-3">
				<div class="flex-1">
					<label class="text-xs text-gray-500 mb-1 block">Max Kullanım</label>
					<input class="w-full text-sm bg-transparent border border-gray-200 dark:border-gray-700 rounded px-3 py-2 outline-hidden" type="number" min="1" bind:value={bulkMaxUsage} required />
				</div>
				<div class="flex-1">
					<label class="text-xs text-gray-500 mb-1 block">Kod Öneki (opsiyonel)</label>
					<input class="w-full text-sm bg-transparent border border-gray-200 dark:border-gray-700 rounded px-3 py-2 outline-hidden" type="text" bind:value={bulkPrefix} placeholder="VIP" />
				</div>
			</div>
			<div>
				<label class="text-xs text-gray-500 mb-1 block">Not (opsiyonel)</label>
				<input class="w-full text-sm bg-transparent border border-gray-200 dark:border-gray-700 rounded px-3 py-2 outline-hidden" type="text" bind:value={bulkNote} placeholder="Toplu kampanya..." />
			</div>
			<button type="submit" class="mt-2 px-4 py-2 text-sm font-medium bg-purple-500 hover:bg-purple-600 text-white rounded-lg">Oluştur</button>
		</form>
	</div>
</Modal>
