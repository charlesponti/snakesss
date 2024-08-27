import pandas as pd
import logging
from lib.clients.openai import get_openai_embedding
from dataclasses import dataclass
from numpy import matrix
import tqdm
import json
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class Profile:
    id: str
    description: str
    embedding: matrix


def get_profile_matches():
    users: dict[str, Profile] = json.load(open("embeddings.json"))

    ids = list(users.keys())

    matches = []

    for i in tqdm.tqdm(range(len(ids))):
        id = ids[i]

        to_compare = ids[i + 1 :]

        for j in range(len(to_compare)):
            user_1 = users[id]
            user_2 = users[to_compare[j]]

            similarity = cosine_similarity(user_1.embedding, user_2.embedding)[0][0]

            matches.append(
                {
                    "user_1": id,
                    "user_2": to_compare[j],
                    "profile_1": user_1.description,
                    "profile_2": user_2.description,
                    "score": similarity,
                }
            )

    matches = sorted(matches, key=lambda x: x["score"], reverse=True)

    return matches


async def get_profile_data() -> pd.DataFrame:
    logging.info("Reading profile data", extra={"step": "retrieve profile data"})
    df = pd.read_csv("./.data/profiles.csv")

    # Filter out non-null values
    df = df[df["description"].notnull()]

    return df

async def get_embeddings(df: pd.DataFrame) -> dict:
    logging.info("Fetching embeddings", extra={"step": "fetch_embeddings"})
    embeddings = {}

    for i, row in df.iterrows():
        embeddings[row["id"]] = {
            "description": row["description"],
            "embedding": get_openai_embedding(row["description"]),
        }

    return embeddings
