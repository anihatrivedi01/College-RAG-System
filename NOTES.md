# College RAG System: project notes

## 1. Pipeline
PDF -> text layer, or Tesseract OCR fallback -> page cleaning -> per-page chunking (1200 / 150)
-> MiniLM embeddings (all-MiniLM-L6-v2, 384-dim) -> ChromaDB
-> question split (Gemini flash-lite) -> top-k retrieval (k=3 per sub-question) -> merged context
-> Gemini generation (temperature 0.2, answer only from context, cite source and page)

Table rows and the CPI formula are added as separate hand-checked chunks from `data/processed/`.

## 2. Corpus
5 PDFs: ordinance on conduct and evaluation (10 pages, scanned), criteria for passing (1, scanned),
unfair means regulation (9, scanned), R&D guidelines (20, text layer), scribe notice (1, scanned).
Final collection: 132 chunks (98 page chunks + 34 table/manual chunks).

## 3. Experiments

### 3.1 OCR preprocessing
- Problem: default Tesseract output garbled words in the section 6(i) promotion criteria
  ("al least, rea a) 50%").
- Change: 300 DPI render, grayscale, fixed threshold (180), `--psm 6`.
- Result: criteria text readable and correct (50%, 90%). Words are sometimes joined
  ("candidateswho") and left as a known limitation.

### 3.2 Page cleaning
- Removed repeated headers and footers, page-number lines and junk lines; skipped the
  table-of-contents page; dropped chunks under 100 characters.
- Ordinance: 30 -> 27 chunks. R&D guidelines: 52 -> 50 chunks.
- Ph.D. assistance query stopped returning the table of contents.

### 3.3 Table extraction
- Problem: OCR read the tables row by row across columns, so the clause 17 punishments were
  garbled and the "Theory Courses" row of the weightage table was lost.
- Gemini returned nothing for "transcribe exactly" prompts (RECITATION block). A structured-JSON
  prompt over the table pages together worked and merged rows that cross page breaks.
- Hand corrections after checking against the PDF: unfair means text, Dissertation/Thesis row
  split into External and Internal examiner rows, marks table restructured (heading rows removed).
- CPI formula (not OCR-readable) written by hand as one chunk.
- Unfair means rows split into one chunk per offence (26 chunks); old garbled OCR chunks 13-21
  of that file skipped.

| Question | Before | After |
|---|---|---|
| Punishment for carrying a mobile phone | [paste baseline answer: no split, guessed "semester"] | Both cases: possession only = exam cancelled; used or helped = cancelled plus 12-month debarment |
| Weightage of end-term exam, theory | "I could not find this information" | 60% end-term (40% continuous evaluation) |

### 3.4 Retrieval depth (k)
Tested k = 2, 3, 4, 5 on four cross-document questions.
- k=2 avoided cross-document noise on small documents but missed context on broad ones.
- k=3 was the best balance. k=4 and 5 added irrelevant chunks (table of contents, an unrelated punishment row).
- Raising k did not fix the mobile phone question: that was a data problem (garbled table), fixed in 3.3.

### 3.5 Prompt revision
Three changes: include every condition/limit/exception stated in the context (instead of "concise"),
decline with one sentence and no source, write fractions in plain text.
- Main set: 8/10 -> 9.5/10 on answers; the last miss (CPI formula omitted the 50% rule) was fixed
  by rewriting the CPI chunk so the rule is part of the formula sentence -> 10/10.

### 3.6 Question decomposition
- Problem: a two-topic question (scribe extra time plus attendance) retrieved only the scribe
  chunks and the answer declined on attendance.
- Change: Gemini splits the question into sub-questions; retrieve per sub-question; merge.
- Hard set retrieval 9/10 -> 10/10, answers 9.5/10 -> 10/10. No change on the main set.

## 4. Evaluation
Two sets of 12 questions (10 answerable, 2 not in the documents). Retrieval hit is checked on
phrases that must appear in the retrieved text.

| Set | Retrieval | Answers | Correct decline |
|---|---|---|---|
| Main | 10/10 | 10/10 | 2/2 |
| Hard (rephrased, short, comparison, two-document) | 10/10 | 10/10 | 2/2 |

Notes: scores were graded by hand against the PDFs by the author. One expected answer (weightage) was
corrected after the first run because it asked for more than the question did.

## 5. Limitations
- Small question sets written by the system's builder. Several questions (mobile phone, weightage,
  CPI, scribe plus attendance) were the ones the fixes targeted; report the rest separately.
- `SKIP_CHUNKS` depends on chunk ids at 1200/150; it breaks if chunk settings change.
- `TABLE_JOBS` lists three tables by hand; a newly uploaded PDF with a table gets no table handling.
- OCR still joins some words; the splitter sometimes splits single-topic questions and uses an
  extra Gemini call (free-tier rate limits).
- Page labels are PDF page indices, not printed page numbers; table chunks cite a page range.
- Chunk size not tuned.