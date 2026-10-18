from types import SimpleNamespace as NS
from pytest import approx
from app.services.similarity import build_vocab, find_dupes


def test_ranking_dan_filter_skor_minimum():
    ref = {"bahan": ["katun twill"], "fit": ["boxy"], "warna": ["olive"], "style": ["utility"]}
    a = (NS(id=1, harga=289000), {"bahan": ["katun twill"], "fit": ["boxy"], "warna": ["olive"], "style": ["workwear"]})
    b = (NS(id=2, harga=329000), {"bahan": ["katun canvas"], "fit": ["boxy"], "warna": ["olive"], "style": ["utility"]})
    c = (NS(id=3, harga=219000), {"bahan": ["katun twill"], "fit": ["regular"], "warna": ["hijau army"], "style": ["utility"]})
    pairs = [(t, v) for attrs in (ref, a[1], b[1], c[1]) for t, vs in attrs.items() for v in vs]
    hasil = find_dupes(ref, [a, b, c], build_vocab(pairs), limit=3, min_score=0.5)
    assert [o.id for _, o in hasil] == [1, 2]
    assert hasil[0][0] == approx(0.90, abs=1e-4)
    assert hasil[1][0] == approx(0.70, abs=1e-4)