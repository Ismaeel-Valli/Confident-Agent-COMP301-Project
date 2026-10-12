# Building the final report

The report is generated from text and data, so every number and chart can be traced to the
recorded experiment.

| File | Content |
|---|---|
| `content_part1.js` … `content_part4.js` | the report's text, tables and figure references, section by section |
| `build_report.js` | renders the content to `.docx` with the `docx` package (figures and tables are numbered automatically) |
| `build_diagrams.py` | the architecture and UML diagrams in `figures/` (matplotlib) |
| `word_finalize.ps1` | opens the document in Microsoft Word, updates the table of contents, the lists of figures and tables and all fields, saves the `.docx` and exports the PDF |

Charts come from `Findings/Statistical Analysis/tempstats/` (cost statistics) and
`tempstats/report_figures/` (report-specific charts), which read only `Unprocessed Data`.

```bat
python -X utf8 build_diagrams.py
npm install
node build_report.js report.docx
powershell -ExecutionPolicy Bypass -File word_finalize.ps1 -InPath "%CD%\report.docx" -OutDocx "%CD%\..\COMP301 The Skeptics Final Report.docx" -OutPdf "%CD%\..\COMP301 The Skeptics Final Report.pdf"
```

Without Word, open the generated `.docx` and update fields (Ctrl+A, F9) to fill the
table of contents and the lists of figures and tables.
