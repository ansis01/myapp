import streamlit as st
import random
import string
import yt_dlp as youtube_dl
import instaloader
import requests
from requests.exceptions import RequestException

def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

# Fonction pour télécharger une vidéo YouTube
def download_youtube_video(link):
    try:
        if not (("youtube.com/watch?v=") in link and "https://" in link and len(link) <= 75):
            st.write('URL invalide.')
            return None

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'noplaylist': True,
            'quiet': True
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            video_url = info_dict['url']

        if video_url:
            st.write('Téléchargement direct:')
            st.markdown(f'[Télécharger la vidéo ici]({video_url})')
            return video_url
        else:
            st.write('Aucun URL de vidéo trouvé.')
            return None
    except RequestException as e:
        st.write(f'Erreur lors du téléchargement: {e}')
        return None
    except Exception as e:
        st.write(f'Erreur inconnue lors du téléchargement: {e}')
        return None

# Function to download an Instagram reel
def download_instagram_reel(url):
    try:
        if not (("instagram.com/reel/" in url) and "https://" in url and len(url) <= 95):
            st.write('URL invalide.')
            return None

        L = instaloader.Instaloader()
        shortcode = url.split('/')[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        video_url = post.video_url

        if video_url:
            st.write('Téléchargement direct:')
            st.markdown(f'[Télécharger le reel ici]({video_url})')
            return video_url
        else:
            st.write('Aucun reel trouvé.')
            return None
    except RequestException as e:
        st.write(f'Erreur lors du téléchargement: {e}')
        return None
    except Exception as e:
        st.write(f'Erreur inconnue lors du téléchargement: {e}')
        return None
        
# Fonction pour afficher la barre de navigation
def show_navigation():
    st.sidebar.title('Navigation')
    st.sidebar.subheader('Menu')
    st.sidebar.button('Accueil')
    st.sidebar.button('Qui sommes-nous ?')
    st.sidebar.button('Futurs outils')
    st.sidebar.button('Faire un don')
    st.sidebar.button('Partager')

# Page d'accueil
def main_page():
    st.title('Outils en Ligne')
    st.write('Bienvenue sur notre site d\'outils en ligne. Sélectionnez un outil dans le menu à gauche.')

def about_us():
    st.title('Qui sommes-nous ?')
    st.write('Nous sommes une équipe dédiée à fournir des outils en ligne pratiques et utiles.')

def future_tools():
    st.title('Futurs outils')
    st.write('Nous travaillons sur de nouveaux outils pour améliorer votre expérience.')

def donate():
    st.title('Faire un don')
    st.write('Si vous aimez notre site et souhaitez nous soutenir, vous pouvez faire un don via [ce lien](#).')

def share():
    st.title('Partager')
    st.write('Partagez notre site avec vos amis et famille !')

# Sélectionner la page à afficher
show_navigation()
page = st.sidebar.radio("Choisissez une page",
                        ["Accueil", "Qui sommes-nous ?", "Futurs outils", "Faire un don", "Partager"])

if (page == "Accueil"):
    main_page()
elif (page == "Qui sommes-nous ?"):
    about_us()
elif page == "Futurs outils":
    future_tools()
elif page == "Faire un don":
    donate()
elif page == "Partager":
    share()

# Outils disponibles
if page == "Accueil":
    st.header('Outils disponibles')
    option = st.selectbox(
        'Choisissez un outil',
        ['Téléchargeur de Vidéo YouTube',
         'Téléchargeur de Reel Instagram', 'Générateur de Mot de Passe', 'Générateur de Nom Aléatoire']
    )

    if option == 'Générateur de Mot de Passe':
        st.header('Générateur de Mot de Passe')
        length = st.slider('Longueur du mot de passe', 8, 32, 12)
        password = generate_password(length)
        if "@" in password:
            password = generate_password(length)
        st.write(f"Mot de passe généré : {password}")

    elif option == 'Générateur de Nom Aléatoire':
        st.header('Générateur de Nom Aléatoire')
        names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Edward']
        st.write(f"Nom généré : {random.choice(names)}")

    elif option == 'Téléchargeur de Vidéo YouTube':
        st.header('Téléchargeur de Vidéo YouTube')
        url = st.text_input('Entrez l\'URL de la vidéo YouTube', placeholder='Ex: https://www.youtube.com/watch?v=xyz')
        if st.button('Télécharger'):
            if url:
                path = download_youtube_video(url)
            else:
                st.write('Veuillez entrer une URL.')

    elif option == 'Téléchargeur de Reel Instagram':
        st.header('Téléchargeur de Reel Instagram')
        url = st.text_input('Entrez l\'URL du reel Instagram', placeholder='Ex: https://www.instagram.com/reel/...')
        if st.button('Télécharger'):
            if url:
                path = download_instagram_reel(url)
            else:
                st.write('Veuillez entrer une URL.')
