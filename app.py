import streamlit as st
import re
import numpy as np
import matplotlib.pyplot as plt

# ---------- Twin logic (same as your Colab) ----------

def generate_twin_profile(note):

    text = note.lower()

    uncertainty_terms = ["?", "likely", "unclear", "under evaluation", "await"]
    u_count = sum(text.count(term) for term in uncertainty_terms)

    if u_count >= 6:
        uncertainty = "High"
    elif u_count >= 3:
        uncertainty = "Moderate"
    else:
        uncertainty = "Low"

    severity_markers = ["ventilator", "vasopressor", "metastatic", "post arrest"]
    ethical_terms = ["goals of care", "dnr", "prognosis", "family discussion"]

    severe = any(term in text for term in severity_markers)
    ethical_present = any(term in text for term in ethical_terms)

    if severe and not ethical_present:
        ethical = "High"
    elif ethical_present:
        ethical = "Low"
    else:
        ethical = "Moderate"

    numbers = len(re.findall(r'\d+', text))
    words = len(text.split())
    ratio = numbers / max(words, 1)

    if ratio > 0.15:
        numeric = "High"
    elif ratio > 0.05:
        numeric = "Moderate"
    else:
        numeric = "Low"

    diffusion_terms = ["await", "as per", "to discuss", "will clarify"]
    d_count = sum(text.count(term) for term in diffusion_terms)

    if d_count >= 4:
        diffusion = "High"
    elif d_count >= 2:
        diffusion = "Moderate"
    else:
        diffusion = "Low"

    plan_terms = ["continue", "monitor", "repeat", "follow"]
    p_count = sum(text.count(term) for term in plan_terms)

    if p_count >= 6:
        fragmentation = "High"
    elif p_count >= 3:
        fragmentation = "Moderate"
    else:
        fragmentation = "Low"

    scores = [uncertainty, ethical, numeric, diffusion, fragmentation]
    high_count = scores.count("High")

    if high_count >= 3:
        overall = "High"
    elif high_count >= 1:
        overall = "Moderate"
    else:
        overall = "Low"

    return {
        "uncertainty_density": uncertainty,
        "ethical_silence_risk": ethical,
        "numeric_dominance": numeric,
        "responsibility_diffusion": diffusion,
        "narrative_fragmentation": fragmentation,
        "overall_risk": overall
    }

# ---------- Radar ----------

score_map = {"Low":1,"Moderate":2,"High":3}

def plot_radar(profile):

    labels = list(profile.keys())[:-1]
    values = [score_map[profile[l]] for l in labels]
    values += values[:1]

    angles = np.linspace(0,2*np.pi,len(labels),endpoint=False)
    angles = np.concatenate((angles,[angles[0]]))

    fig = plt.figure(figsize=(5,5))
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    plt.title("ICU Cognitive Digital Twin (Prototype)")

    return fig

# ---------- UI ----------

st.title("ICU Cognitive Digital Twin")

note = st.text_area("Paste ICU Handover Note")

if st.button("Generate Twin"):

    if note.strip() == "":
        st.warning("Please paste a handover note.")
    else:
        profile = generate_twin_profile(note)

        fig = plot_radar(profile)
        st.pyplot(fig)

        st.subheader("Twin Profile")
        st.json(profile)
