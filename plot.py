from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


ATOL = 0.2
RTOL = 0.2

output_path = Path('output')
plot_path = Path('plot')

tools = {
    'amici': 'AMICI',
    'pypesto': 'pyPESTO',
}

vectors = {
    'default': 'PEtab nominal',
    'midpoint': 'Midpoint of scaled bounds',
}

data = {(vector_id, tool_id): {} for vector_id in vectors for tool_id in tools}
for full_model_path in output_path.glob('*'):
    model_name = full_model_path.stem
    for tool_id, tool_name in tools.items():
        for vector_id, vector_name in vectors.items():
            data_tsv = output_path / model_name / tool_id / 'result' / (vector_id + '.tsv')
            try:
                df = pd.read_csv(str(data_tsv), sep='\t')
                result = int((np.array(df.abs_err < ATOL) | np.array(df.rel_err < RTOL)).all())
            except FileNotFoundError:
                result = -1
            data[(vector_id, tool_id)][model_name] = result

sorted_data = {}
for vector_tool in sorted(data):
    sorted_data[vector_tool] = {model_name: data[vector_tool][model_name] for model_name in sorted(data[vector_tool])}

df = pd.DataFrame(data=sorted_data)
fig, ax = plt.subplots(figsize=(10, 15))
sns.heatmap(df, ax=ax)
plt.tight_layout()
plt.savefig(str(plot_path / 'result.png'))
