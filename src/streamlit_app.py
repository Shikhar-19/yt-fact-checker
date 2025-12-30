# src/streamlit_app.py
import streamlit as st
import requests
import json
import os
from report_generator import save_html_report, save_pdf_report

API_URL = "http://localhost:8000/check"

st.set_page_config(page_title="YouTube Fact Checker", layout="wide")

st.title("YouTube Fact Checker")

st.markdown("Paste a YouTube URL (or a local transcript path) and click **Check**.")

url = st.text_input("YouTube URL or local transcript path (e.g. yt_captions/Ks-_Mh1QhMc.en.json3)")

if st.button("Check"):
    if not url:
        st.warning("Enter a URL or local path.")
    else:
        with st.spinner("Running pipeline — this may take a while for LLM checks..."):
            try:
                resp = requests.post(API_URL, json={"url": url}, timeout=600)
                resp.raise_for_status()
                data = resp.json()
                if data.get("status") != "ok":
                    st.error(f"API error: {data}")
                else:
                    report = data["report"]

                    # summary
                    st.subheader("Summary")
                    cols = st.columns(4)
                    cols[0].metric("Total sentences", report["total_sentences"])
                    cols[1].metric("Factual claims", report["counts"]["factual_claims"])
                    cols[2].metric("Disputed claims", report["counts"]["disputed_claims"])
                    cols[3].metric("Ignored", report["counts"]["ignored"])

                    # factual list
                    st.subheader("Factual claims (verified)")
                    for f in report["factual_claims_verified"]:
                        verdict = f["fact_check"].get("verdict", "UNVERIFIABLE")
                        color = "green" if verdict == "TRUE" else ("orange" if "PARTIAL" in verdict else "red")
                        st.markdown(f"**Verdict:** `{verdict}` — **Score:** {f['model_score']}")
                        st.write(f["sentence"])
                        with st.expander("Explanation & Evidence"):
                            st.write(f["fact_check"].get("explanation",""))
                            st.write(f["fact_check"].get("evidence", []))

                    # disputed
                    st.subheader("Disputed claims (verified)")
                    for f in report["disputed_claims_verified"]:
                        verdict = f["fact_check"].get("verdict", "UNVERIFIABLE")
                        st.markdown(f"**Verdict:** `{verdict}` — **Score:** {f['model_score']}")
                        st.write(f["sentence"])
                        with st.expander("Explanation & Evidence"):
                            st.write(f["fact_check"].get("explanation",""))
                            st.write(f["fact_check"].get("evidence", []))

                    # download HTML / PDF
                    tmp_dir = "reports"
                    os.makedirs(tmp_dir, exist_ok=True)
                    html_path = os.path.join(tmp_dir, f"report_{report['video_id']}.html")
                    save_html_report(report, html_path)
                    st.markdown("### Downloads")
                    with open(html_path, "rb") as fh:
                        st.download_button("Download HTML Report", fh.read(), file_name=os.path.basename(html_path), mime="text/html")

                    # offer PDF if pdfkit installed
                    try:
                        pdf_path = os.path.join(tmp_dir, f"report_{report['video_id']}.pdf")
                        save_pdf_report(report, pdf_path)
                        with open(pdf_path, "rb") as fh:
                            st.download_button("Download PDF Report", fh.read(), file_name=os.path.basename(pdf_path), mime="application/pdf")
                    except Exception as e:
                        st.info("PDF generation unavailable (needs wkhtmltopdf + pdfkit). You can still download HTML.")
            except Exception as e:
                st.error(f"Error calling API: {e}")
