const API_BASE = (import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000").replace(/\/$/, "");

async function request(path, { signal } = {}) {
  const response = await fetch(`${API_BASE}${path}`, { signal });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(body.detail || "Terjadi kesalahan saat menghubungi server.");
  }
  return body;
}

export const api = {
  products: ({ q = "", page = 1, perPage = 48, signal } = {}) =>
    request(`/products?page=${page}&per_page=${perPage}&q=${encodeURIComponent(q)}`, { signal }),
  product: (id) => request(`/products/${id}`),
  dupes: (id, maxPrice, limit = 5) =>
    request(`/products/${id}/dupes?max_price=${maxPrice}&limit=${limit}`),
  affiliateUrl: (path) => new URL(path, API_BASE).toString(),
  health: () => request("/health"),
};
