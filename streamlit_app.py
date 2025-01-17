import streamlit as st
import pandas as pd
import json

# Chemin du fichier de sauvegarde
DATA_FILE = "bets_data.json"

# Fonction pour sauvegarder les données dans un fichier JSON
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

# Fonction pour charger les données depuis un fichier JSON
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Initialisation des données stockées
if 'bets' not in st.session_state:
    st.session_state.bets = load_data()

# Titre de l'application
st.title("\U0001F37A Pariez sur le prochain départ au boulot! \U0001F379")
st.markdown("### Faites vos jeux : pints ou cocktails ?")

# Formulaire pour enregistrer un pari
with st.form("bet_form"):
    pseudo = st.text_input("Votre pseudo", placeholder="Entrez votre pseudo", max_chars=20)
    bet_type = st.radio("Type de pari", ["\U0001F37A Pinte de bière", "\U0001F379 Cocktail"])
    amount = st.slider("Quantité (1-5)", min_value=1, max_value=5, step=1)
    suggestion = st.text_input("Prénom du collaborateur", placeholder="Entrez un prénom")

    submitted = st.form_submit_button("Parier")

    if submitted:
        if pseudo and suggestion:
            # Validation des doublons
            existing_bets = [bet for bet in st.session_state.bets if bet['Pseudo'] == pseudo and bet['Prénom'] == suggestion]
            if existing_bets:
                st.error("Vous avez déjà parié sur ce prénom !")
            else:
                # Enregistrer le pari
                new_bet = {
                    'Pseudo': pseudo,
                    'Type de pari': bet_type,
                    'Quantité': amount,
                    'Prénom': suggestion
                }
                st.session_state.bets.append(new_bet)
                save_data(st.session_state.bets)
                st.success(f"Merci pour votre pari, {pseudo} !")
        else:
            st.error("Veuillez remplir tous les champs pour soumettre un pari.")

# Affichage des paris
if st.session_state.bets:
    st.markdown("### \U0001F4C8 Liste des paris en cours")
    bets_df = pd.DataFrame(st.session_state.bets)
    st.dataframe(bets_df.style.set_table_styles([
        {'selector': 'thead th', 'props': [('background-color', '#FFDDC1'), ('color', 'black'), ('font-weight', 'bold')]},
        {'selector': 'tbody td', 'props': [('background-color', '#FFF8E7')]}]))
else:
    st.info("Aucun pari n'a été enregistré pour le moment. Soyez le premier à participer!")

# Footer interactif
st.markdown("---")
st.markdown("**Disclaimer :** Cette application est un projet humoristique et n'encourage pas les paris en milieu professionnel.")
