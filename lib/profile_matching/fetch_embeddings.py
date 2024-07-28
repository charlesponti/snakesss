import json

import pandas as pd
import time
import tqdm

from lib.clients.openai import get_open_api_embedding


"""
================= Read Profile data ===========================
"""


df = pd.read_csv("profiles.csv")

# Filter out non-null values
df = df[df["description"].notnull()]


"""
================= Get Embeddings ===========================
"""

embeddings = {}

for i, row in tqdm.tqdm(df.iterrows(), total=df.shape[0]):

    embeddings[row["id"]] = {
        "description": row["description"],
        "embedding": get_open_api_embedding(row["description"]),
    }

    time.sleep(0.1)  ## Avoid Azure rate limiting


"""
================= Save output ===========================
"""

## Store the output so we don't need to keep calling the Open AI api every time

f = open("embeddings.json", "w")

f.write(json.dumps(embeddings))

f.close()

print("Successfully fetched {} embeddings".format(df.shape[0]))
