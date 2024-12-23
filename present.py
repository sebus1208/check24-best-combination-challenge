import pandas as pd
import app

game, streaming_offer, streaming_packages = app.load_data()
streamed_games = pd.merge(game, streaming_offer, left_on="id", right_on="game_id")
all_df = pd.merge(streamed_games, streaming_packages, left_on="streaming_package_id", right_on="id")

def anbieter_info(analyse):
    df = streaming_packages[streaming_packages["id"].isin(analyse["selected_providers"])]
    df = df.drop(["id", "monthly_price_cents"], axis=1)
    df = df.rename(columns={"monthly_price_yearly_subscription_in_cents": "Monthly Price"})
    df["Monthly Price"] = df["Monthly Price"].apply(lambda x: f"{x / 100:.2f} €")
    return df.to_dict(orient="records")

def liga_info(analyse):
    df = all_df[all_df["streaming_package_id"].isin(analyse["selected_providers"])]
    ligen = df.groupby("tournament_name").apply(lambda x: {
        "Total Games": len(x),
        "Displayed Games": x["id_x"].nunique()
    }).reset_index(name="Details")
    result = pd.DataFrame({
        "League": ligen["tournament_name"],
        "Total Games": ligen["Details"].apply(lambda x: x["Total Games"]),
        "Displayed Games": ligen["Details"].apply(lambda x: x["Displayed Games"]),
        "Coverage": ligen["Details"].apply(lambda x: "All" if x["Total Games"] == x["Displayed Games"] else ("Partial" if x["Displayed Games"] > 0 else "None"))
    })
    return result

def full_info(analyse = None):
    if analyse is not None:
        df = all_df[all_df["streaming_package_id"].isin(analyse["selected_providers"])]
    else:
        df = all_df
    df = df.drop(["id_x", "id_y", "game_id", "streaming_package_id", "monthly_price_cents", "monthly_price_yearly_subscription_in_cents"], axis=1)
    return df
