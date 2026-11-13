import sys

import pymupdf

pdf_path = sys.argv[1]
doc = pymupdf.open(pdf_path)

total = 0
for page_number, page in enumerate(doc, start=1):
    tabs = page.find_tables()
    for i, t in enumerate(tabs.tables):
        rows = t.extract()
        total += 1
        print(f"\n=== page {page_number}, table {i}: {len(rows)} rows x {len(rows[0]) if rows else 0} cols ===")
        for row in rows[:4]:      # show the first four rows only
            print(row)

print("\nTables found:", total)