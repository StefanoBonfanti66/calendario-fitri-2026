#!/usr/bin/env python3
"""Convert a Markdown file to PDF using markdown + xhtml2pdf.

Usage:
    python tools/markdown_to_pdf.py [input.md] [output.pdf]
"""
import sys
import os
from markdown import markdown
from xhtml2pdf import pisa


def md_to_pdf(md_path, pdf_path):
    with open(md_path, "r", encoding="utf-8") as f:
        md = f.read()
    html_body = markdown(md, extensions=["fenced_code", "tables"]) 
    html = f"""<html><head><meta charset=\"utf-8\">\n<style>
    body {{ font-family: DejaVu Sans, Arial, sans-serif; margin: 2cm; }}
    pre {{ background: #f5f5f5; padding:10px; white-space: pre-wrap; }}
    code {{ font-family: monospace; }}
    table {{ border-collapse: collapse; }}
    table, th, td {{ border: 1px solid #ccc; padding: 6px; }}
    h1,h2,h3 {{ font-weight: bold; }}
</style></head><body>\n""" + html_body + "\n</body></html>"

    with open(pdf_path, "wb") as result_file:
        pisa_status = pisa.CreatePDF(html, dest=result_file)
    return pisa_status.err == 0


if __name__ == "__main__":
    md = "GUIDA_UTENTE.md"
    pdf = "GUIDA_UTENTE.pdf"
    if len(sys.argv) > 1:
        md = sys.argv[1]
    if len(sys.argv) > 2:
        pdf = sys.argv[2]
    ok = md_to_pdf(md, pdf)
    if not ok:
        print("Errore nella creazione del PDF.")
        sys.exit(1)
    print("PDF creato:", pdf)
