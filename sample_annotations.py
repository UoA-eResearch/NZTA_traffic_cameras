#!/usr/bin/env python3

import os
import random
import json
from tqdm.auto import tqdm

random.seed(9001)

camIds = sorted(os.listdir("annotations"))

results = {}

for camId in tqdm(camIds):
    annotations = os.listdir(f"annotations/{camId}")
    unique_days = set()
    results[camId] = {}
    for a in annotations:
        unique_days.add(a[:10])
    for d in sorted(unique_days):
        annotations_for_day = [a for a in annotations if a.startswith(d)]
        if len(annotations_for_day) > 2:
            annotations_for_day = random.sample(annotations_for_day, 2)
        for annotation_path in annotations_for_day:
            with open(f"annotations/{camId}/{annotation_path}") as f:
                a = json.load(f)
                for e in a:
                    e["percentage_probability"] = round(e["percentage_probability"],2)
            results[camId][annotation_path] = a
print(json.dumps(results))
