from app.chunker import chunk_article, split_sections, wc

ART = {"id": 1, "title": "Refresh Firefox", "url": "https://x/y", "product": "firefox"}
STEPS = "\n".join(f"{i}. Step number {i} " + "word " * 12 for i in range(1, 21))
MD = f"Intro paragraph here.\n\n# Refresh Firefox\n\n{STEPS}\n\n## Saved items\n\n- Bookmarks\n- Passwords\n"


def chunks(max_words=60, overlap=30, md=MD):
    return chunk_article(ART, md, max_words, overlap)


def test_no_empty_chunks():
    assert all(c.body.strip() for c in chunks())


def test_body_never_exceeds_limit():
    assert all(wc(c.body) <= 60 for c in chunks())


def test_prefix_has_title_product_section():
    c = next(c for c in chunks() if c.section == "Refresh Firefox")
    assert c.text.startswith("Refresh Firefox [Firefox] > Refresh Firefox\n")


def test_text_before_first_heading_gets_default_section():
    assert split_sections(MD)[0][0] == "Overview"


def test_nested_headings_build_a_path():
    assert any(c.section == "Refresh Firefox > Saved items" for c in chunks())


def test_heading_with_only_subheading_is_not_a_chunk():
    secs = split_sections("# A\n\n## B\n\ntext here")
    assert secs == [("A > B", "text here")]


def test_every_step_present_and_in_order():
    joined = "\n".join(c.body for c in chunks())
    pos = [joined.index(f"Step number {i} word") for i in range(1, 21)]
    assert pos == sorted(pos)


def test_overlap_repeats_last_step_of_previous_chunk():
    cs = [c for c in chunks() if c.section == "Refresh Firefox"]
    assert len(cs) > 1
    assert cs[0].body.splitlines()[-1] in cs[1].body


def test_zero_overlap_repeats_nothing():
    lines = [l for c in chunks(overlap=0) if c.section == "Refresh Firefox" for l in c.body.splitlines()]
    assert len(lines) == len(set(lines)) == 20


def test_single_huge_paragraph_is_split():
    cs = chunks(100, 0, "# T\n\n" + "word " * 500)
    assert len(cs) == 5 and all(wc(c.body) <= 100 for c in cs)


def test_chunk_ids_unique():
    ids = [c.chunk_id for c in chunks()]
    assert len(ids) == len(set(ids))