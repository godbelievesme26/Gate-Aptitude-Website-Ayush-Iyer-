class SessionTimer {
 constructor(session,now=()=>Date.now()){this.session=session;this.now=now;this.last=null;this.visit=0;this.notified=false;this.noticeUntil=0;}
 start(){if(this.last===null)this.last=this.now();}
 flush(){if(this.last===null)return 0;const next=this.now(),delta=Math.max(0,next-this.last);this.last=next;const id=this.session.questionIds[this.session.currentPosition];this.session.elapsed+=delta;this.session.times[id]=(this.session.times[id]||0)+delta;this.visit+=delta;return delta;}
 stop(){this.flush();this.last=null;this.visit=0;this.notified=false;this.noticeUntil=0;}
 pause(){this.flush();this.last=null;}
 leave(){this.flush();this.visit=0;this.notified=false;this.noticeUntil=0;}
 checkpoint(){if(this.visit>=120000&&!this.notified){this.notified=true;this.noticeUntil=this.now()+10000;return true;}return false;}
 checkpointVisible(){return this.notified&&this.now()<=this.noticeUntil;}
 remaining(){return null;}
 expired(){return false;}
}

export class PracticeTimer extends SessionTimer {}

export class CountdownTimer extends SessionTimer {
 remaining(){return Math.max(0,(this.session.deadline??this.now())-this.now());}
 expired(){return this.remaining()===0;}
}

export const createSessionTimer=(session,now=()=>Date.now())=>session.mode==='test'?new CountdownTimer(session,now):new PracticeTimer(session,now);
export const QuizTimer=PracticeTimer;
export function clock(ms){const secs=Math.floor(Math.max(0,ms||0)/1000);return `${String(Math.floor(secs/60)).padStart(2,'0')}:${String(secs%60).padStart(2,'0')}`;}
