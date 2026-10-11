import re

content = open('C:/Users/godbe/.gemini/antigravity/brain/c05ba5de-1c22-4609-a6ec-bfdf2114d4f1/.system_generated/steps/2633/content.md', encoding='utf8').read()
links = re.findall(r'href=["\']([^"\']+)["\']', content)
for l in sorted(set(links)):
    print(l)
