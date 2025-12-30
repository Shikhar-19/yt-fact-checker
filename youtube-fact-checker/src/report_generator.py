# src/report_generator.py

import os
import re
import json
from typing import Dict
from datetime import datetime


# ---------------------------------------
# SAFELY SANITIZE FILENAMES FOR WINDOWS
# ---------------------------------------
def make_safe_filename(name: str) -> str:
    """
    Removes illegal characters from filenames.
    Supports YouTube URLs, paths, and arbitrary strings.
    """
    name = name.strip()

    # Replace URL-specific chars
    name = name.replace("https://", "").replace("http://", "")

    # Replace all illegal Windows filesystem characters
    name = re.sub(r'[\\/:*?"<>|]+', "_", name)

    # Limit filename length
    if len(name) > 200:
        name = name[:200]

    return name


# ---------------------------------------
# HTML RENDERING
# ---------------------------------------
def render_html_report(report: Dict) -> str:
    """
    Returns HTML string of the report.
    """

    video_id = report.get("video_id", "unknown")
    total = report.get("total_sentences", 0)
    counts = report.get("counts", {})
    factual = report.get("factual_claims_verified", [])
    disputed = report.get("disputed_claims_verified", [])

    html = f"""
    <html>
    <head>
      <meta charset="utf-8"/>
      <title>Fact Check Report - {video_id}</title>
      <style>
        body{{font-family: Arial, sans-serif; margin:20px;}}
        .summary{{margin-bottom:20px;}}
        .card{{border-radius:8px;padding:12px;margin-bottom:10px;box-shadow: 0 1px 3px rgba(0,0,0,0.08);}}
        .true{{border-left:6px solid #22c55e}}
        .false{{border-left:6px solid #ef4444}}
        .partial{{border-left:6px solid #f59e0b}}
        .unv{{border-left:6px solid #94a3b8}}
        pre{{white-space:pre-wrap;}}
        h2{{margin-top:24px;}}
      </style>
    </head>
    <body>
      <h1>Fact Check Report — {video_id}</h1>
      <div class="summary card">
        <p><strong>Total sentences:</strong> {total}</p>
        <p><strong>Factual claims:</strong> {counts.get('factual_claims', 0)}</p>
        <p><strong>Disputed claims:</strong> {counts.get('disputed_claims', 0)}</p>
        <p><strong>Ignored:</strong> {counts.get('ignored', 0)}</p>
      </div>
    """

    # ------------------------------
    # FACTUAL CLAIMS
    # ------------------------------
    html += "<h2>Factual claims (verified)</h2>\n"
    for item in factual:
        fc = item.get("fact_check", {})
        verdict = fc.get("verdict", "UNVERIFIABLE")

        # assign CSS class
        css = "unv"
        if verdict == "TRUE": css = "true"
        elif verdict == "FALSE": css = "false"
        elif "PARTIAL" in verdict: css = "partial"

        # Evidence HTML
        evidence_html = "".join(
            f"<li><strong>{ev.get('source')}</strong>: {ev.get('description')}</li>"
            for ev in fc.get("evidence", [])
        )

        html += f"""
        <div class="card {css}">
          <p><strong>Sentence:</strong> <em>{item.get('sentence')}</em></p>
          <p><strong>Model score:</strong> {item.get('model_score')}</p>
          <p><strong>Verdict:</strong> {verdict}</p>
          <p><strong>Explanation:</strong> {fc.get('explanation')}</p>
          <p><strong>Evidence:</strong></p>
          <ul>{evidence_html}</ul>
        </div>
        """

    # ------------------------------
    # DISPUTED CLAIMS
    # ------------------------------
    html += "<h2>Disputed claims (verified)</h2>\n"
    for item in disputed:
        fc = item.get("fact_check", {})
        verdict = fc.get("verdict", "UNVERIFIABLE")

        css = "unv"
        if verdict == "TRUE": css = "true"
        elif verdict == "FALSE": css = "false"
        elif "PARTIAL" in verdict: css = "partial"

        evidence_html = "".join(
            f"<li><strong>{ev.get('source')}</strong>: {ev.get('description')}</li>"
            for ev in fc.get("evidence", [])
        )

        html += f"""
        <div class="card {css}">
          <p><strong>Sentence:</strong> <em>{item.get('sentence')}</em></p>
          <p><strong>Model score:</strong> {item.get('model_score')}</p>
          <p><strong>Verdict:</strong> {verdict}</p>
          <p><strong>Explanation:</strong> {fc.get('explanation')}</p>
          <ul>{evidence_html}</ul>
        </div>
        """

    html += "</body></html>"
    return html


# -------------------------------------------------
# SAVE HTML FILE WITH SAFE FILENAME
# -------------------------------------------------
def save_html_report(report: Dict, out_path: str):
    safe_path = make_safe_filename(out_path)

    html = render_html_report(report)
    with open(safe_path, "w", encoding="utf-8") as f:
        f.write(html)

    return safe_path


# -------------------------------------------------
# SAVE PDF REPORT (optional)
# -------------------------------------------------
def save_pdf_report(report: Dict, out_path: str):
    try:
        import pdfkit
    except ImportError:
        raise RuntimeError(
            "pdfkit is not installed. Run: pip install pdfkit + install wkhtmltopdf system binary."
        )

    safe_path = make_safe_filename(out_path)

    tmp_html = safe_path + ".tmp.html"
    save_html_report(report, tmp_html)

    # PDF export
    pdfkit.from_file(tmp_html, safe_path)
    os.remove(tmp_html)

    return safe_path
