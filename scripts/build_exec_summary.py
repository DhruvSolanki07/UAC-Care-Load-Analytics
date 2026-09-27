"""Build the executive summary: markdown -> self-contained HTML -> PDF.

Images would be inlined as base64 data URIs (none are used in the summary, but the
shared converter supports it). The HTML is printed to PDF with headless Chrome so
the output needs no external dependencies beyond Chrome.
"""
import re
import subprocess
import sys
from pathlib import Path

import html as htmllib

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_paper_html import CSS, convert

ROOT = Path(__file__).resolve().parent.parent
MD = ROOT / "reports" / "executive_summary.md"
OUT_HTML = ROOT / "reports" / "executive_summary.html"
OUT_PDF = ROOT / "reports" / "executive_summary.pdf"

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

# Denser than the paper stylesheet: the summary is a two-page brief, not a paper.
PRINT_CSS = """
@media print {
  body { font-size: 9.7pt; line-height: 1.47; }
  h1 { font-size: 16.5pt; margin-bottom: .2em; }
  h1 + h3 { font-size: 10pt; }
  h2 { font-size: 11.8pt; margin: 1.15em 0 .45em; }
  p, li { margin-bottom: .5em; }
  ul { margin-bottom: .6em; }
  table { font-size: 8.3pt; margin: .75em 0 1em; }
  th, td { padding: .26em .45em; }
  @page { margin: 14mm 16mm; }
}
"""


def find_browser():
    for candidate in CHROME_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    raise FileNotFoundError(
        "No Chrome or Edge install found. Open the generated HTML in a browser "
        "and use Print > Save as PDF instead."
    )


def main():
    body = convert(MD.read_text(encoding="utf-8"))
    title = re.search(r"^#\s+(.*)$", MD.read_text(encoding="utf-8"), re.M).group(1)
    doc = (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{htmllib.escape(title)}</title>\n"
        f"<style>{CSS}\n{PRINT_CSS}</style>\n</head>\n<body>\n{body}\n</body>\n</html>\n"
    )
    OUT_HTML.write_text(doc, encoding="utf-8")
    print(f"Wrote {OUT_HTML}")

    browser = find_browser()
    subprocess.run(
        [
            browser,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={OUT_PDF}",
            OUT_HTML.as_uri(),
        ],
        check=True,
    )
    print(f"Wrote {OUT_PDF} ({OUT_PDF.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
