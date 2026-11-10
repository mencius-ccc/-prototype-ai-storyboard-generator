import streamlit as st
import time
import hashlib

# Page Configuration
st.set_page_config(
    page_title="AI Storyboard Generator",
    page_icon="🎬",
    layout="wide"
)

# Title & Metadata
st.title("🎬 AI Storyboard & Micro-Proof-of-Concept Generator")
st.subheader("Multi-Agent Workflow for Solo Writers (Dynamic Prototype)")

st.markdown("""
* **Target User:** Solo Screenwriters & Independent Content Creators
* **Architecture:** Multi-Agent Pipeline (Orchestrator, Scene Adapter, Image Bot, Video Bot)
* **Autonomy Level:** Semi-Autonomous (Human-in-the-Loop Step Approval)
""")

st.divider()

# Input Section
st.sidebar.header("1. Script Input & Parameters")
genre = st.sidebar.selectbox("Genre", ["Sci-Fi", "Cyberpunk", "Drama", "Thriller", "Fantasy", "Comedy"])
target_platform = st.sidebar.selectbox("Target Platform Trend", ["TikTok / Shorts (Vertical)", "YouTube (16:9)", "Pitch Deck Trailer"])
user_script = st.sidebar.text_area(
    "Input Raw Script / Concept Draft",
    value="A lonely mechanic in a futuristic neon city discovers an abandoned Android that holds the key to a missing satellite.",
    height=150
)

start_pipeline = st.sidebar.button("🚀 Run Multi-Agent Pipeline")

# Helper function to generate dynamic scenes based on user input text
def generate_dynamic_scenes(script, selected_genre):
    # Clean script text
    words = script.strip().split()
    chunk_size = max(1, len(words) // 3)
    
    part1 = " ".join(words[:chunk_size]) if words else "The opening sequence begins..."
    part2 = " ".join(words[chunk_size:chunk_size*2]) if len(words) > chunk_size else "The conflict intensifies..."
    part3 = " ".join(words[chunk_size*2:]) if len(words) > chunk_size*2 else "The final resolution unfolds..."
    
    scenes = [
        {
            "scene": 1, 
            "title": "Act I: Setup & Introduction",
            "desc": f"Establishing shot in a {selected_genre.lower()} setting. Visualizing: '{part1}'", 
            "hook": f"#{selected_genre} #OpeningScene #ViralHook"
        },
        {
            "scene": 2, 
            "title": "Act II: Conflict & Discovery",
            "desc": f"Deepening tension and core action. Visualizing: '{part2}'", 
            "hook": "#PlotTwist #Engagement #Masterclass"
        },
        {
            "scene": 3, 
            "title": "Act III: Climax & Resolution",
            "desc": f"High-impact conclusion and teaser. Visualizing: '{part3}'", 
            "hook": "#Cliffhanger #ComingSoon #IndieFilm"
        }
    ]
    return scenes

# Agent Processing Logic
if start_pipeline:
    if not user_script.strip():
        st.warning("Please enter a script draft before running the pipeline.")
    else:
        # --- Agent 1: Orchestrator Bot ---
        with st.status("🤖 Agent 1: Main Orchestrator analyzing script & trending metadata...", expanded=True) as status:
            time.sleep(1.2)
            st.write("✅ Script parsed successfully and tokenized.")
            st.write(f"✅ Matched viral pacing and tags for **{target_platform}** under **{genre}** style.")
            status.update(label="Agent 1: Script Analysis Complete!", state="complete")

        # Generate dynamic scenes from user input
        scenes = generate_dynamic_scenes(user_script, genre)

        # --- Agent 2: Scene Adaptation Model ---
        st.subheader("2. Dynamic Visual Scene Breakdown (Scene Adapter Bot)")
        st.info("The Scene Adapter Bot dynamically parsed your script into three optimized storyboard acts:")
        
        for s in scenes:
            st.markdown(f"**{s['title']} (Scene {s['scene']}):** {s['desc']}")
            st.caption(f"Suggested Platform Tags: {s['hook']}")

        st.divider()
        
        # --- Agent 3 & 4: Image & Video Generation ---
        st.subheader("3. Asset Generation (Image & Keyframe Video Bots)")
        st.markdown("*Each scene's visual seed is dynamically hashed and generated from your specific script text.*")
        
        col1, col2, col3 = st.columns(3)
        columns = [col1, col2, col3]
        
        # Unique seed generator based on user text to ensure distinct images per run
        base_seed = int(hashlib.md5(user_script.encode()).hexdigest(), 16) % 10000

        for idx, s in enumerate(scenes):
            with columns[idx]:
                st.markdown(f"### Scene {s['scene']}")
                
                # Dynamic image URL using user script hash + scene index for unique visuals
                img_url = f"https://picsum.photos/seed/{base_seed + idx}/400/225"
                st.image(
                    img_url, 
                    caption=f"Image Bot: {genre} Concept Art (Seed #{base_seed + idx})"
                )
                
                # Varying video placeholder behavior
                if idx == 1:
                    st.video("https://www.w3schools.com/html/movie.mp4")
                else:
                    st.video("https://www.w3schools.com/html/mov_bbb.mp4")
                    
                st.caption(f"Keyframe Video Bot: Act {idx+1} stitched preview.")

        # Approval Callout
        st.success("✅ **Human-in-the-Loop Check:** Dynamic assets successfully generated from your custom script! Review and approve above.")

else:
    st.info("👈 Enter your custom script draft in the sidebar, choose your genre, and click **Run Multi-Agent Pipeline** to test dynamic generation.")
