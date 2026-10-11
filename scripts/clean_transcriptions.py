import re
import json

with open('scripts/ae2025-transcriptions.json', 'r', encoding='utf8') as f:
    text = f.read()

# Replace any backslash that is not followed by " or \ with \\
# First escape all backslashes that might be standalone
# Better yet: replace known LaTeX patterns before json parsing
text = text.replace('\\matrix', 'MATRIX_TOKEN')
text = text.replace('\\frac', 'FRAC_TOKEN')
text = text.replace('\\overline', 'OVERLINE_TOKEN')

# Remove rogue backslashes
text = re.sub(r'\\([^\x00-\x7F])', r'\1', text)
text = re.sub(r'\\([a-zA-Z])', r'\1', text)
text = re.sub(r'\\(?![\\"])', r'', text)

# Restore tokens
text = text.replace('MATRIX_TOKEN', r'\\matrix')
text = text.replace('FRAC_TOKEN', r'\\frac')
text = text.replace('OVERLINE_TOKEN', r'\\overline')

data = json.loads(text, strict=False)

with open('scripts/ae2025-transcriptions.json', 'w', encoding='utf8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write('\n')

print('Successfully cleaned ae2025-transcriptions.json!')
