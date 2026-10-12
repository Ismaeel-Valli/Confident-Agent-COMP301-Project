param([string]$InPath, [string]$OutDocx, [string]$OutPdf)
# Opens a .docx in Microsoft Word, updates every field (captions, cross-references),
# tables of contents and tables of figures, then saves the .docx and exports a PDF.
$ErrorActionPreference = "Stop"
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($InPath, $false, $false)
    $doc.Fields.Update() | Out-Null
    foreach ($toc in $doc.TablesOfContents) { $toc.Update() | Out-Null }
    foreach ($tof in $doc.TablesOfFigures) { $tof.Update() | Out-Null }
    $doc.Fields.Update() | Out-Null
    foreach ($toc in $doc.TablesOfContents) { $toc.UpdatePageNumbers() | Out-Null }
    foreach ($tof in $doc.TablesOfFigures) { $tof.UpdatePageNumbers() | Out-Null }
    $doc.SaveAs2($OutDocx, 16)          # wdFormatDocumentDefault
    if ($OutPdf) { $doc.ExportAsFixedFormat($OutPdf, 17) }   # wdExportFormatPDF
    "pages: " + $doc.ComputeStatistics(2)
    "figures in table of figures: " + ($(if ($doc.TablesOfFigures.Count) { $doc.TablesOfFigures.Item(1).Range.Paragraphs.Count } else { 0 }))
    $doc.Close($false)
} finally {
    $word.Quit()
}
