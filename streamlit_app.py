import streamlit as st
import random
import string
import yt_dlp as youtube_dl
import instaloader

# Custom CSS for styling
st.markdown("""
    <style>
        .download-button {
            display: inline-block;
            padding: 10px 20px;
            font-size: 16px;
            color: #fff;
            background-color: #007bff;
            border-radius: 5px;
            text-decoration: none;
        }
        .download-button:hover {
            background-color: #0056b3;
        }
        .tool-card {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .tool-card h2 {
            margin-bottom: 10px;
        }
        .search-bar {
            width: 100%;
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 5px;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

def fetch_youtube_info(link):
    try:
        if ("script" in link) or len(link) > 75 or ("https://" not in link):
            st.write('URL invalide.')
            return None, None, None

        ydl_opts = {'format': 'mp4'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            video_url = info_dict['url']
            thumbnail_url = info_dict['thumbnail']
            title = info_dict['title']

        return video_url, thumbnail_url, title
    except Exception as e:
        st.write(f'Erreur lors de la récupération des informations: {e}')
        return None, None, None



def show_navigation():
    st.sidebar.title('Navigation')
    st.sidebar.subheader('Menu')
    st.sidebar.button('Accueil')
    st.sidebar.button('Qui sommes-nous ?')
    st.sidebar.button('Futurs outils')
    st.sidebar.button('Faire un don')
    st.sidebar.button('Partager')

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

def search_tool(tools, query):
    return [tool for tool in tools if query.lower() in tool.lower()]

tools = ['','Téléchargeur de Vidéo YouTube', 'Générateur de Mot de Passe']

show_navigation()
page = st.sidebar.radio("Choisissez une page", ["Accueil", "Qui sommes-nous ?", "Futurs outils", "Faire un don", "Partager"])


if page == "Accueil":
    main_page()
elif page == "Qui sommes-nous ?":
    about_us()
elif page == "Futurs outils":
    future_tools()
elif page == "Faire un don":
    donate()
elif page == "Partager":
    share()

# Search bar


if page == "Accueil":
    query = st.text_input('Chercher une outil', placeholder='Rechercher...')
    if query:
        search_results = search_tool(tools, query)
    else:
        search_results = tools
    st.header('Outils disponibles')
    option = st.selectbox('Choisissez un outil', search_results)

    if option == 'Générateur de Mot de Passe':
        st.header('Générateur de Mot de Passe')
        length = st.slider('Longueur du mot de passe', 8, 32, 12)
        password = generate_password(length)
        if "@" in password:
            password = generate_password(length)
        st.write(f"Mot de passe généré : {password}")


    elif option == 'Téléchargeur de Vidéo YouTube':
        st.header('Téléchargeur de Vidéo YouTube')
        url = st.text_input('Entrez l\'URL de la vidéo YouTube', placeholder='Ex: https://www.youtube.com/watch?v=xyz')
        if st.button('Télécharger'):
            if url:
                video_url, thumbnail_url, title = fetch_youtube_info(url)
                if video_url and thumbnail_url and title:
                    st.image(thumbnail_url, caption=title)
                    st.write('Téléchargement direct:')
                    st.markdown(f'<a href="{video_url}" class="download-button">Télécharger la vidéo ici</a>', unsafe_allow_html=True)
            else:
                st.write('Veuillez entrer une URL.')
