import re

with open('js/views.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update renderExamMode to include isAe and isVerified, and verify button in .cbt-question-header
old_cbt_header = '''        <div class="cbt-question-header">
          <div class="cbt-qtype">Question Type: ${q.type}</div>
          <div class="cbt-marks">Marks for correct answer: <span class="green">${q.marks}</span> | Negative Marks: <span class="red">${formattedPenalty}</span></div>
        </div>'''

new_cbt_header = '''        <div class="cbt-question-header">
          <div class="cbt-qtype" style="display:flex; align-items:center; gap:12px;">
            <span>Question Type: ${q.type}</span>
            ${isAe ? `<button data-action="toggle-verify-question" data-value="${esc(q.id)}" class="${isVerified ? 'primary small' : 'quiet small'}" style="padding: 2px 10px; font-size: 12px; cursor: pointer; border-radius: 3px; font-weight: 600; ${isVerified ? 'background: #2b669a; color: #fff; border: 1px solid #2b669a;' : 'background: #fff; color: #333; border: 1px solid #999;'}">${isVerified ? '✓ Verified' : 'Mark as Verified'}</button>` : ''}
          </div>
          <div class="cbt-marks">Marks for correct answer: <span class="green">${q.marks}</span> | Negative Marks: <span class="red">${formattedPenalty}</span></div>
        </div>'''

if old_cbt_header in content:
    content = content.replace(old_cbt_header, new_cbt_header)
    print("Patched cbt-question-header")
else:
    print("Warning: old_cbt_header not found directly, checking normalized...")
    content = content.replace(old_cbt_header.replace('\r\n', '\n'), new_cbt_header.replace('\r\n', '\n'))

# Ensure isAe and isVerified are defined in renderExamMode
old_render_vars = '''  const visibleIds = sectionId === 'GA' ? gaIds : aeIds;
  const isTest = true;'''

new_render_vars = '''  const visibleIds = sectionId === 'GA' ? gaIds : aeIds;
  const isTest = true;
  const isAe = q.paper === 'AE' || q.id?.includes('-ae-');
  const isVerified = a.verification?.[q.id]?.status === 'verified';'''

if old_render_vars in content:
    content = content.replace(old_render_vars, new_render_vars)
    print("Patched renderExamMode variables")
else:
    content = content.replace(old_render_vars.replace('\r\n', '\n'), new_render_vars.replace('\r\n', '\n'))
    print("Patched renderExamMode variables (LF)")

# 2. Update aerospace(s, a, id) to include question list in paper overview
old_paper_view = '''    <div class="actions" style="margin-top:20px;">
      ${button('Start PYQ','start-paper',paper.id,'primary')}
      ${button('Timed Test','time-paper',paper.id)}
    </div>
  </section></div>`;'''

new_paper_view = '''    <div class="actions" style="margin-top:20px;">
      ${button('Start PYQ','start-paper',paper.id,'primary')}
      ${button('Timed Test','time-paper',paper.id)}
    </div>
  </section>
  <section class="panel">
    <h2>Questions & Verification Status</h2>
    <p class="caption">Direct access to all ${paper.totalQuestions} questions. Open any question to review and verify.</p>
    <div style="max-height: 380px; overflow-y: auto; padding-right: 4px; display: flex; flex-direction: column; gap: 4px; margin-top: 12px;">
      ${paper.questionOrder.map(qId => {
        const item = a.byId.get(qId);
        if (!item) return '';
        const isV = a.verification?.[qId]?.status === 'verified';
        return `<div class="row" style="padding: 6px 0; border-bottom: 1px solid var(--border, #eee);">
          <span><strong>Q${item.number}</strong> · ${esc(item.section || 'AE')} · ${esc(item.type)} · ${item.marks}M</span>
          <span style="display:flex; align-items:center; gap:8px;">
            <span class="pill" style="${isV ? 'background: #2b669a; color: white;' : ''}">${isV ? '✓ Verified' : 'Unverified'}</span>
            ${link('Open', '#/question/' + item.id, 'button quiet small')}
          </span>
        </div>`;
      }).join('')}
    </div>
  </section></div>`;'''

if old_paper_view in content:
    content = content.replace(old_paper_view, new_paper_view)
    print("Patched aerospace paper view")
else:
    content = content.replace(old_paper_view.replace('\r\n', '\n'), new_paper_view.replace('\r\n', '\n'))
    print("Patched aerospace paper view (LF)")

with open('js/views.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved js/views.js")
