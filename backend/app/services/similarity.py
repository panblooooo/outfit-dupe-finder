import math

ATTR_ORDER = ["warna", "bahan", "fit", "style"]
WEIGHTS = {"warna": 0.35, "bahan": 0.30, "fit": 0.25, "style": 0.10}


def build_vocab(pairs):
    """Kumpulkan semua nilai atribut yang ada, dikelompokkan per tipe."""
    vocab = {t: [] for t in ATTR_ORDER}
    for tipe, nilai in pairs:
        if tipe in vocab and nilai not in vocab[tipe]:
            vocab[tipe].append(nilai)
    return vocab


def vectorize(attrs, vocab):
    """One-hot berbobot: nilai yang dimiliki produk bernilai akar(bobot), selain itu 0."""
    vec = []
    for tipe in ATTR_ORDER:
        scale = math.sqrt(WEIGHTS[tipe])
        for nilai in vocab[tipe]:
            vec.append(scale if nilai in attrs.get(tipe, []) else 0.0)
    return vec


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return 0.0 if na == 0 or nb == 0 else dot / (na * nb)


def find_dupes(ref_attrs, candidates, vocab, limit=3, min_score=0.5):
    """candidates: list of (objek_produk, atribut_dict). Hasil: [(skor, objek)] terurut."""
    ref_vec = vectorize(ref_attrs, vocab)
    scored = []
    for obj, attrs in candidates:
        s = cosine(ref_vec, vectorize(attrs, vocab))
        if s >= min_score:
            scored.append((round(s, 4), obj))
    scored.sort(key=lambda t: (-t[0], t[1].harga, t[1].id))
    return scored[:limit]