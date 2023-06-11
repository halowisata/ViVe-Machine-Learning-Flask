import pandas as pd

from models.knowledge_constraint.prediction import knowledge_main
from models.collaborative_filtering.prediction import cf_main


def recommendation_place(user_id, mood_input, budget_input, city_input):
    place = pd.read_csv("./datasets/raw/tourism_with_id_updated.csv")
    final_result = place.copy()
    result_constraints_recommender = knowledge_main(
        mood_input, budget_input, city_input)
    result_cf_recommender = cf_main()
    final_result = pd.merge(final_result, result_constraints_recommender[['Place_Id', 'score']], on='Place_Id',
                            how='left')
    final_result.rename(columns={'score': 'score_1'}, inplace=True)

    final_result = pd.merge(final_result, result_cf_recommender[[
                            'Place_Id', 'score']], on='Place_Id', how='left')
    final_result.rename(columns={'score': 'score_2'}, inplace=True)

    final_result['score_sum'] = final_result['score_1'].fillna(
        0) + final_result['score_2'].fillna(0)
    final_result.sort_values("score_sum", ascending=False, inplace=True)
    return final_result
