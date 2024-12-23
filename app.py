import streamlit as st
import pandas as pd
import calc
import present
import time

@st.cache_data
def load_data():
    return (pd.read_csv('data/bc_game.csv'), pd.read_csv('data/bc_streaming_offer.csv'), pd.read_csv('data/bc_streaming_package.csv'))

@st.cache_data
def cached_calculation(choice, anbieter, abdeckung, preis):
    return calc.greedy_set_cover(get_game_ids(choice), anbieter, abdeckung, preis), \
           calc.ILP_set_cover(get_game_ids(choice), anbieter, abdeckung, preis)


# Einlesen aller Tabellen
game, streaming_offer, streaming_packages = load_data()

# Funktion mit Rückgabe aller Spiele für ein Team
def get_game_ids(team_list):
    filtered_games = game[game['team_home'].isin(team_list) | game['team_away'].isin(team_list)]
    return filtered_games['id'].tolist()

# Extrahierung aller nötigen Daten für das LpProblem
teams = list(set(game["team_home"]).union(set(game["team_away"])))
anbieter = streaming_packages["id"].tolist()
preis = dict(zip(streaming_packages["id"], streaming_packages["monthly_price_yearly_subscription_in_cents"]))
abdeckung = streaming_offer[streaming_offer["live"] == 1].groupby("streaming_package_id")["game_id"].apply(list).to_dict()

# App-Titel
st.title("Streaminganbieter Vergleich")

# Multi-Select Dropdown für Lieblingsvereine
choice = st.multiselect(
    "Wähle deine Lieblingsvereine:",
    options=teams,
    default=["Bayern München"]
)



if st.button("Berechnung starten"):
    if choice:
        with st.spinner("Lösung wird noch berechnet..."):
            greedy = calc.greedy_set_cover(get_game_ids(choice), anbieter, abdeckung, preis)
            st.subheader("Ausgewählte Anbieter:")
            
            greedy_anbieter = present.anbieter_info(greedy)
            with st.empty():
                st.table(greedy_anbieter)

                optimum = calc.ILP_set_cover(get_game_ids(choice), anbieter, abdeckung, preis)
                optimum_anbieter = present.anbieter_info(optimum)

                if greedy["preis"] > optimum["preis"]:
                    st.table(optimum_anbieter)

            with st.expander("Nicht gezeigte Spiele:"):
                for spiel_id in optimum["ungedeckte_spiele"]:
                    spiel = game[game["id"]==spiel_id]
                    st.write(f"{spiel['team_home'].iloc[0]} gegen {spiel['team_away'].iloc[0]} - {spiel['tournament_name'].iloc[0]}")

            with st.expander("Liga Informationen der Anbieter:"):
                liga_optimum = present.liga_info(optimum)
                st.table(liga_optimum)

            with st.expander("Ausührliche Infos der Anbieter (alle möglichen Spiele)"):
                optimum_spiele = present.full_info(optimum)
                st.table(optimum_spiele)
    else:
        st.warning("Bitte wähle mindestens ein Team aus.")

