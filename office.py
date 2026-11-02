"""Read Word and Excel files, and write simple Word files, with the Python standard library only.

Word (.docx) and Excel (.xlsx) files are zip folders of XML, so no extra packages are needed.
"""

from __future__ import annotations

import csv
import io
import re
import zipfile
import xml.etree.ElementTree as ET

MAX_XML_BYTES = 30 * 1024 * 1024  # refuse files that unpack to something huge
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


def _xml(zf: zipfile.ZipFile, name: str) -> ET.Element:
    if zf.getinfo(name).file_size > MAX_XML_BYTES:
        raise ValueError("The file is too large to read.")
    return ET.fromstring(zf.read(name))


# ------------------------------------------------------------------ reading ---

def _para_text(p: ET.Element) -> str:
    parts = []
    for el in p.iter():
        if el.tag == f"{W}t":
            parts.append(el.text or "")
        elif el.tag == f"{W}tab":
            parts.append("\t")
        elif el.tag in (f"{W}br", f"{W}cr"):
            parts.append("\n")
    return "".join(parts)


def docx_text(data: bytes) -> str:
    """The text of a Word document: one paragraph per line, table rows as 'cell | cell'."""
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        root = _xml(zf, "word/document.xml")
    body = root.find(f"{W}body")
    lines = []
    for el in (body if body is not None else []):
        if el.tag == f"{W}p":
            lines.append(_para_text(el))
        elif el.tag == f"{W}tbl":
            for tr in el.iter(f"{W}tr"):
                cells = [" ".join(_para_text(p) for p in tc.iter(f"{W}p")).strip() for tc in tr.findall(f"{W}tc")]
                lines.append(" | ".join(cells))
            lines.append("")
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def _col(ref: str) -> int:
    letters = re.match(r"[A-Za-z]+", ref)
    n = 0
    for ch in (letters.group(0).upper() if letters else "A"):
        n = n * 26 + ord(ch) - 64
    return n - 1


def xlsx_text(data: bytes, max_rows: int = 300, max_cols: int = 40) -> str:
    """Each sheet of an Excel workbook as CSV text. Formulas show their last calculated value."""
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        names = set(zf.namelist())
        shared = []
        if "xl/sharedStrings.xml" in names:
            for si in _xml(zf, "xl/sharedStrings.xml").iter(f"{S}si"):
                shared.append("".join(t.text or "" for t in si.iter(f"{S}t")))
        rels = {}
        if "xl/_rels/workbook.xml.rels" in names:
            for rel in _xml(zf, "xl/_rels/workbook.xml.rels"):
                rels[rel.get("Id")] = rel.get("Target") or ""
        out = []
        for sheet in _xml(zf, "xl/workbook.xml").iter(f"{S}sheet"):
            target = rels.get(sheet.get(f"{R}id"), "").lstrip("/")
            part = target if target.startswith("xl/") else f"xl/{target}"
            if part not in names:
                continue
            rows, truncated = [], False
            for row in _xml(zf, part).iter(f"{S}row"):
                if len(rows) >= max_rows:
                    truncated = True
                    break
                cells = {}
                for c in row.iter(f"{S}c"):
                    col = _col(c.get("r") or "") if c.get("r") else len(cells)
                    if col >= max_cols:
                        continue
                    kind, v = c.get("t"), c.find(f"{S}v")
                    raw = v.text if v is not None and v.text else ""
                    if kind == "s":
                        value = shared[int(raw)] if raw.isdigit() and int(raw) < len(shared) else ""
                    elif kind == "inlineStr":
                        value = "".join(t.text or "" for t in c.iter(f"{S}t"))
                    elif kind == "b":
                        value = "TRUE" if raw == "1" else "FALSE"
                    elif not raw and c.find(f"{S}f") is not None:
                        value = "=" + (c.find(f"{S}f").text or "")  # a formula Excel has not calculated yet
                    else:
                        value = raw
                    cells[col] = value
                if any(cells.values()):
                    rows.append([cells.get(i, "") for i in range(max(cells) + 1)])
            buf = io.StringIO()
            csv.writer(buf, lineterminator="\n").writerows(rows)
            note = f"\n(only the first {max_rows} rows are shown)" if truncated else ""
            out.append(f"Sheet: {sheet.get('name')}\n{buf.getvalue().strip()}{note}")
    return "\n\n".join(out).strip()


# ------------------------------------------------------------------ writing ---

_BAD_XML = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def _esc(text: str) -> str:
    text = _BAD_XML.sub("", text)
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


_INLINE = re.compile(r"(\*\*[^*]+\*\*|__[^_]+__|`[^`]+`|\[[^\]]+\]\([^)\s]+\)|\*[^*\s][^*]*\*)")


def _runs(text: str, bold: bool = False, italic: bool = False) -> str:
    """Markdown inline formatting (bold, italic, code, links) as Word runs."""
    out = []
    for part in _INLINE.split(text):
        if not part:
            continue
        b, i, mono = bold, italic, False
        if (part.startswith("**") and part.endswith("**")) or (part.startswith("__") and part.endswith("__")):
            part, b = part[2:-2], True
        elif part.startswith("`") and part.endswith("`"):
            part, mono = part[1:-1], True
        elif part.startswith("[") and "](" in part:
            label, url = part[1:].split("](", 1)
            part = f"{label} ({url[:-1]})"
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            part, i = part[1:-1], True
        # Word expects run properties in schema order: font, then bold, then italic.
        props = ('<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>' if mono else "") + \
                ("<w:b/>" if b else "") + ("<w:i/>" if i else "")
        rpr = f"<w:rPr>{props}</w:rPr>" if props else ""
        out.append(f'<w:r>{rpr}<w:t xml:space="preserve">{_esc(part)}</w:t></w:r>')
    return "".join(out)


def _para(text: str, style: str = "", indent: int = 0, bold: bool = False, italic: bool = False) -> str:
    ppr = ""
    if style or indent:
        ppr = "<w:pPr>" + (f'<w:pStyle w:val="{style}"/>' if style else "") + \
              (f'<w:ind w:left="{indent}" w:hanging="300"/>' if indent else "") + "</w:pPr>"
    return f"<w:p>{ppr}{_runs(text, bold, italic)}</w:p>"


TEXT_WIDTH = 9306  # A4 width minus margins, in twentieths of a point


def _table(rows: list[list[str]]) -> str:
    """A full-width table; wider columns for longer text."""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    weight = [min(max(max(len(r[c]) for r in rows), 6), 60) for c in range(width)]
    cols = [TEXT_WIDTH * w // sum(weight) for w in weight]
    border = "".join(f'<w:{side} w:val="single" w:sz="4" w:space="0" w:color="999999"/>'
                     for side in ("top", "left", "bottom", "right", "insideH", "insideV"))
    xml = [f'<w:tbl><w:tblPr><w:tblW w:w="{TEXT_WIDTH}" w:type="dxa"/><w:tblBorders>{border}</w:tblBorders>'
           '<w:tblLayout w:type="fixed"/></w:tblPr>',
           "<w:tblGrid>" + "".join(f'<w:gridCol w:w="{c}"/>' for c in cols) + "</w:tblGrid>"]
    for n, row in enumerate(rows):
        cells = "".join(f'<w:tc><w:tcPr><w:tcW w:w="{cols[i]}" w:type="dxa"/></w:tcPr>{_para(c, bold=(n == 0))}</w:tc>'
                        for i, c in enumerate(row))
        xml.append(f"<w:tr>{cells}</w:tr>")
    xml.append("</w:tbl><w:p/>")
    return "".join(xml)


def _split_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def markdown_to_docx(markdown: str) -> bytes:
    """A simple Word file from Markdown: headings, paragraphs, bullet and numbered lists, tables and bold text."""
    body, para, lines, i = [], [], markdown.replace("\r\n", "\n").split("\n"), 0

    def flush():
        if para:
            body.append(_para(" ".join(para)))
            para.clear()

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        heading = re.match(r"(#{1,6})\s+(.*)", stripped)
        bullet = re.match(r"(\s*)[-*+]\s+(.*)", line)
        number = re.match(r"(\s*)(\d+)[.)]\s+(.*)", line)
        if stripped.startswith("```"):
            flush()
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                body.append(f'<w:p><w:r><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/></w:rPr>'
                            f'<w:t xml:space="preserve">{_esc(lines[i])}</w:t></w:r></w:p>')
                i += 1
        elif not stripped or re.fullmatch(r"[-*_]{3,}", stripped):
            flush()
        elif heading:
            flush()
            level = len(heading.group(1))
            style = {1: "Title", 2: "Heading1", 3: "Heading2"}.get(level, "Heading3")
            body.append(_para(heading.group(2).strip("# "), style))
        elif stripped.startswith("|") and i + 1 < len(lines) and re.match(r"\s*\|?\s*:?-{3,}", lines[i + 1]):
            flush()
            rows = [_split_row(line)]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(_split_row(lines[i]))
                i += 1
            body.append(_table(rows))
            continue
        elif bullet:
            flush()
            depth = len(bullet.group(1).replace("\t", "    ")) // 2
            body.append(_para("• " + bullet.group(2), indent=360 + 360 * depth))
        elif number:
            flush()
            depth = len(number.group(1).replace("\t", "    ")) // 2
            body.append(_para(f"{number.group(2)}. {number.group(3)}", indent=360 + 360 * depth))
        elif stripped.startswith(">"):
            flush()
            body.append(_para(stripped.lstrip("> "), indent=360, italic=True))
        else:
            para.append(stripped)
            if line.endswith("  "):  # Markdown line break
                flush()
        i += 1
    flush()

    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>'
                + "".join(body) +
                '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1300" w:right="1300" w:bottom="1300" '
                'w:left="1300" w:header="708" w:footer="708" w:gutter="0"/></w:sectPr></w:body></w:document>')

    def style(sid, name, size, outline=None, after=80):
        lvl = f'<w:outlineLvl w:val="{outline}"/>' if outline is not None else ""
        return (f'<w:style w:type="paragraph" w:styleId="{sid}"><w:name w:val="{name}"/><w:basedOn w:val="Normal"/>'
                f'<w:next w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="240" w:after="{after}"/>{lvl}</w:pPr>'
                f'<w:rPr><w:b/><w:sz w:val="{size}"/></w:rPr></w:style>')

    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
              '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>'
              '<w:sz w:val="22"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" '
              'w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>'
              '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>'
              + style("Title", "Title", 40, after=200) + style("Heading1", "heading 1", 30, 0)
              + style("Heading2", "heading 2", 26, 1) + style("Heading3", "heading 3", 23, 2) + "</w:styles>")
    content_types = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                     '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                     '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                     '<Default Extension="xml" ContentType="application/xml"/>'
                     '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
                     '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
                     '</Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '</Relationships>')
    doc_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
                '</Relationships>')
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", rels)
        zf.writestr("word/document.xml", document)
        zf.writestr("word/styles.xml", styles)
        zf.writestr("word/_rels/document.xml.rels", doc_rels)
    return buf.getvalue()


def _letters(n: int) -> str:
    s = ""
    n += 1
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


_NUMBER = re.compile(r"^-?\d+(\.\d+)?$")


def _cell(value: str, ref: str, header: bool) -> str:
    """One spreadsheet cell: a formula, a number (with £ or % formats) or text."""
    v = value.strip()
    if header:
        return f'<c r="{ref}" t="inlineStr" s="1"><is><t xml:space="preserve">{_esc(v)}</t></is></c>'
    if v.startswith("=") and len(v) > 1:
        return f'<c r="{ref}"><f>{_esc(v[1:])}</f></c>'
    plain = v.replace(",", "")
    negative = plain.startswith("-") or (plain.startswith("(") and plain.endswith(")"))
    plain = plain.strip("()").lstrip("-")
    style = 0
    if plain.startswith("£"):
        plain, style = plain[1:], 2
    if (plain[:1] == "0" and len(plain) > 1 and plain[1:2] != ".") or len(plain.replace(".", "")) > 15:
        return f'<c r="{ref}" t="inlineStr"><is><t xml:space="preserve">{_esc(v)}</t></is></c>'  # phone numbers, IDs
    if plain.endswith("%") and _NUMBER.match(plain[:-1]):
        number, style = float(plain[:-1]) / 100, 3
    elif _NUMBER.match(plain):
        number = float(plain)
    else:
        return f'<c r="{ref}" t="inlineStr"><is><t xml:space="preserve">{_esc(v)}</t></is></c>' if v else ""
    number = -number if negative else number
    text = repr(int(number)) if number == int(number) and abs(number) < 1e15 else repr(number)
    return f'<c r="{ref}"{f" s={chr(34)}{style}{chr(34)}" if style else ""}><v>{text}</v></c>'


def csv_to_xlsx(csv_text: str, sheet_name: str = "Sheet1") -> bytes:
    """A real Excel file from CSV text: bold, frozen header row, £ and % formats, and live formulas (cells starting =)."""
    rows = [r for r in csv.reader(io.StringIO(csv_text.lstrip("﻿")))]
    rows = [r for r in rows if any(c.strip() for c in r)] or [[""]]
    width = max(len(r) for r in rows)
    widths = [min(max([len(r[c]) if c < len(r) else 0 for r in rows] + [6]) + 2, 60) for c in range(width)]
    cols = "".join(f'<col min="{i + 1}" max="{i + 1}" width="{w}" customWidth="1"/>' for i, w in enumerate(widths))
    data = []
    for y, row in enumerate(rows, 1):
        cells = "".join(_cell(value, f"{_letters(x)}{y}", y == 1) for x, value in enumerate(row))
        data.append(f'<row r="{y}">{cells}</row>')
    sheet = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
             '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
             '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>'
             '</sheetView></sheetViews>'
             f'<cols>{cols}</cols><sheetData>{"".join(data)}</sheetData></worksheet>')
    name = _esc(re.sub(r"[\[\]:*?/\\]", " ", sheet_name)[:31] or "Sheet1")
    workbook = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
                'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
                f'<sheets><sheet name="{name}" sheetId="1" r:id="rId1"/></sheets><calcPr calcId="191029" fullCalcOnLoad="1"/></workbook>')
    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
              '<numFmts count="1"><numFmt numFmtId="164" formatCode="&quot;£&quot;#,##0.00"/></numFmts>'
              '<fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="11"/><name val="Calibri"/></font></fonts>'
              '<fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill>'
              '<fill><patternFill patternType="solid"><fgColor rgb="FFEFE6D2"/><bgColor indexed="64"/></patternFill></fill></fills>'
              '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
              '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
              '<cellXfs count="4"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
              '<xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1"/>'
              '<xf numFmtId="164" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/>'
              '<xf numFmtId="9" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/></cellXfs>'
              '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>')
    content_types = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                     '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                     '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                     '<Default Extension="xml" ContentType="application/xml"/>'
                     '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
                     '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
                     '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
                     '</Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            '</Relationships>')
    wb_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
               '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
               '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
               '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
               '</Relationships>')
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", rels)
        zf.writestr("xl/workbook.xml", workbook)
        zf.writestr("xl/_rels/workbook.xml.rels", wb_rels)
        zf.writestr("xl/worksheets/sheet1.xml", sheet)
        zf.writestr("xl/styles.xml", styles)
    return buf.getvalue()
