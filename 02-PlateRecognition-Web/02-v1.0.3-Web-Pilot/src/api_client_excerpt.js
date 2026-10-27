// Selected API helper only; UI, event handlers and startup omitted.
async function api(url, options = {}) {
  const response = await fetch(url, {
    headers: {'Content-Type': 'application/json'},
    ...options,
  });
  const data = await response.json().catch(() => ({ok:false, message:'پاسخ برنامه قابل خواندن نیست.'}));
  if (!response.ok || data.ok === false) throw new Error(data.message || 'عملیات انجام نشد.');
  return data;
}

