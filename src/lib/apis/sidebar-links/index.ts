import { WEBUI_API_BASE_URL } from '$lib/constants';

export const getSidebarLinks = async (token: string) => {
	let error = null;
	const res = await fetch(`${WEBUI_API_BASE_URL}/sidebar-links`, {
		method: 'GET',
		headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` }
	})
		.then(async (res) => { if (!res.ok) throw await res.json(); return res.json(); })
		.catch((err) => { console.error(err); error = err.detail; return null; });
	if (error) throw error;
	return res;
};

export const createSidebarLink = async (token: string, data: { title: string; url: string; icon?: string; sort_order?: number }) => {
	let error = null;
	const res = await fetch(`${WEBUI_API_BASE_URL}/sidebar-links/create`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
		body: JSON.stringify(data)
	})
		.then(async (res) => { if (!res.ok) throw await res.json(); return res.json(); })
		.catch((err) => { console.error(err); error = err.detail; return null; });
	if (error) throw error;
	return res;
};

export const updateSidebarLink = async (token: string, id: string, data: { title: string; url: string; icon?: string; sort_order?: number }) => {
	let error = null;
	const res = await fetch(`${WEBUI_API_BASE_URL}/sidebar-links/${id}/update`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
		body: JSON.stringify(data)
	})
		.then(async (res) => { if (!res.ok) throw await res.json(); return res.json(); })
		.catch((err) => { console.error(err); error = err.detail; return null; });
	if (error) throw error;
	return res;
};

export const deleteSidebarLink = async (token: string, id: string) => {
	let error = null;
	const res = await fetch(`${WEBUI_API_BASE_URL}/sidebar-links/${id}`, {
		method: 'DELETE',
		headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` }
	})
		.then(async (res) => { if (!res.ok) throw await res.json(); return res.json(); })
		.catch((err) => { console.error(err); error = err.detail; return null; });
	if (error) throw error;
	return res;
};
