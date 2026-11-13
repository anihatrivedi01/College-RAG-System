import re

import pymupdf


def clean_cell(value):
    if value is None:
        return ""
    value = value.replace("\uf0b7", " ")             # bullet symbol from some PDF fonts
    return re.sub(r"\s+", " ", value).strip()         # newlines and extra spaces -> one space


def avg_cell_words(data_rows):
    cells = [c for r in data_rows for c in r if c]
    return sum(len(c.split()) for c in cells) / max(len(cells), 1)


def looks_like_page_numbers(values):
    values = [v for v in values if v]
    return bool(values) and all(re.fullmatch(r"\d+(\s*-\s*\d+)?", v) for v in values)


def header_is_plausible(header):
    cells = [h for h in header if h]
    return (
        len(cells) >= 2
        and len(set(cells)) == len(cells)          # no repeated labels
        and all(len(h) <= 60 for h in cells)       # labels are short
    )

def digit_share(data_rows):
    cells = [c for r in data_rows for c in r if c]
    return sum(1 for c in cells if re.search(r"\d", c)) / max(len(cells), 1)


def reject_reason(rows):
    """Return why a candidate is not a data table, or None if it looks like one."""
    if len(rows) < 3 or len(rows[0]) < 2:
        return "too small (needs a header row, 2+ data rows and 2+ columns)"

    header = [clean_cell(c) for c in rows[0]]
    data_rows = [[clean_cell(c) for c in r] for r in rows[1:]]

    if not header_is_plausible(header):
        return "header row is not plausible (repeated, empty or too long labels)"

    if looks_like_page_numbers([r[-1] for r in data_rows if r]):
        return "last column holds page numbers (looks like a table of contents)"

    if avg_cell_words(data_rows) < 3 and digit_share(data_rows) < 0.2:
        return "short, digit-free cells (looks like a list of terms drawn as a grid)"

    filled_columns = sum(1 for col in zip(*data_rows) if any(col))
    if filled_columns < 2:
        return "fewer than 2 columns contain data"

    return None


def title_above(page, table, max_lines=1):
    x0, y0, x1, y1 = table.bbox
    lines = []
    for block in page.get_text("blocks"):
        by1, text = block[3], block[4]
        if by1 <= y0 and (y0 - by1) < 60:
            lines.append((by1, re.sub(r"\s+", " ", text).strip()))
    lines.sort()
    texts = [t for _, t in lines if t][-max_lines:]
    title = " ".join(texts)
    if len(title) > 150:
        title = title[:150].rsplit(" ", 1)[0] + "..."
    return title

def extract_tables_from_pdf(pdf_path, source, report=None):
    """Return one chunk per data row of every table that passes the filters.
    If `report` is a list, it receives a line per candidate table explaining the verdict."""
    doc = pymupdf.open(pdf_path)
    chunks = []

    for page_number, page in enumerate(doc, start=1):
        for t_index, table in enumerate(page.find_tables().tables):
            rows = table.extract()
            reason = reject_reason(rows)

            if report is not None:
                verdict = "REJECTED: " + reason if reason else "ACCEPTED"
                report.append(f"page {page_number} table {t_index} ({len(rows)} rows): {verdict}")

            if reason:
                continue

            title = title_above(page, table) or "Table"
            header = [clean_cell(c) for c in rows[0]]

            for r_index, row in enumerate(rows[1:]):
                cells = [clean_cell(c) for c in row]
                pairs = [f"{h}: {v}" for h, v in zip(header, cells) if h and v]
                if not pairs:
                    continue

                chunks.append({
                    "text": f"{title.rstrip('.')}. Table row. " + ". ".join(pairs) + ".",
                    "metadata": {
                        "source": source,
                        "page": str(page_number),
                        "chunk_id": f"auto_p{page_number}_t{t_index}_r{r_index}",
                        "type": "table",
                        "machine_extracted": True,
                    },
                })

    doc.close()
    return chunks