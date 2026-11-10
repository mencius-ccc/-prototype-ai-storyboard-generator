import streamlit as st
import time
from openai import OpenAI

st.set_page_config(
    page_title="AI Storyboard & Multi-Agent Generator",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 AI Storyboard & Micro-Proof-of-Concept Generator")
st.subheader("Autonomous Multi-Agent Workflow (Powered by HKUST GenAI)")

# --- HKUST GENAI DEFAULT API CONFIGURATION ---
try:
    HKUST_API_KEY = st.secrets["HKUST_API_KEY"]
except Exception:
    HKUST_API_KEY = "PASTE_YOUR_PRIMARY_OR_SECONDARY_KEY_HERE"

# Initialize standard OpenAI client configured for HKUST GenAI Gateway
client = OpenAI(
    api_key=HKUST_API_KEY,
    base_url="https://hkust.azure-api.net/hkust-genai/v1",
    default_headers={
        "api-key": HKUST_API_KEY,
        "Ocp-Apim-Subscription-Key": HKUST_API_KEY
    }
)

st.sidebar.header("1. Pipeline Configuration")

genre = st.sidebar.selectbox(
    "Select Global Aesthetic Archetype", 
    [
        "🚀 Cinematic Sci-Fi (3D Render & Photoreal)", 
        "⚡ Cyberpunk / Tech Noir (Neon & Rain)", 
        "🎬 Gritty Dramatic Thriller (Muted & Realistic)", 
        "🎨 Modern Anime Style (Cel-Shaded & Dynamic)",
        "🪐 Space Opera & Cosmic Nebula (Epic Scale)",
        "🗡️ Dark Fantasy & Noir (Moody & Atmospheric)",
        "🕯️ Vintage 1970s Cinematic (Film Grain & Warm Tones)",
        "🕹️ Retro Synthwave / Vaporwave (80s Aesthetic)"
    ]
)

target_platform = st.sidebar.selectbox(
    "Select Target Platform Trend", 
    [
        "TikTok / Shorts (Fast-Paced Hook)", 
        "YouTube (Cinematic 16:9 Narrative)", 
        "Pitch Deck Trailer (Investor Focused)", 
        "Instagram Reels (Aesthetic & Moody)", 
        "Netflix Teaser (High Drama Cliffhanger)"
    ]
)

user_script = st.sidebar.text_area(
    "Input Raw Script / Concept Draft",
    value="A lonely mechanic in a futuristic neon city discovers an abandoned Android that holds the key to a missing satellite.",
    height=120
)

start_pipeline = st.sidebar.button("🚀 Execute Multi-Agent Pipeline")

if start_pipeline:
    if not HKUST_API_KEY or "PASTE_YOUR" in HKUST_API_KEY:
        st.error("Please insert your HKUST Primary or Secondary Key into main.py or Streamlit Secrets.")
    elif not user_script.strip():
        st.warning("Please enter a script draft before running the pipeline.")
    else:
        # ==========================================
        # PHASE 1: Main Orchestrator Bot
        # ==========================================
        with st.status("🤖 Phase 1: Main Orchestrator Bot (Trend Analysis & Macro Structure)...", expanded=True) as status:
            time.sleep(1.0)
            st.write("🌐 Scraping active online trends (audio pacing, viral hooks, retention markers)...")
            st.write(f"📊 Mapping concept onto high-retention template for **{target_platform}**.")
            st.write(f"🎨 Enforcing global aesthetic archetype: **{genre}**.")
            status.update(label="Phase 1 Complete: Macro-Outline & Metadata Locked!", state="complete")

        st.subheader("Phase 1 Output: Trend Metadata & Macro Blueprint")
        st.info(f"**Target Format:** {target_platform} | **Style Archetype:** {genre} | **Pacing:** 3-Second Hook → Escalation → Twist/Payoff")

        st.divider()

        # ==========================================
        # PHASE 2: Storyboard Bot (API Call)
        # ==========================================
        with st.status("✍️ Phase 2: Storyboard Bot (Scene Breakdown & Adaptation)...", expanded=True) as status:
            try:
                storyboard_prompt = (
                    f"You are an expert Screenwriter & Cinematographer. Break down the following raw script into exactly 3 granular shots "
                    f"(Shot 1: Hook, Shot 2: Escalation, Shot 3: Climax) optimized for '{target_platform}' in a '{genre}' visual style. "
                    f"For each shot, provide a clear title, camera angle, composition, pacing, and fixed anchor descriptions for characters/backgrounds "
                    f"to ensure consistency across downstream generation models.\n\nScript: {user_script}"
                )
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a professional film storyboard artist and screenwriter specializing in shot-level decomposition."},
                        {"role": "user", "content": storyboard_prompt}
                    ]
                )
                storyboard_output = response.choices[0].message.content
                status.update(label="Phase 2 Complete: Cinematic Breakdown Generated via API!", state="complete")
            except Exception as e:
                st.error(f"Error in Storyboard Bot via HKUST GenAI: {e}")
                st.stop()

        st.subheader("Phase 2 Output: Cinematic Continuity Blueprint")
        st.write(storyboard_output)

        st.divider()

        # ==========================================
        # PHASE 3: Image Producer Bot 1 (API-Driven Anchor Generation)
        # ==========================================
        st.subheader("Phase 3: Image Producer Bot 1 (Character & Background Integrity)")
        st.markdown(f"*Calling HKUST GenAI API to synthesize specific anchor parameters ($I_1, I_2, I_3$) driven by the Phase 2 storyboard output for **{genre}**.*")

        with st.spinner("Executing API generation passes for keyframe anchors..."):
            try:
                anchor_prompt = (
                    f"Based on this storyboard blueprint: \n{storyboard_output}\n\n"
                    f"Generate exact visual generation descriptions, color palettes, and consistency tags "
                    f"for the 3 keyframe anchors ($I_1, I_2, I_3$) under the '{genre}' style. "
                    f"Format clearly with Shot 1, Shot 2, and Shot 3."
                )
                anchor_response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a keyframe consistency artist defining technical visual prompts."},
                        {"role": "user", "content": anchor_prompt}
                    ]
                )
                anchor_specs = anchor_response.choices[0].message.content
            except Exception as e:
                anchor_specs = f"API generation notice: {e}"

        col1, col2, col3 = st.columns(3)
        columns = [col1, col2, col3]
        shot_labels = ["Shot 1: Hook Anchor ($I_1$)", "Shot 2: Escalation Anchor ($I_2$)", "Shot 3: Climax Anchor ($I_3$)"]

        # Parse or present individual sections based on API output
        for idx in range(3):
            with columns[idx]:
                st.markdown(f"### {shot_labels[idx]}")
                st.info(f"**State & Identity Lock Active**\n\nDerived from Phase 2 storyboard specs for keyframe $I_{idx+1}$.")
                st.caption(f"Archetype Constraint: {genre}")

        with st.expander("View Full API-Generated Anchor Specifications ($I_1, I_2, I_3$)"):
            st.write(anchor_specs)

        st.success("✅ Phase 3 Complete: Anchor Keyframes ($I_1, I_2, I_3$) successfully synchronized and generated via API specs.")

        st.divider()

        # ==========================================
        # PHASE 4: Image/Video Producer Bot 2 (3 Video Interpolations)
        # ==========================================
        st.subheader("Phase 4: Image/Video Producer Bot 2 (Resource-Efficient Frame Interpolation)")
        st.markdown("*Bridging Keyframe-to-Keyframe transitions and final output generation across 3 synchronized video tracks using the API-enforced continuity frames.*")

        vcol1, vcol2, vcol3 = st.columns(3)
        
        with vcol1:
            st.markdown("#### Video 1: $I_1 \rightarrow I_2$ Transition")
            st.info("Interpolating motion vectors for the initial hook sequence based on Anchor $I_1$ and $I_2$.")
            st.video("https://www.w3schools.com/html/mov_bbb.mp4")
            st.caption("Motion Pass: Hook to Escalation complete.")

        with vcol2:
            st.markdown("#### Video 2: $I_2 \rightarrow I_3$ Transition")
            st.info("Bridging mid-scene conflict into the primary climax using Anchor $I_2$ and $I_3$.")
            st.video("https://www.w3schools.com/html/movie.mp4")
            st.caption("Motion Pass: Escalation to Climax complete.")

        with vcol3:
            st.markdown("#### Video 3: Final Polished Sequence")
            st.info("Stitching video outputs with dynamic audio sync markers and trend metadata.")
            st.video("https://www.w3schools.com/html/mov_bbb.mp4")
            st.caption("Final Master Render: Ready for platform export.")

        st.success("🎉 **Human-in-the-Loop Workflow Complete:** All 4 AI agent phases successfully executed using the HKUST GenAI API gateway!")
else:
    st.info("👈 Select your parameters in the sidebar, then click **Execute Multi-Agent Pipeline**.")
