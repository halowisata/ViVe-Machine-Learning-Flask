
```
Flask_Implementation
├─ app
│  ├─ app.py
│  ├─ config.py
│  ├─ models
│  │  ├─ collaborative_filtering
│  │  │  ├─ prediction.py
│  │  │  └─ training.py
│  │  ├─ knowledge_constraint
│  │  │  └─ prediction.py
│  │  ├─ preprocessing
│  │  │  └─ preprocessing.py
│  │  └─ __init__.py
│  ├─ routes
│  │  ├─ api.py
│  │  └─ __init__.py
│  ├─ utils.py
│  └─ __init__.py
├─ datasets
│  ├─ output
│  │  ├─ output.txt
│  │  ├─ places.txt
│  │  └─ recommender_output
│  │     ├─ cf_recommendation.csv
│  │     └─ knowledge_recommendation.csv
│  ├─ processed
│  │  └─ tourism_with_id_updated.csv
│  └─ raw
│     ├─ tourism_rating.csv
│     ├─ tourism_with_id.csv
│     └─ user.csv
├─ notebooks
│  ├─ preprocessing
│  │  └─ preprocessing.ipynb
│  └─ recommender
│     ├─ Collaborative Filtering with Predictions.ipynb
│     ├─ hybridization.ipynb
│     ├─ knowledge_constraint.ipynb
│     └─ test.ipynb
├─ README.md
├─ requirements.txt
└─ run.py

```