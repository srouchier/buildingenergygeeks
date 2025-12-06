import json

notebook_path = 'rnn_implementation.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

for cell in notebook['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if "build_and_train('SimpleRNN'" in source or \
           "build_and_train('LSTM'" in source or \
           "build_and_train('GRU'" in source:
            
            if 'metadata' not in cell:
                cell['metadata'] = {}
            
            if 'tags' not in cell['metadata']:
                cell['metadata']['tags'] = []
            
            if 'remove-output' not in cell['metadata']['tags']:
                cell['metadata']['tags'].append('remove-output')
                print(f"Added remove-output tag to cell with source: {source[:30]}...")

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=4)

print("Notebook updated successfully.")
