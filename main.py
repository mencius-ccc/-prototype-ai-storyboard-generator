import streamlit as st
import time
import hashlib

st.set_page_config(
    page_title="AI Storyboard Generator",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 AI Storyboard & Micro-Proof-of-Concept Generator")
st.subheader("Multi-Agent Workflow for Solo Writers (Dynamic Script Integration)")

st.sidebar.header("1. Script Input & Parameters")

genre = st.sidebar.selectbox(
    "Select Genre", 
    ["🚀 Sci-Fi / Space", "⚡ Cyberpunk / Tech", "🎬 Dramatic Thriller"]
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

start_pipeline = st.sidebar.button("🚀 Run Multi-Agent Pipeline")

# Preset framework database for all 15 combinations
MATRIX_DATA = {
    ("🚀 Sci-Fi / Space", "TikTok / Shorts (Fast-Paced Hook)"): {
        "title": "The Dark Edge of the Orbit",
        "style": "Vertical 9:16, rapid jump cuts (0.5s), heavy bass drops, glitch transitions.",
        "hooks": ["Act I: Fast countdown HUD on a broken helmet. Focus: ", "Act II: System failure alarms blare. Focus: ", "Act III: Gasping breath cutoff right as crisis peaks. Focus: "]
    },
    ("🚀 Sci-Fi / Space", "YouTube (Cinematic 16:9 Narrative)"): {
        "title": "Echoes of Proxima",
        "style": "Wide 16:9 anamorphic letterbox, slow orchestral buildup, deep-space color grade.",
        "hooks": ["Act I: Sweeping alien landscape log recording. Focus: ", "Act II: Power grid fails as mystery deepens. Focus: ", "Act III: Existential voiceover over grand cosmic scale. Focus: "]
    },
    ("🚀 Sci-Fi / Space", "Pitch Deck Trailer (Investor Focused)"): {
        "title": "Project Kepler-9",
        "style": "Sleek sci-fi UI overlays, photorealistic visual effects proof-of-concept.",
        "hooks": ["Act I: High-concept IP premise reel. Focus: ", "Act II: Survival stakes & technical mechanics. Focus: ", "Act III: Production scale & commercial franchise appeal. Focus: "]
    },
    ("🚀 Sci-Fi / Space", "Instagram Reels (Aesthetic & Moody)"): {
        "title": "Starlight Drift",
        "style": "Warm lens flares, neon engine trails, ambient synth music, vertical frame.",
        "hooks": ["Act I: Atmospheric lens flare opening. Focus: ", "Act II: Quiet tension in dark ship corridors. Focus: ", "Act III: Minimalist typography and visual mood-board climax. Focus: "]
    },
    ("🚀 Sci-Fi / Space", "Netflix Teaser (High Drama Cliffhanger)"): {
        "title": "The Signal Beyond",
        "style": "HDR cinematography, dramatic lighting contrast, swelling choir score.",
        "hooks": ["Act I: Earth command center picks up distress beacon. Focus: ", "Act II: Decrypting the encrypted warning. Focus: ", "Act III: Massive unexplained blast; cuts to black. Focus: "]
    },
    ("⚡ Cyberpunk / Tech", "TikTok / Shorts (Fast-Paced Hook)"): {
        "title": "Glitch City: Overdrive",
        "style": "High-contrast neon, quick cutbeats to synthwave, screen shake.",
        "hooks": ["Act I: POV rooftop chase fleeing pursuit drones. Focus: ", "Act II: Glitch cuts of cyber upgrades and hacking. Focus: ", "Act III: Rapid katana clash into title drop. Focus: "]
    },
    ("⚡ Cyberpunk / Tech", "YouTube (Cinematic 16:9 Narrative)"): {
        "title": "Neon Ghost",
        "style": "4K 16:9 widescreen, heavy rain atmospheric noise, synth-drone score.",
        "hooks": ["Act I: Rogue investigator navigating rain-slicked alleys. Focus: ", "Act II: Uncovering memory market network. Focus: ", "Act III: Dialogue clash: corporate greed vs. consciousness. Focus: "]
    },
    ("⚡ Cyberpunk / Tech", "Pitch Deck Trailer (Investor Focused)"): {
        "title": "Neural Net: 2099",
        "style": "Clean infographics, character concept highlights, action snippets.",
        "hooks": ["Act I: Faction designs: megacorps vs. subterranean hackers. Focus: ", "Act II: High-octane cyber-combat showcase. Focus: ", "Act III: Gaming/streaming market crossover metrics. Focus: "]
    },
    ("⚡ Cyberpunk / Tech", "Instagram Reels (Aesthetic & Moody)"): {
        "title": "Chrome & Rain",
        "style": "Lo-fi synth beats, film grain, magenta/cyan palette, vertical frame.",
        "hooks": ["Act I: Neon light reflecting in street puddles. Focus: ", "Act II: Cybernetic arm repairs in back alleys. Focus: ", "Act III: Human intimacy amidst high-tech isolation. Focus: "]
    },
    ("⚡ Cyberpunk / Tech", "Netflix Teaser (High Drama Cliffhanger)"): {
        "title": "System Wipe",
        "style": "Sharp cinematic framing, ticking sound design, sudden silence shifts.",
        "hooks": ["Act I: Corporate launch of global neural link. Focus: ", "Act II: Countdown clock initiates global wipe. Focus: ", "Act III: Screen flickers off at 00:00:01. Focus: "]
    },
    ("🎬 Dramatic Thriller", "TikTok / Shorts (Fast-Paced Hook)"): {
        "title": "30 Seconds to Alibi",
        "style": "Fast pacing, rapid pulse audio beat, dynamic text.",
        "hooks": ["Act I: '30 seconds to clean the room before police knock.' Focus: ", "Act II: Rapid panic: spilled wine, broken watch, mirror shot. Focus: ", "Act III: Door handle turns right at audio peak. Focus: "]
    },
    ("🎬 Dramatic Thriller", "YouTube (Cinematic 16:9 Narrative)"): {
        "title": "The Glass House",
        "style": "Cold blue tones, symmetrical 16:9 framing, slow pans, ominous score.",
        "hooks": ["Act I: Dinner party in an isolated estate. Focus: ", "Act II: Arrival of unwelcome guest with black envelope. Focus: ", "Act III: Deceit and past secrets unravel in tense dialogue. Focus: "]
    },
    ("🎬 Dramatic Thriller", "Pitch Deck Trailer (Investor Focused)"): {
        "title": "Silent Verdict",
        "style": "Critical quotes layout, plot flowcharts, intense performance clips.",
        "hooks": ["Act I: Character-driven psychological setup. Focus: ", "Act II: Low-budget high-ROI location efficiency. Focus: ", "Act III: Festival acclaim & award-season pitch beats. Focus: "]
    },
    ("🎬 Dramatic Thriller", "Instagram Reels (Aesthetic & Moody)"): {
        "title": "Shadows on Glass",
        "style": "Slow-motion, muted earth tones, dramatic shadows, piano track.",
        "hooks": ["Act I: Trembling hand over a silent phone. Focus: ", "Act II: Headlights cutting through thick fog. Focus: ", "Act III: Eyes watching across a crowded room. Focus: "]
    },
    ("🎬 Dramatic Thriller", "Netflix Teaser (High Drama Cliffhanger)"): {
        "title": "Lies We Bury",
        "style": "Fast montage to standstill, heavy bass thuds, dramatic cuts.",
        "hooks": ["Act I: Intercutting courtroom trial with river flashbacks. Focus: ", "Act II: Prosecutor delivers the damning question. Focus: ", "Act III: Key witness grins directly at the camera. Focus: "]
    }
}

if start_pipeline:
    if not user_script.strip():
        st.warning("Please enter a script draft before running the pipeline.")
    else:
        concept_data = MATRIX_DATA.get((genre, target_platform))
        
        # Split user's script into 3 dynamic narrative chunks
        words = user_script.strip().split()
        chunk_size = max(1, len(words) // 3)
        act_texts = [
            " ".join(words[:chunk_size]) if words else "The story begins...",
            " ".join(words[chunk_size:chunk_size*2]) if len(words) > chunk_size else "The conflict deepens...",
            " ".join(words[chunk_size*2:]) if len(words) > chunk_size*2 else "The climax occurs..."
        ]

        with st.status(f"🤖 Agent 1: Parsing user script into **{concept_data['title']}**...", expanded=True) as status:
            time.sleep(1.0)
            st.write("✅ Tokenized raw input script into 3 thematic beats.")
            st.write(f"✅ Blended user story content with **{genre}** under **{target_platform}** template.")
            status.update(label="Agent 1: Script Integration Complete!", state="complete")

        st.subheader(f"2. Concept Adaptation: {concept_data['title']}")
        st.markdown(f"**Visual Style & Framing:** {concept_data['style']}")
        
        st.divider()
        st.subheader("3. Integrated Storyboard & Multi-Modal Assets")
        
        col1, col2, col3 = st.columns(3)
        columns = [col1, col2, col3]
        
        base_seed = int(hashlib.md5((user_script + genre + target_platform).encode()).hexdigest(), 16) % 10000

        for idx, act_text in enumerate(act_texts):
            with columns[idx]:
                st.markdown(f"### Act {idx+1}")
                
                # Combine matrix platform hook with the user's specific script text
                full_description = f"{concept_data['hooks'][idx]}\"{act_text}\""
                st.info(full_description)
                
                img_url = f"https://picsum.photos/seed/{base_seed + idx}/400/225"
                st.image(img_url, caption=f"Keyframe {idx+1} (Seed #{base_seed + idx})")
                
                if idx == 1:
                    st.video("https://www.w3schools.com/html/movie.mp4")
                else:
                    st.video("https://www.w3schools.com/html/mov_bbb.mp4")
                    
                st.caption(f"Act {idx+1} Keyframe Render Preview")

        st.success("✅ **Human-in-the-Loop Check:** Custom script input successfully synthesized across the 3×5 matrix!")
else:
    st.info("👈 Select your parameters, type your script in the sidebar, and click **Run Multi-Agent Pipeline**.")
