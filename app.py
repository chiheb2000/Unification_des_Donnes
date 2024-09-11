import streamlit as st
import pickle
import pandas as pd
import time  
import matplotlib.pyplot as plt


model_path = "dectree_model (3).p" 
def load_model():
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model

tree_model = load_model()

def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            # Appliquer la fonction Soundex aux colonnes Prénom et Nom
            if 'Prénom' in df.columns and 'Nom' in df.columns:
                df['Prénom_Soundex'] = df['Prénom'].apply(soundex)
                df['Nom_Soundex'] = df['Nom'].apply(soundex)
                st.session_state['data_loaded'] = True  # Marquer les données comme chargées
                st.session_state['df'] = df
                st.success("Données préparées avec succès !")
            else:
                st.error("Le fichier doit contenir les colonnes 'Nom' et 'Prénom'.")
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier : {e}")
    else:
        st.error("Veuillez téléverser un fichier CSV.")
        
def soundex(name):
    soundex_mapping = {
        'a': '', 'e': '', 'i': '', 'o': '', 'u': '', 'y': '', 'h': '', 'w': '',
        'b': '1', 'f': '1', 'p': '1', 'v': '1',
        'c': '2', 'g': '2', 'j': '2', 'k': '2', 'q': '2', 's': '2', 'x': '2', 'z': '2',
        'd': '3', 't': '3',
        'l': '4',
        'm': '5', 'n': '5',
        'r': '6'
    }
    
    name = name.lower().strip()
    first_letter = name[0].upper()
    tail = name[1:]

    soundex_numbers = [soundex_mapping.get(char, '') for char in tail]

    filtered_numbers = []
    for number in soundex_numbers:
        if not filtered_numbers or (number != filtered_numbers[-1]):
            filtered_numbers.append(number)

    filtered_numbers = [num for num in filtered_numbers if num != '']

    soundex_code = first_letter + ''.join(filtered_numbers)[:3]

    soundex_code = soundex_code.ljust(4, '0')

    return soundex_code

def rechercher_par_soundex(nom, prenom, df):
    nom_soundex = soundex(nom)
    prenom_soundex = soundex(prenom)

    correspondances = df[(df['Nom_Soundex'] == nom_soundex) & 
                              (df['Prénom_Soundex'] == prenom_soundex)]
    return correspondances

def ton_modele_verification(cin, email, date_naissance, sexe, lieu, existing_record):
    new_pair = {
        'Email_Match': int(email == existing_record['Email']),
        'CIN_Match': int(cin == existing_record['CIN']),
        'Date_Match': int(date_naissance == existing_record['Date de naissance']),
        'Sexe_Match': int(sexe == existing_record['Sexe']),
        'Lieu_Match': int(lieu == existing_record['Lieu']),
    }
    score = 0

    if new_pair['CIN_Match'] or new_pair['Email_Match']:
        score = 100  
    else:
        if (cin == None) and (email == ''):
            total_criteria = 5  
            matches = new_pair['Date_Match'] + new_pair['Sexe_Match'] + new_pair['Lieu_Match']
            score = (matches / total_criteria) * 100
        else:  
            score = 0

    new_pair_df = pd.DataFrame([new_pair])

    prediction = tree_model.predict(new_pair_df)

    return prediction[0], score  

def create_progress_bar(percentage):
    bar_length = 10  
    filled_length = int(percentage / 10)  
    bar = '█' * filled_length + '-' * (bar_length - filled_length) 
    return f"{bar} {percentage:.1f}%"  

if 'prenom' not in st.session_state:
    st.session_state['prenom'] = ''
if 'nom' not in st.session_state:
    st.session_state['nom'] = ''
if 'correspondances' not in st.session_state:
    st.session_state['correspondances'] = pd.DataFrame()
if 'predictions' not in st.session_state:
    st.session_state['predictions'] = pd.DataFrame()  
if 'data_loaded' not in st.session_state:
    st.session_state['data_loaded'] = False
    
def reset_state():
    """Réinitialiser l'état de l'application."""
    st.session_state['prenom'] = ''
    st.session_state['nom'] = ''
    st.session_state['correspondances'] = pd.DataFrame()
    st.session_state['predictions'] = pd.DataFrame()
    st.session_state['data_loaded'] = False
def main():
    st.set_page_config(page_title="Unification des Données", layout="wide")
    
    logo_path = "Logo.png"  
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.image(logo_path, width=200)
    st.markdown('<p class="title">👥 Plateforme Unification des Données 👥 </p>', unsafe_allow_html=True)

    st.sidebar.header("Étape 1 : Charger le fichier CSV")
    uploaded_file = st.sidebar.file_uploader("Téléverser un fichier CSV", type=["csv"])
    
    if st.sidebar.button("Charger et Préparer les Données"):
        reset_state()
        load_data(uploaded_file)
    
    if st.session_state['data_loaded']:
        st.sidebar.header("Formulaire")

    
        new_prenom = st.sidebar.text_input("Entrez votre prénom", value=st.session_state['prenom'])
        new_nom = st.sidebar.text_input("Entrez votre nom", value=st.session_state['nom'])

        if st.sidebar.button("Vérifier 🔎") or (new_nom != st.session_state['nom']) or (new_prenom != st.session_state['prenom']):
            st.session_state['nom'] = new_nom
            st.session_state['prenom'] = new_prenom
            st.session_state['predictions'] = pd.DataFrame() 

            if st.session_state['nom'] and st.session_state['prenom']:
                st.sidebar.write(f"Recherche pour {st.session_state['nom']} {st.session_state['prenom']} en cours...")
                progress_bar = st.sidebar.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.01)  
                    progress_bar.progress(percent_complete + 1)
                
                st.session_state['correspondances'] = rechercher_par_soundex(st.session_state['nom'], st.session_state['prenom'], st.session_state['df'])

                if not st.session_state['correspondances'].empty:

                    st.write(f"{len(st.session_state['correspondances'])} correspondance(s) trouvée(s) 🔎:")
                    st.dataframe(st.session_state['correspondances'][['Nom', 'Prénom', 'CIN', 'Date de naissance', 'Lieu', 'Email', 'Sexe']])
                else:
                    st.warning("⚠️ Aucune correspondance trouvée. Veuillez vérifier vos entrées.")
            else:
                st.error("Veuillez entrer un nom et un prénom.")

        if not st.session_state['correspondances'].empty:
            st.subheader("Visualisation des correspondances")
            col1, col2, col3 = st.columns(3)

            with col1:
                plt.figure(figsize=(10, 6))
                st.session_state['correspondances']['Lieu'].value_counts().plot(kind='bar')
                plt.title("Nombre de correspondances par lieu")
                plt.xlabel("Lieu")
                plt.ylabel("Nombre de correspondances")
                st.pyplot(plt)

            with col2:
                plt.figure(figsize=(6, 4))
                st.session_state['correspondances']['Sexe'].value_counts().plot(kind='bar', color='orange')
                plt.title("Répartition des sexes")
                plt.xlabel("Sexe")
                plt.ylabel("Nombre")
                st.pyplot(plt)

            with col3:
                plt.figure(figsize=(10, 6))
                birthdate_counts = st.session_state['correspondances']['Date de naissance'].value_counts()
                plt.pie(birthdate_counts, labels=birthdate_counts.index, autopct='%1.1f%%', startangle=90)
                plt.title("Répartition des dates de naissance")
                plt.axis('equal') 
                st.pyplot(plt)

        if not st.session_state['correspondances'].empty:
            st.markdown('<p class="subtitle">Étape 2 : Ajouter des informations supplémentaires pour prédiction</p>', unsafe_allow_html=True)

            cin_str = st.text_input("🪪 Entrez votre CIN (numérique uniquement)")
            if cin_str:
                try:
                    cin = int(cin_str)
                except ValueError:
                    st.error("Veuillez entrer un numéro de CIN valide.")
                    cin = None
            else:
                cin = None

            email = st.text_input(" 📧 Entrez votre email")
            date_naissance = st.text_input("🗓️ Entrez votre date de naissance (format: jj/mm/aaaa)")
            sexe = st.selectbox("🚻 Sélectionnez votre sexe", ["M", "F"])
            lieu = st.text_input("🗺️ Entrez votre lieu")

            predire_bouton = st.button("Prédire avec le modèle")
            if predire_bouton:
                result_df = pd.DataFrame()

                for idx, existing_record in st.session_state['correspondances'].iterrows():
                    prediction, score = ton_modele_verification(cin, email, date_naissance, sexe, lieu, existing_record)
                    person_info = st.session_state['correspondances'].loc[[idx], ['Nom', 'Prénom', 'CIN', 'Date de naissance', 'Lieu', 'Email', 'Sexe']].copy()
                    person_info['Barre de progression'] = create_progress_bar(score)  
                    person_info['Prediction'] = "✅ Même personne" if prediction == 1 else "❌ Personne différente"
                    result_df = pd.concat([result_df, person_info], ignore_index=True)

                st.session_state['predictions'] = result_df  

        
        if not st.session_state['predictions'].empty:  
            st.subheader("Résultats des prédictions :")
            st.dataframe(st.session_state['predictions'])

if __name__ == "__main__":
    main()
