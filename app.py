import streamlit as st
import pandas as pd
import calc
import present
import time

@st.cache_data
def load_data():
    return (pd.read_csv('data/bc_game.csv'), pd.read_csv('data/bc_streaming_offer.csv'), pd.read_csv('data/bc_streaming_package.csv'))

@st.cache_data
def cached_calculation(choice, providers, coverage, price):
    return calc.greedy_set_cover(get_game_ids(choice), providers, coverage, price), \
           calc.ILP_set_cover(get_game_ids(choice), providers, coverage, price)


# Load all tables
game, streaming_offer, streaming_packages = load_data()

# Function to return all games for a team
def get_game_ids(team_list):
    filtered_games = game[game['team_home'].isin(team_list) | game['team_away'].isin(team_list)]
    return filtered_games['id'].tolist()

# Extract all necessary data for the LP problem
teams = list(set(game["team_home"]).union(set(game["team_away"])))
providers = streaming_packages["id"].tolist()
price = dict(zip(streaming_packages["id"], streaming_packages["monthly_price_yearly_subscription_in_cents"]))
coverage = streaming_offer[streaming_offer["live"] == 1].groupby("streaming_package_id")["game_id"].apply(list).to_dict()

# App title
st.title("Streaming Provider Comparison")

# Multi-Select Dropdown for favorite teams
choice = st.multiselect(
    "Select your favorite teams:",
    options=teams,
    default=["Bayern München"]
)

if st.button("Start Calculation"):
    if choice:
        with st.spinner("Calculating the solution..."):
            greedy = calc.greedy_set_cover(get_game_ids(choice), providers, coverage, price)
            st.subheader("Selected Providers:")
            
            greedy_providers = present.anbieter_info(greedy)
            with st.empty():
                st.table(greedy_providers)

                optimum = calc.ILP_set_cover(get_game_ids(choice), providers, coverage, price)
                optimum_providers = present.anbieter_info(optimum)

                if greedy["cost"] > optimum["cost"]:
                    st.table(optimum_providers)
                else:
                    optimum = greedy

            with st.expander("Uncovered Games:"):
                for game_id in optimum["uncovered_games"]:
                    game_details = game[game["id"] == game_id]
                    st.write(f"{game_details['team_home'].iloc[0]} vs {game_details['team_away'].iloc[0]} - {game_details['tournament_name'].iloc[0]}")

            with st.expander("League Information of Providers (all displayed games):"):
                league_optimum = present.liga_info(optimum)
                st.table(league_optimum)

            with st.expander("Detailed Information of Providers (all possible games):"):
                optimum_games = present.full_info(optimum)
                st.table(optimum_games)
    else:
        st.warning("Please select at least one team.")