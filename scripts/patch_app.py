from pathlib import Path

path = Path('c:/Users/godbe/Desktop/Aptitude Website/js/app.js')
content = path.read_text(encoding='utf-8')

old_part = " bookmark:openBookmark,'quick-bookmark':v=>{"
new_part = """ 'toggle-verify-question':async v=>{const current=state.content.verification?.[v]?.status;const nextStatus=current==='verified'?'unverified':'verified';try{const res=await fetch('/api/ae/verify',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({questionId:v,status:nextStatus})});const data=await res.json();if(data.ok){state.content.verification=data.verification;render();toast(nextStatus==='verified'?'Question marked as verified.':'Verification removed.');}else toast(data.error||'Could not update verification.');}catch{toast('Could not connect to local server.');}},
 bookmark:openBookmark,'quick-bookmark':v=>{"""

assert old_part in content, "old_part not found"
updated = content.replace(old_part, new_part, 1)
path.write_text(updated, encoding='utf-8')
print("Successfully patched js/app.js with toggle-verify-question!")
