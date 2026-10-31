import json
import os
import re

from src.ingestion.table_jobs import TABLE_JOBS


def fix_spacing(text):
    text = re.sub(r"(?<=[a-z])\(", " (", text)        # year(12 -> year (12
    text = re.sub(r"(?<=\d)(?=[A-Za-z])", " ", text)   # 12months -> 12 months
    return text


def row_to_text(title, row, lead):
    # fields listed in "lead" come first, so they fall inside the part of the
    # text that the embedding model actually reads
    keys = [k for k in lead if k in row] + [k for k in row if k not in lead]

    parts = []
    for k in keys:
        v = row[k]
        if v is None:
            continue
        if isinstance(v, list):
            v = "; ".join(str(x) for x in v)
        parts.append(f"{k.replace('_', ' ').title()}: {str(v).rstrip('.')}")

    return fix_spacing(f"{title}. " + ". ".join(parts) + ".")


def load_table_chunks():
    chunks = []

    for job in TABLE_JOBS:
        with open(f"data/processed/{job['name']}.json", encoding="utf-8") as f:
            table = json.load(f)

        pages = job["pages"]
        page_label = str(pages[0]) if len(pages) == 1 else f"{pages[0]}-{pages[-1]}"
        title = job.get("title", job["describe"])

        for i, row in enumerate(table):

            # one chunk per offence, if the flag is on and the row has a list of offences
            if job.get("split_offences") and isinstance(row.get("offences"), list):
                for j, offence in enumerate(row["offences"]):
                    split_row = {
                        "part": row.get("part"),
                        "punishment": row.get("punishment"),
                        "offence": offence,
                    }
                    chunks.append({
                        "text": row_to_text(title, split_row, job["lead"]),
                        "metadata": {
                            "source": job["source"],
                            "page": page_label,
                            "chunk_id": f"table_{job['name']}_{i}_{j}",
                        },
                    })

            # otherwise one chunk per row, as before
            else:
                chunks.append({
                    "text": row_to_text(title, row, job["lead"]),
                    "metadata": {
                        "source": job["source"],
                        "page": page_label,
                        "chunk_id": f"table_{job['name']}_{i}",
                    },
                })

    return chunks


def load_manual_chunks(path="data/processed/manual_chunks.json"):
    # hand-written chunks, for example the CPI formula
    if not os.path.exists(path):
        return []

    with open(path, encoding="utf-8") as f:
        items = json.load(f)

    return [
        {
            "text": item["text"],
            "metadata": {
                "source": item["source"],
                "page": item["page"],
                "chunk_id": f"manual_{i}",
            },
        }
        for i, item in enumerate(items)
    ]