with open('js/views.js', 'r', encoding='utf-8') as f:
    content = f.read()

target = '<span class="source-context">${q.year} ${esc(q.paper)} <span>· Question ${q.number}</span></span></div>'
replacement = '<span class="source-context">${q.year} ${esc(q.paper)} <span>· Question ${q.number}</span></span>${(q.paper===\'AE\'||q.id?.includes(\'-ae-\')) ? `<button data-action="toggle-verify-question" data-value="${esc(q.id)}" class="${a.verification?.[q.id]?.status===\'verified\'?\'primary small\':\'quiet small\'}" style="margin-left:12px; padding:2px 8px; font-size:12px; vertical-align:middle;">${a.verification?.[q.id]?.status===\'verified\'?\'✓ Verified\':\'Mark as Verified\'}</button>` : \'\'}</div>'

if target in content:
    content = content.replace(target, replacement)
    with open('js/views.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully patched quiz in views.js")
else:
    print("Target not found")
