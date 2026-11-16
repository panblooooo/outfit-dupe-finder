import { useCallback, useEffect, useMemo, useState } from "react";
import { api } from "./api";

const CATEGORIES = ["Semua", "Atasan", "Bawahan", "Dress", "Outer"];
const formatPrice = (value) => new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR", maximumFractionDigits: 0 }).format(value || 0);
const productName = (p) => p?.nama_produk || "Produk fashion";
const brandName = (p) => p?.brand || p?.brand_lokal || "Brand lokal";
const attributes = (obj = {}) => [
  ["Kategori", obj.kategori || obj.category || "Fashion"],
  ["Bahan", (obj.bahan || []).join?.(", ") || obj.bahan || "—"],
  ["Warna", (obj.warna || []).join?.(", ") || obj.warna || "—"],
  ["Potongan", (obj.fit || []).join?.(", ") || obj.fit || "—"],
];

function Logo() { return <a className="logo" href="#" onClick={(e) => { e.preventDefault(); window.location.hash = ""; }}>Dupe finder<span>.</span></a>; }

function ImagePanel({ src, className = "", label = "Outfit" }) {
  return <div className={`image-panel ${className}`}>
    {src ? <img src={src} alt={label} loading="lazy" /> : <div className="image-placeholder"><span>DF</span><small>STYLE, MADE LOCAL</small></div>}
  </div>;
}

function Header({ onHome }) {
  return <header className="site-header"><button className="logo-button" onClick={onHome}><Logo /></button><span className="header-note">DISCOVER YOUR NEXT LOOK</span></header>;
}

function ProductCard({ product, onSelect }) {
  return <button className="product-card" onClick={() => onSelect(product)} aria-label={`Lihat ${productName(product)}`}>
    <div className="card-image-wrap">
      <ImagePanel src={product.image_url} label={productName(product)} />
      <span className="dupe-tag">FIND YOUR DUPE</span>
      <span className="card-arrow">↗</span>
    </div>
    <div className="product-info">
      <span className="eyebrow">{brandName(product)}</span>
      <strong>{productName(product)}</strong>
      <span className="product-price">{formatPrice(product.harga)}</span>
    </div>
  </button>;
}

function Catalog({ onSelect }) {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("Semua");
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadProducts = useCallback(async (q) => {
    setLoading(true); setError("");
    try {
      const result = await api.products({ q, perPage: 48 });
      setProducts(result.data || []);
    } catch (err) { setError(err.message); setProducts([]); }
    finally { setLoading(false); }
  }, []);

  useEffect(() => { const timer = setTimeout(() => loadProducts(query), 250); return () => clearTimeout(timer); }, [query, loadProducts]);

  const visibleProducts = useMemo(() => category === "Semua" ? products : products.filter((p) => (p.kategori || "").toLowerCase() === category.toLowerCase()), [products, category]);

  return <main className="catalog-page">
    <section className="hero">
      <p className="overline">THE SMARTER WAY TO STYLE</p>
      <h1>Gaya High-End,<br /><em>Harga Lokal.</em></h1>
      <p className="hero-copy">Pilih outfit impianmu, kami carikan dupe-nya.</p>
      <label className="search-box"><span className="search-icon">⌕</span><input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Cari blazer, dress, brand..." /><kbd>⌘ K</kbd></label>
    </section>
    <section className="catalog-content">
      <div className="section-heading"><div><p className="overline">CURATED FOR YOU</p><h2>Temukan gayamu</h2></div><span className="result-count">{visibleProducts.length} produk</span></div>
      <div className="category-row">{CATEGORIES.map((item) => <button key={item} onClick={() => setCategory(item)} className={category === item ? "category-chip active" : "category-chip"}>{item}</button>)}</div>
      {loading ? <div className="state-message">Sedang memuat katalog...</div> : error ? <div className="state-message error"><strong>Belum bisa memuat produk.</strong><span>{error}</span><small>Pastikan backend FastAPI berjalan di alamat API yang dikonfigurasi.</small></div> : visibleProducts.length ? <div className="product-grid">{visibleProducts.map((p) => <ProductCard key={p.id} product={p} onSelect={onSelect} />)}</div> : <div className="state-message">Produk belum ditemukan. Coba kata kunci lain.</div>}
    </section>
  </main>;
}

function Detail({ productId, onBack, onCompare }) {
  const [product, setProduct] = useState(null);
  const [budget, setBudget] = useState(350000);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  useEffect(() => {
    let active = true; setLoading(true); setError("");
    api.product(productId).then((data) => {
      if (!active) return;
      setProduct(data);
      const max = Math.min(500000, data.budget_range?.max || 500000);
      setBudget(Math.min(350000, max));
    }).catch((err) => active && setError(err.message)).finally(() => active && setLoading(false));
    return () => { active = false; };
  }, [productId]);
  if (loading) return <div className="state-message page-state">Memuat detail produk...</div>;
  if (error || !product) return <div className="state-message page-state error">{error || "Produk tidak ditemukan."}<button className="text-button" onClick={onBack}>Kembali ke katalog</button></div>;
  const min = product.budget_range?.min || 100000;
  const max = Math.min(500000, product.budget_range?.max || 500000);
  const attrs = product.attributes || {};
  return <main className="detail-page">
    <button className="back-link" onClick={onBack}>← Kembali ke katalog</button>
    <div className="detail-layout">
      <ImagePanel src={product.image_url} className="detail-image" label={productName(product)} />
      <section className="detail-copy">
        <p className="overline">THE ORIGINAL PIECE</p><h1>{productName(product)}</h1><p className="detail-brand">{product.brand}</p><p className="detail-price">{formatPrice(product.harga)}</p>
        <div className="attribute-grid">{attributes({ ...attrs, kategori: product.kategori }).map(([label, value]) => <div className="attribute-box" key={label}><span>{label}</span><strong>{value}</strong></div>)}</div>
        <div className="budget-panel"><div className="budget-heading"><span>Batas harga maksimal dupe</span><strong>{formatPrice(budget)}</strong></div><input className="budget-slider" type="range" min={min} max={Math.max(min + 1, max)} step="10000" value={Math.min(budget, max)} onChange={(e) => setBudget(Number(e.target.value))} /><div className="range-labels"><span>{formatPrice(min)}</span><span>{formatPrice(max)}</span></div></div>
        <button className="primary-button" onClick={() => onCompare(product, budget)}>Temukan dupe untukku <span>→</span></button>
      </section>
    </div>
  </main>;
}

function Comparison({ product, budget, onBack }) {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  useEffect(() => {
    let active = true; setLoading(true); setError("");
    api.dupes(product.id, budget).then((data) => active && setResult(data.data)).catch((err) => active && setError(err.message)).finally(() => active && setLoading(false));
    return () => { active = false; };
  }, [product.id, budget]);
  return <main className="comparison-page">
    <button className="back-link" onClick={onBack}>← Kembali ke detail</button>
    <div className="comparison-title"><p className="overline">THE LOOK, REIMAGINED</p><h1>Looks like it. Costs less.</h1><p>Alternatif lokal yang punya vibe serupa, tanpa harga high-end.</p></div>
    <div className="comparison-layout">
      <section className="reference-column"><h2>Produk Acuan</h2><article className="reference-card"><ImagePanel src={product.image_url} label={productName(product)} /><div><span className="eyebrow">{product.brand}</span><h3>{productName(product)}</h3><strong>{formatPrice(product.harga)}</strong></div></article></section>
      <section className="dupe-column"><div className="dupe-heading"><div><p className="overline">YOUR LOCAL FINDS</p><h2>Dupe pilihan</h2></div><span className="budget-pill">Di bawah {formatPrice(budget)}</span></div>
        {loading ? <div className="state-message">Mencari alternatif terbaik...</div> : error ? <div className="state-message error">{error}</div> : result?.results?.length ? <div className="dupe-grid">{result.results.map((item) => <article className="dupe-card" key={item.id}><div className="dupe-image"><ImagePanel src={item.image_url} label={item.nama_produk} /><span className="match-tag">{item.similarity?.percent ?? 0}% match</span></div><div className="dupe-info"><span className="eyebrow">{item.brand_lokal}</span><h3>{item.nama_produk}</h3><strong>{formatPrice(item.harga)}</strong><p className="saving-copy">Hemat {formatPrice(item.price_diff?.nominal)}</p><a className="buy-button" href={api.affiliateUrl(item.buy_url)} target="_blank" rel="noreferrer">Beli Dupe <span>↗</span></a></div></article>)}</div> : <div className="empty-dupes"><span>✳</span><h3>Belum ada dupe yang cocok</h3><p>Coba naikkan batas harga atau pilih produk acuan lainnya.</p></div>}
      </section>
    </div>
  </main>;
}

export default function App() {
  const [selected, setSelected] = useState(null);
  const [comparison, setComparison] = useState(null);
  const [budget, setBudget] = useState(350000);
  const [health, setHealth] = useState("checking");
  const goHome = () => { setSelected(null); setComparison(null); };
  useEffect(() => { api.health().then(() => setHealth("online")).catch(() => setHealth("offline")); }, []);
  return <div className="app-shell"><Header onHome={goHome} /><div className="api-status"><span className={health === "online" ? "status-dot online" : "status-dot"} />{health === "online" ? "API terhubung" : health === "offline" ? "API offline" : "Menghubungkan API"}</div>
    {comparison && selected ? <Comparison product={selected} budget={budget} onBack={() => setComparison(null)} /> : selected ? <Detail productId={selected.id} onBack={goHome} onCompare={(p, b) => { setSelected(p); setBudget(b); setComparison(true); }} /> : <Catalog onSelect={(p) => setSelected(p)} />}
    <footer className="site-footer"><span>DUPE FINDER</span><span>Gaya lebih cerdas, dukung brand lokal.</span><span>© 2026</span></footer>
  </div>;
}