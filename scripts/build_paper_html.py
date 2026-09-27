"""Build a self-contained, print-ready HTML version of research_paper.md.

Images are inlined as base64 data URIs so the output is a single file that can
be opened in a browser and printed to PDF with no external dependencies.
"""
import base64
import html as htmllib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MD = ROOT / "reports" / "research_paper.md"
OUT = ROOT / "reports" / "research_paper.html"


def inline(text):
    """Apply inline markdown to a span of text."""
    t = htmllib.escape(text)
    # code spans first so their contents are not further transformed
    codes = []

    def stash(m):
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    t = re.sub(r"`([^`]+)`", stash, t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", t)
    t = re.sub(r"\$([^$]+)\$", r"<span class='math'>\1</span>", t)
    t = re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{codes[int(m.group(1))]}</code>", t)
    return t


def table_row(line):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return cells


def convert(md_text, base=None):
    """Convert markdown to HTML. Relative image paths resolve against `base`."""
    base = Path(base) if base else MD.parent
    lines = md_text.split("\n")
    out = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # blank
        if not stripped:
            i += 1
            continue

        # horizontal rule
        if stripped in ("---", "***", "___"):
            out.append("<hr>")
            i += 1
            continue

        # headings
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
            i += 1
            continue

        # image
        m = re.match(r"^!\[(.*?)\]\((.*?)\)$", stripped)
        if m:
            alt, src = m.group(1), m.group(2)
            path = (base / src).resolve()
            if path.exists():
                b64 = base64.b64encode(path.read_bytes()).decode("ascii")
                mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
                out.append(
                    f'<figure><img src="data:{mime};base64,{b64}" alt="{htmllib.escape(alt)}">'
                    f"<figcaption>{inline(alt)}</figcaption></figure>"
                )
            else:
                out.append(f'<p class="missing">[missing image: {htmllib.escape(src)}]</p>')
            i += 1
            continue

        # table
        if stripped.startswith("|") and i + 1 < n and re.match(
            r"^\|[\s:\-|]+\|$", lines[i + 1].strip()
        ):
            header = table_row(stripped)
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(table_row(lines[i].strip()))
                i += 1
            t = ["<table>", "<thead><tr>"]
            t += [f"<th>{inline(c)}</th>" for c in header]
            t.append("</tr></thead><tbody>")
            for r in rows:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table>")
            out.append("".join(t))
            continue

        # blockquote
        if stripped.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(re.sub(r"^>\s?", "", lines[i].strip()))
                i += 1
            out.append(f"<blockquote>{inline(' '.join(buf))}</blockquote>")
            continue

        # lists
        if re.match(r"^([-*]|\d+\.)\s+", stripped):
            ordered = bool(re.match(r"^\d+\.\s", stripped))
            tag = "ol" if ordered else "ul"
            items = []
            while i < n and re.match(r"^([-*]|\d+\.)\s+", lines[i].strip()):
                items.append(re.sub(r"^([-*]|\d+\.)\s+", "", lines[i].strip()))
                i += 1
            lis = "".join(f"<li>{inline(it)}</li>" for it in items)
            out.append(f"<{tag}>{lis}</{tag}>")
            continue

        # paragraph: consume until blank or a new block
        buf = []
        while i < n and lines[i].strip() and not re.match(
            r"^(#{1,6}\s|\||>|!\[|([-*]|\d+\.)\s|---$)", lines[i].strip()
        ):
            buf.append(lines[i].strip())
            i += 1
        if buf:
            out.append(f"<p>{inline(' '.join(buf))}</p>")

    return "\n".join(out)


CSS = """
:root {
  --ink: #16191d;
  --muted: #5b6570;
  --rule: #d8dde3;
  --accent: #1f4e79;
  --soft: #f4f6f8;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  padding: 48px 56px 72px;
  background: #fff;
  color: var(--ink);
  font-family: "Charter", "Georgia", "Times New Roman", serif;
  font-size: 11.2pt;
  line-height: 1.62;
  max-width: 46em;
  margin-inline: auto;
}
h1 {
  font-size: 21pt;
  line-height: 1.2;
  text-align: center;
  margin: 0 0 .35em;
  letter-spacing: -0.01em;
}
h1 + h3 { text-align: center; font-weight: 400; color: var(--muted); font-size: 12pt; }
h2 {
  font-size: 14.5pt;
  margin: 2.1em 0 .7em;
  padding-bottom: .25em;
  border-bottom: 1.5px solid var(--rule);
  color: var(--accent);
  page-break-after: avoid;
}
h3 { font-size: 12.3pt; margin: 1.6em 0 .5em; page-break-after: avoid; }
h4 { font-size: 11.4pt; margin: 1.3em 0 .4em; color: var(--muted); page-break-after: avoid; }
p { margin: 0 0 .85em; text-align: justify; hyphens: auto; }
hr { border: 0; border-top: 1px solid var(--rule); margin: 1.6em 0; }
strong { font-weight: 700; }
em { font-style: italic; }
code {
  font-family: "SF Mono", "Consolas", monospace;
  font-size: .88em;
  background: var(--soft);
  padding: .08em .32em;
  border-radius: 3px;
}
.math { font-family: "Cambria Math", "Times New Roman", serif; font-style: italic; }
ul, ol { margin: 0 0 .95em; padding-left: 1.5em; }
li { margin-bottom: .34em; text-align: justify; }
table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.1em 0 1.4em;
  font-size: 9.1pt;
  font-family: "Segoe UI", "Helvetica Neue", sans-serif;
  page-break-inside: avoid;
}
caption { caption-side: top; text-align: left; font-weight: 600; padding-bottom: .4em; }
th, td { padding: .38em .55em; text-align: left; vertical-align: top; }
thead th { border-bottom: 1.6px solid var(--ink); font-weight: 600; }
tbody tr:nth-child(even) { background: var(--soft); }
tbody td { border-bottom: .5px solid var(--rule); }
td:has(> strong:only-child) { text-align: right; }
figure { margin: 1.4em 0; text-align: center; page-break-inside: avoid; }
figure img { width: 100%; max-width: 100%; height: auto; }
figcaption {
  font-size: 8.9pt;
  font-family: "Segoe UI", sans-serif;
  color: var(--muted);
  text-align: left;
  margin-top: .5em;
  line-height: 1.5;
}
blockquote {
  margin: 1.1em 0;
  padding: .7em 1em;
  background: var(--soft);
  border-left: 3px solid var(--accent);
  font-size: 10.2pt;
}
blockquote p { margin: 0; }
.missing { color: #b00; font-style: italic; }
@media print {
  body { padding: 0; max-width: none; font-size: 10.5pt; }
  h2 { page-break-before: auto; }
  h2, h3 { page-break-after: avoid; }
  table, figure { page-break-inside: avoid; }
  a { color: inherit; text-decoration: none; }
}
@page { margin: 20mm 18mm; }
"""


def main():
    body = convert(MD.read_text(encoding="utf-8"))
    title = re.search(r"^#\s+(.*)$", MD.read_text(encoding="utf-8"), re.M).group(1)
    doc = (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{htmllib.escape(title)}</title>\n"
        f"<style>{CSS}</style>\n</head>\n<body>\n{body}\n</body>\n</html>\n"
    )
    OUT.write_text(doc, encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
