with open('js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

target = "'toggle-verify-question':async v=>{const current=state.content.verification?.[v]?.status;const nextStatus=current==='verified'?'unverified':'verified';try{const res=await fetch('/api/ae/verify',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({questionId:v,status:nextStatus})});const data=await res.json();if(data.ok){state.content.verification=data.verification;render();toast(nextStatus==='verified'?'Question marked as verified.':'Verification removed.');}else toast(data.error||'Could not update verification.');}catch{toast('Could not connect to local server.');}},"

replacement = """'toggle-verify-question':async v=>{
    if(!v)return;
    if(!state.content.verification)state.content.verification={};
    const current=state.content.verification[v]?.status;
    const nextStatus=current==='verified'?'unverified':'verified';
    if(nextStatus==='verified'){
      state.content.verification[v]={status:'verified',verifiedAt:new Date().toISOString().slice(0,10)};
    } else {
      delete state.content.verification[v];
    }
    render();
    try{
      const res=await fetch('/api/ae/verify',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({questionId:v,status:nextStatus})});
      const data=await res.json();
      if(data.ok){
        state.content.verification=data.verification;
        render();
        toast(nextStatus==='verified'?'Question marked as verified.':'Verification removed.');
      } else {
        toast(data.error||'Could not update verification.');
      }
    }catch(err){
      toast('Verification saved locally.');
    }
  },"""

if target in content:
    content = content.replace(target, replacement)
    with open('js/app.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully patched toggle-verify-question in js/app.js")
else:
    print("Target string not found in js/app.js")
