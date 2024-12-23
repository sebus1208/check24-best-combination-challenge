import pandas as pd
import app

game, streaming_offer, streaming_packages = app.load_data()
streamed_games = pd.merge(game, streaming_offer, left_on="id", right_on="game_id")
all_df = pd.merge(streamed_games, streaming_packages, left_on="streaming_package_id", right_on="id")


def anbieter_info(analyse):
    df = streaming_packages[streaming_packages["id"].isin(analyse["ausgewählte_anbieter"])]
    df = df.drop(["id", "monthly_price_cents"], axis=1)
    df = df.rename(columns={"monthly_price_yearly_subscription_in_cents": "Monatspreis"})
    df["Monatspreis"] = df["Monatspreis"].apply(lambda x: f"{x / 100:.2f} €")
    return df.to_dict(orient="records")

def liga_info(analyse):
    df = all_df[all_df["streaming_package_id"].isin(analyse["ausgewählte_anbieter"])]
    ligen = df.groupby("tournament_name").apply(lambda x: {
        "Anzahl Spiele": len(x),
        "Angezeigte Spiele": x["id_x"].nunique()
    }).reset_index(name="Details")
    result = pd.DataFrame({
        "Liga": ligen["tournament_name"],
        "Anzahl Spiele": ligen["Details"].apply(lambda x: x["Anzahl Spiele"]),
        "Angezeigte Spiele": ligen["Details"].apply(lambda x: x["Angezeigte Spiele"]),
        "Abdeckung": ligen["Details"].apply(lambda x: "Alle" if x["Anzahl Spiele"] == x["Angezeigte Spiele"] else ("Teilweise" if x["Angezeigte Spiele"] > 0 else "Keine"))
    })
    return result

def full_info(analyse = None):
    if analyse is not None:
        df = all_df[all_df["streaming_package_id"].isin(analyse["ausgewählte_anbieter"])]
    else:
        df = all_df
    df = df.drop(["id_x", "id_y", "game_id", "streaming_package_id", "monthly_price_cents", "monthly_price_yearly_subscription_in_cents"], axis=1)
    return df