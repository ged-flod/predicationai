"""
This script generates a cohesive script based on the transcripts of multiple YouTube videos
using the YouTube Transcript API and the GoogleGemini API.

"""

import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from pytube import YouTube

from style import style
from structure import structure
from schemas import schemas
from options import sermon_lengths
from options import orateurs


# Streamlit app configuration
st.set_page_config(page_title="Prediction AI", page_icon=":video_camera:")

# Page title
st.title("Prediction AI")
st.subheader("Un générateur de prédictions par Intelligence Artificielle")
st.divider()

# User input for YouTube video IDs
st.sidebar.header("MENU")

# INPUTS
theme = st.sidebar.text_input(label="Theme", value="")
objectifs = st.sidebar.text_input(label="Objectifs du sermon ", value="")
textes = st.sidebar.text_input(label="Textes de bases ", value="", help="Proposer le texte de base")
contexte = st.sidebar.text_area(label="Mise en contexte ", value="", help="Expliquer le thème/Textes de base")

# STRUCTURE
structure_description = "Voici le model de structure de prédication"
structure_choice = st.sidebar.selectbox('Choisissez une structure de prédication:', list(structure.keys()), help=structure_description)
# SCHEMAS
schemas_description = "Pour développer un sous-point de manière structurée et efficace dans une prédication, il est utile de suivre des schémas ou des structures claires. Voici plusieurs types de schémas que vous pouvez utiliser "
schemas_choice = st.sidebar.selectbox('Choisissez le Schéma de prédication:', list(schemas.keys()), help=schemas_description)
# STYLE
style_option_liste = list(style.keys())
style_description = "Voici le model de style de prédication"
style_option = st.sidebar.selectbox("Choisissez un style de prédication:", style_option_liste, help=style_description)
# TONALITE
tone = st.sidebar.text_input(label="Choisir la Tonalite ", value="")
# ORATEURS
orateur = st.sidebar.selectbox("Choisissez un orateur:", orateurs)
# SERMON_LENGTH
sermon_length = st.sidebar.selectbox("Choisissez une longueur de sermon:", sermon_lengths)






# User input for Gemini API key
# api_key = st.sidebar.text_input("Gemini API Key", type="password", value="AIzaSyDybIK0Bw6WYe-ZFM235KWRL2xxYuX8ryQ")
api_key = "AIzaSyDybIK0Bw6WYe-ZFM235KWRL2xxYuX8ryQ"

if st.sidebar.button("Générateur la prédiction"):
    
    # Fetch transcripts for all videos
    # st.write("Fetching YouTube videos ...")
    # st.success("Transcripts fetched successfully!")
    if not theme:
        st.error("Veillez entrer le thème")
        st.stop()
    
    # Generate prompt template
    role = "Un générateur de prédictions"
    prompt = """
    Create an one complete script from all these video transcriptions by synthesizing information from various sources into a single one coherent context by following the following Instructions:
    """
    instructions = contexte
    prompt_template = f"""ton role est: {role}.\n
    
    Générer une prédication en utilisant les informations suivantes:\n
    Thème: {theme}\n
    Objectifs du sermon: {objectifs}\n
    Textes de bases: {textes}\n
    Mise en contexte: {contexte}\n
    
    Structure de prédication: {structure_choice}\n
    Schéma de prédication: {schemas_choice}\n
    Style de prédication: {style_option}\n
    
    Tonalité: {tone}\n
    Orateur: {orateur}\n
    Longueur du sermon: {sermon_length}\n

    Veuillez créer une prédication complète qui suit ces directives et qui inspire et édifie l'auditoire. Assurez-vous d'inclure des exemples pertinents, des histoires ou des anecdotes, des citations des textes de bases, et des appels à l'action clairs. Le ton doit correspondre à la tonalité choisie et refléter le style de l'orateur sélectionné.
    """

    # Configure Gemini API
    try:
        st.write("génération de la prédiction...")
        genai.configure(api_key=api_key)
        # Choose a model
        model = genai.GenerativeModel('gemini-pro')
        # Generate content
        response = model.generate_content(prompt_template)
        st.subheader("La prédiction genéré:")
        st.write(response.text)
        # st.subheader("Generated Script Editable")
        # st.text_area(label="la prédiction", value=response.text, height=500)
    except Exception as e:
        st.error(f"Error génération de la prédiction: {e}")


