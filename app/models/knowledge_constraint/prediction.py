import pandas as pd


def read_csv(file_path):
    df = pd.read_csv(file_path)
    return df


def drop_columns(df, column_names):
    # Get the columns present in the DataFrame
    existing_columns = df.columns

    # Filter the column names that exist in the DataFrame
    valid_column_names = [col for col in column_names if col in existing_columns]

    # Drop the valid column names
    df = df.drop(valid_column_names, axis=1)
    return df


# knowledge based on paper


def mood_constraint(mood):
    mood = mood.capitalize()
    preferences = []
    if mood == "Happy" or mood == "Sad":
        preferences = ["Petualangan", "Keluarga", "Romantis", "Budaya"]
    elif mood == "Calm" or mood == "Angry":
        preferences = ["Alam", "Hiburan", "Olahraga", "Relaksasi"]

    return preferences


def filter_by_budget(df, column_name, category):
    category = category.capitalize()
    quartiles = df[column_name].quantile([0.25, 0.5, 0.75])
    q1 = quartiles[0.25]
    q2 = quartiles[0.5]
    q3 = quartiles[0.75]

    if category == "Low":
        filtered_df = df[df[column_name] <= q1]
    elif category == "Medium":
        filtered_df = df[(df[column_name] > q1) & (df[column_name] <= q2)]
    elif category == "High":
        filtered_df = df[
            ((df[column_name] > q2) & (df[column_name] <= q3)) | (df[column_name] > q3)
        ]
    elif category == "Random":
        filtered_df = df
    else:
        filtered_df = []

    return filtered_df


def filter_by_city(df, city):
    city = city.capitalize()
    if city == None or city == "Random":
        filtered_df = df
    else:
        filtered_df = df[df["City"] == city]
    return filtered_df


def knowledge_recommender(df, mood, budget, city):
    recommended_destinations = []

    mood_preferences = mood_constraint(mood)

    # filter dataset based on budget
    filtered_df = filter_by_budget(df, "Price", budget)

    # filter dataset based on city
    filtered_df = filter_by_city(filtered_df, city)

    # print(filtered_df)
    recommended_destinations = filtered_df[
        filtered_df["new_category"].apply(
            lambda x: any(preference in x for preference in mood_preferences)
        )
    ]
    return recommended_destinations


def give_scoring(df):
    # this function will return score for each user recommended items
    df["score"] = 1
    return df


def knowledge_main(mood_input, budget_input, city_input):
    path = "./datasets/raw/tourism_with_id_updated.csv"
    df = read_csv(path)
    df = drop_columns(df, ["Description", "Time_Minutes", "Coordinate"])
    knowledge_recommendation = knowledge_recommender(
        df, mood_input, budget_input, city_input
    )
    knowledge_recommendation.sort_values("Rating", ascending=False, inplace=True)
    knowledge_recommendation = drop_columns(
        knowledge_recommendation,
        ["Place_Name", "City", "Price", "Lat", "Long", "new_category", "Rating"],
    )
    knowledge_recommendation = give_scoring(knowledge_recommendation)
    return knowledge_recommendation
