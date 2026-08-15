import re
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="CRISPR Guide RNA Safety Pipeline", page_icon="🧬", layout="centered"
)

st.title("🧬 CRISPR Guide RNA Design & Safety Pipeline")
st.markdown(
    "**An applied bioinformatics tool** that scans target DNA sequences,"
    " evaluates R-loop thermodynamic stability (GC content), and recommends"
    " precision genome editing modalities (Standard Cas9 vs. Non-DSB Base"
    " Editors) to eliminate chromosomal translocation risks."
)

st.markdown("---")

# User Input Section
default_sequence = (
    "ACATTTGCTTCTGACACAACTGTGTTCACTAGCAACCTCAAACAGACACCATGGTGCATCTGACTCCTGAGGAGA"
    "AGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAACGTGGATGAAGTTGGTGGTGAGGCCCTGGGCAGGTTGGTATCA"
)

dna_input = st.text_area(
    "Enter Target DNA Sequence (FASTA or raw sequence):",
    value=default_sequence,
    height=150,
)

if st.button("Run Safety & Modality Analysis", type="primary"):
  dna_sequence = dna_input.upper().strip()

  # Regex pattern to find 20bp spacer followed by an NGG PAM site
  pattern = r"(?=(.{20})([ATCG]GG))"
  matches = list(re.finditer(pattern, dna_sequence))

  if len(matches) == 0:
    st.warning(
        "No valid SpCas9 PAM sites (NGG) found in the sequence. Please try"
        " another sequence."
    )
  else:
    st.success(f"Analysis Complete! Found {len(matches)} potential target sites.")
    st.markdown("### 📊 Target Site Breakdown")

    for i, match in enumerate(matches):
      spacer = match.group(1)
      pam = match.group(2)

      # Calculate GC content (Optimal range for CRISPR is 40% - 60%)
      gc_count = spacer.count("G") + spacer.count("C")
      gc_content = round((gc_count / 20) * 100, 1)

      # Biological evaluations
      if gc_content < 30 or gc_content > 70:
        status = "Suboptimal Binding"
        recommendation = (
            "⚠️ Avoid: Poor thermodynamic stability for R-loop formation."
        )
      elif "TTTT" in spacer:
        status = "Poly-T Transcription Risk"
        recommendation = "⚠️ Avoid: Triggers U6 polymerase termination."
      else:
        status = "Optimal"
        # Check if cytosine exists in the active window (positions 4 to 8) for Base Editing
        if "C" in spacer[3:8]:
          recommendation = (
              "✅ **Recommended: Cytosine Base Editor (CBE)** — Avoids double-strand"
              " breaks (DSBs) and p53 activation."
          )
        else:
          recommendation = (
              "ℹ️ **Standard Cas9 Knockout or Prime Editor** — No ideal"
              " deamination window detected."
          )

      # Display inside clean containers
      with st.expander(
          f"Target #{i + 1} | Spacer: `{spacer}` | PAM: `{pam}`"
      ):
        col1, col2 = st.columns(2)
        with col1:
          st.metric(label="GC Content", value=f"{gc_content}%")
        with col2:
          st.metric(label="Binding Status", value=status)
        st.markdown(f"**Modality Recommendation:** {recommendation}")

st.markdown("---")
st.markdown(
    "*Developed as an independent computational biotechnology project bridging"
    " molecular genetics theory with programmatic execution.*"
)
