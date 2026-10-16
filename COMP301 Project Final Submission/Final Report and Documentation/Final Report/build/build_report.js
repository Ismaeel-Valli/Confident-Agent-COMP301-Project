// Builds the final report (.docx) from content.js with the `docx` package.
//   node build_report.js <out.docx>
// Figures and tables are numbered in order of appearance; {fig:key} and {tab:key} in the text
// become "Figure N" / "Table N". Captions use Word SEQ fields, so Word's table of figures and
// list of tables pick them up when fields are updated (word_finalize.ps1 does that).
const fs = require('fs');
const path = require('path');
const d = require('docx');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, TableOfContents, SequentialIdentifier, PageOrientation,
  Footer, Header, PageNumber, AlignmentType, NumberFormat, ImageRun, SectionType, Table, TableRow, TableCell,
  WidthType, BorderStyle, ShadingType, LevelFormat, VerticalAlign, TabStopType, PageBreak,
} = d;

const content = require('./content.js');
const OUT = process.argv[2] || 'report.docx';
const FONT = 'Calibri';
const ACCENT = '1F3864';
const BODY_W = 9026;                // A4 portrait text width in twips (2.54 cm margins)
const A3_W = 22111;                 // A3 landscape text width in twips (1.5 cm margins)

// ------------------------------------------------------------------ numbering of figures and tables
const numbers = { fig: {}, tab: {} };
let nf = 0, nt = 0;
for (const b of content.blocks) {
  if (b.t === 'fig' || b.t === 'collage') numbers.fig[b.key] = ++nf;
  if (b.t === 'table') numbers.tab[b.key] = ++nt;
}
function resolveRefs(s) {
  return s.replace(/\{(fig|tab):([\w-]+)\}/g, (m, kind, key) => {
    const n = numbers[kind][key];
    if (!n) throw new Error(`unknown reference ${m}`);
    return (kind === 'fig' ? 'Figure ' : 'Table ') + n;
  });
}

// ------------------------------------------------------------------ inline markup: **bold**, *italic*, `code`
function runs(text, opts = {}, resolved = false) {
  const s = resolved ? text : resolveRefs(text);
  const out = [];
  const re = /(\*\*.+?\*\*|\*[^*\s][^*]*\*|`[^`]+`)/g;
  let last = 0, m;
  while ((m = re.exec(s))) {
    if (m.index > last) out.push(new TextRun({ text: s.slice(last, m.index), ...opts }));
    const tok = m[0];
    if (tok.startsWith('**')) out.push(...runs(tok.slice(2, -2), { ...opts, bold: true }, true));
    else if (tok.startsWith('`')) out.push(new TextRun({ text: tok.slice(1, -1), font: 'Consolas', size: opts.size ? opts.size - 1 : 20, ...omit(opts, ['size']) }));
    else out.push(...runs(tok.slice(1, -1), { ...opts, italics: true }, true));
    last = m.index + tok.length;
  }
  if (last < s.length) out.push(new TextRun({ text: s.slice(last), ...opts }));
  return out;
}
function omit(o, keys) { const r = { ...o }; for (const k of keys) delete r[k]; return r; }

// ------------------------------------------------------------------ images
function pngSize(buf) { return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) }; }
function image(file, maxWpx, maxHpx) {
  const buf = fs.readFileSync(path.resolve(__dirname, file));
  const { w, h } = pngSize(buf);
  let W = maxWpx, H = Math.round(maxWpx * h / w);
  if (maxHpx && H > maxHpx) { H = maxHpx; W = Math.round(maxHpx * w / h); }
  return new ImageRun({ type: 'png', data: buf, transformation: { width: W, height: H } });
}

// ------------------------------------------------------------------ equations (Office Math)
const M = (t) => new d.MathRun(t);
const sub = (base, s) => new d.MathSubScript({ children: [M(base)], subScript: [M(s)] });
const equations = {
  ewcs: () => [M('EWCS = '), new d.MathFraction({
    numerator: [new d.MathSum({ children: [sub('w', 'l'), M(' · '), sub('t', 'l'), M(' · '), sub('c', 'l')], subScript: [M('l ∈ A')] })],
    denominator: [new d.MathSum({ children: [sub('w', 'l')], subScript: [M('l ∈ A')] })] })],
  signed: () => [M('S = '), new d.MathFraction({
    numerator: [new d.MathSum({ children: [sub('w', 'l'), M(' · '), sub('t', 'l'), M(' · '), sub('σ', 'l')], subScript: [M('l ∈ A')] })],
    denominator: [new d.MathSum({ children: [sub('w', 'l')], subScript: [M('l ∈ A')] })] })],
  ranksum: () => [sub('w', 'k'), M(' ∝ n − '), sub('r', 'k'), M(' + 1,   n = 4 severity ranks  ⇒  4 : 3 : 2 : 1')],
  rand: () => [M('Cost (R) = '), new d.MathFraction({ numerator: [M('E (J)')], denominator: [M('3 600 000 J/kWh')] }),
    M(' × R3.5747/kWh × 1.15 = E × 1.1419 × '), new d.MathSuperScript({ children: [M('10')], superScript: [M('−6')] }), M(' R/J')],
  mcnemar: () => [M('p = min'), new d.MathRoundBrackets({ children: [M('1, 2 '), new d.MathSum({ children: [new d.MathRoundBrackets({ children: [new d.MathFraction({ numerator: [M('b + c')], denominator: [M('k')] })] }), M('0.5'), new d.MathSuperScript({ children: [M('')], superScript: [M('b + c')] })], subScript: [M('k = 0')], superScript: [M('min(b, c)')] })] })],
};

// ------------------------------------------------------------------ tables
const thin = { style: BorderStyle.SINGLE, size: 4, color: 'A6A6A6' };
const borders = { top: thin, bottom: thin, left: thin, right: thin, insideHorizontal: thin, insideVertical: thin };
function table(b, width) {
  const total = b.cols.reduce((a, c) => a + c, 0);
  const widths = b.cols.map(c => Math.round(width * c / total));
  widths[widths.length - 1] += width - widths.reduce((a, c) => a + c, 0);
  const size = b.size || 18;
  const cell = (txt, i, header, shade) => new TableCell({
    width: { size: widths[i], type: WidthType.DXA },
    shading: header ? { type: ShadingType.CLEAR, color: 'auto', fill: 'D9E2F3' } : shade ? { type: ShadingType.CLEAR, color: 'auto', fill: shade } : undefined,
    margins: { top: 50, bottom: 50, left: 90, right: 90 },
    verticalAlign: VerticalAlign.CENTER,
    children: String(txt).split('\n').map(line => new Paragraph({
      spacing: { after: 0, before: 0, line: 240 },
      alignment: (b.align && b.align[i]) === 'r' ? AlignmentType.RIGHT : (b.align && b.align[i]) === 'c' ? AlignmentType.CENTER : AlignmentType.LEFT,
      children: runs(line, { size, bold: header || undefined }),
    })),
  });
  const rows = [new TableRow({ tableHeader: true, children: b.header.map((h, i) => cell(h, i, true)) })];
  b.rows.forEach((r, ri) => rows.push(new TableRow({ cantSplit: true, children: r.map((c, i) => cell(c, i, false, (b.shadeRows || []).includes(ri) ? 'F2F2F2' : null)) })));
  return new Table({ width: { size: width, type: WidthType.DXA }, columnWidths: widths, borders, rows });
}

function caption(kind, text, opts = {}) {
  const label = kind === 'fig' ? 'Figure' : 'Table';
  return new Paragraph({
    style: 'Caption', keepNext: kind === 'tab', alignment: opts.align || AlignmentType.LEFT,
    children: [new TextRun({ text: label + ' ', bold: true }), new SequentialIdentifier(label), new TextRun({ text: ': ', bold: true }), ...runs(text, { italics: false })],
  });
}

// ------------------------------------------------------------------ block rendering
// h1Break: whether a level-1 heading starts a new page unless the block says otherwise
// (`noBreak` or `pageBreak`). The main narrative runs on; appendices start on new pages.
function render(blocks, width, h1Break = true) {
  const out = [];
  for (const b of blocks) {
    switch (b.t) {
      case 'h1': out.push(new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: b.noBreak ? false : b.pageBreak !== undefined ? b.pageBreak : h1Break, children: runs(b.text) })); break;
      case 'h2': out.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: runs(b.text) })); break;
      case 'h3': out.push(new Paragraph({ heading: HeadingLevel.HEADING_3, children: runs(b.text) })); break;
      case 'fronth': out.push(new Paragraph({ style: 'FrontHeading', pageBreakBefore: !!b.pageBreak, children: runs(b.text) })); break;
      case 'ref': out.push(new Paragraph({ alignment: AlignmentType.LEFT, indent: { left: 400, hanging: 400 }, spacing: { after: 100 }, children: runs(b.text) })); break;
      case 'p': out.push(new Paragraph({ alignment: b.align === 'center' ? AlignmentType.CENTER : AlignmentType.JUSTIFIED, children: runs(b.text), keepNext: !!b.keepNext })); break;
      case 'note': out.push(new Paragraph({ shading: { type: ShadingType.CLEAR, color: 'auto', fill: 'EEF3FA' }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: '2A78D6', space: 8 } },
        spacing: { before: 120, after: 160 }, indent: { left: 120, right: 120 }, children: runs(b.text, { size: 21 }) })); break;
      case 'bullets': b.items.forEach(it => out.push(new Paragraph({ numbering: { reference: 'bullets', level: 0 }, alignment: AlignmentType.LEFT, spacing: { after: 60 }, children: runs(it) }))); break;
      case 'numbers': b.items.forEach(it => out.push(new Paragraph({ numbering: { reference: b.ref || 'numbers', level: 0 }, spacing: { after: 60 }, children: runs(it) }))); break;
      case 'code': b.lines.forEach((ln, i) => out.push(new Paragraph({ style: 'Code', spacing: { after: i === b.lines.length - 1 ? 160 : 0, before: i === 0 ? 80 : 0 }, children: [new TextRun({ text: ln || ' ' })] }))); break;
      case 'eq': out.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: 120 }, children: [new d.Math({ children: equations[b.name]() })] })); break;
      case 'fig': out.push(new Paragraph({ alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 120, after: 40 }, children: [image(b.file, b.width || 600, b.maxHeight || 820)] }), caption('fig', b.caption)); break;
      case 'table':
        out.push(caption('tab', b.caption));
        out.push(table(b, width));
        if (b.note) out.push(new Paragraph({ spacing: { before: 40, after: 160 }, children: runs(b.note, { size: 17, color: '52514E' }) }));
        else out.push(new Paragraph({ spacing: { after: 80 }, children: [] }));
        break;
      case 'collage': {
        const cols = b.cols || 3;
        const cw = Math.floor(A3_W / cols);
        const rows = [];
        for (let i = 0; i < b.files.length; i += cols) {
          rows.push(new TableRow({ children: b.files.slice(i, i + cols).map((f, j) => new TableCell({
            width: { size: cw, type: WidthType.DXA }, margins: { top: 40, bottom: 40, left: 60, right: 60 },
            borders: { top: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' }, bottom: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' }, left: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' }, right: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' } },
            children: [new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 0 }, children: [image(f, b.cellW || 470, b.cellH || 205)] }),
              new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 }, children: runs(b.labels[i + j], { size: 16, color: '52514E' }) })],
          })) }));
        }
        out.push(new Table({ width: { size: A3_W, type: WidthType.DXA }, columnWidths: Array(cols).fill(cw), rows,
          borders: { top: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' }, bottom: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' }, left: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' }, right: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' }, insideHorizontal: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' }, insideVertical: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' } } }));
        out.push(caption('fig', b.caption));
        break;
      }
      case 'toc': out.push(new TableOfContents('Table of Contents', { hyperlink: true, headingStyleRange: '1-3' })); break;
      case 'tof': out.push(new TableOfContents('List of Figures', { hyperlink: true, captionLabelIncludingNumbers: 'Figure' })); break;
      case 'tot': out.push(new TableOfContents('List of Tables', { hyperlink: true, captionLabelIncludingNumbers: 'Table' })); break;
      case 'pagebreak': out.push(new Paragraph({ children: [new PageBreak()] })); break;
      case 'spacer': out.push(new Paragraph({ spacing: { after: b.after || 400 }, children: [] })); break;
      case 'title': out.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: b.before || 0, after: b.after || 120 },
        children: [new TextRun({ text: b.text, size: b.size || 28, bold: !!b.bold, color: b.color || '0B0B0B', font: FONT })] })); break;
      case 'members': out.push(table({ cols: [3, 2], header: ['Member', 'Student number'], rows: b.rows, size: 20 }, 5200)); break;
      case 'section': break;
      default: throw new Error('unknown block ' + b.t);
    }
  }
  return out;
}

// ------------------------------------------------------------------ sections
function split(blocks) {
  const parts = {};
  let cur = null;
  for (const b of blocks) {
    if (b.t === 'section') { cur = b.kind; parts[cur] = []; continue; }
    parts[cur].push(b);
  }
  return parts;
}
const parts = split(content.blocks);
const footer = (fmt) => new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], size: 18, color: '52514E' })] })] });
const header = new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: 'BFBFBF', space: 4 } },
  children: [new TextRun({ text: 'COMP301 Confident Agent: Final Report · The Skeptics · UKZN 2026', size: 16, color: '7F7F7F' })] })] });
const A4 = { size: { width: 11906, height: 16838 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440, header: 600, footer: 600 } };
const A3L = { size: { width: 16838, height: 23811, orientation: PageOrientation.LANDSCAPE }, margin: { top: 850, bottom: 850, left: 850, right: 850, header: 400, footer: 400 } };

const doc = new Document({
  creator: 'The Skeptics', title: content.meta.title, description: content.meta.subtitle,
  features: { updateFields: false },
  styles: {
    default: { document: { run: { font: FONT, size: 22 }, paragraph: { spacing: { after: 120, line: 276 } } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 32, bold: true, color: ACCENT, font: FONT }, paragraph: { spacing: { before: 240, after: 200 }, outlineLevel: 0, keepNext: true } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 26, bold: true, color: ACCENT, font: FONT }, paragraph: { spacing: { before: 280, after: 100 }, outlineLevel: 1, keepNext: true } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 23, bold: true, italics: true, color: '2E5597', font: FONT }, paragraph: { spacing: { before: 200, after: 80 }, outlineLevel: 2, keepNext: true } },
      { id: 'FrontHeading', name: 'Front Heading', basedOn: 'Normal', next: 'Normal',
        run: { size: 32, bold: true, color: ACCENT, font: FONT }, paragraph: { spacing: { before: 240, after: 200 } } },
      { id: 'Caption', name: 'Caption', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 18, color: '404040', font: FONT }, paragraph: { spacing: { before: 60, after: 200 } } },
      { id: 'Code', name: 'Code', basedOn: 'Normal', next: 'Normal',
        run: { font: 'Consolas', size: 17 }, paragraph: { shading: { type: ShadingType.CLEAR, color: 'auto', fill: 'F4F4F2' }, indent: { left: 200, right: 200 }, spacing: { line: 240 } } },
    ],
  },
  numbering: { config: [
    { reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] },
    { reference: 'numbers', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 300 } } } }] },
    ...Array.from({ length: 12 }, (_, i) => ({ reference: 'numbers' + (i + 1), levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 300 } } } }] })),
  ] },
  sections: [
    { properties: { page: A4 }, children: render(parts.title, BODY_W) },
    { properties: { type: SectionType.NEXT_PAGE, page: { ...A4, pageNumbers: { start: 1, formatType: NumberFormat.LOWER_ROMAN } } },
      headers: { default: header }, footers: { default: footer() }, children: render(parts.front, BODY_W) },
    { properties: { type: SectionType.NEXT_PAGE, page: { ...A4, pageNumbers: { start: 1, formatType: NumberFormat.DECIMAL } } },
      headers: { default: header }, footers: { default: footer() }, children: render(parts.main, BODY_W, false) },
    { properties: { type: SectionType.NEXT_PAGE, page: A3L }, headers: { default: header }, footers: { default: footer() }, children: render(parts.a3, A3_W) },
    { properties: { type: SectionType.NEXT_PAGE, page: A4 }, headers: { default: header }, footers: { default: footer() }, children: render(parts.appendix, BODY_W) },
  ],
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync(OUT, buf); console.log(`wrote ${OUT}: ${nf} figures, ${nt} tables`); });
