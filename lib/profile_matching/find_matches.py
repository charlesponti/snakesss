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
