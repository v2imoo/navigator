// NAVIGATOR — interactive tools (client-side only, no login, results downloadable/shareable)
(function(){
/* ---------- shared: download a canvas as PNG ---------- */
function downloadCanvas(canvas,name){var a=document.createElement('a');a.download=name+'.png';a.href=canvas.toDataURL('image/png');a.click();}
function downloadText(text,name,type){var b=new Blob([text],{type:type||'text/plain'});var a=document.createElement('a');a.download=name;a.href=URL.createObjectURL(b);a.click();}
function esc(s){return (s||'').replace(/[<>&]/g,function(c){return{'<':'&lt;','>':'&gt;','&':'&amp;'}[c];});}

/* =========================================================
   DECISION MATRIX  (weighted scoring)
   ========================================================= */
window.initDecisionMatrix=function(root){
  var el=document.getElementById(root); if(!el) return;
  var state={criteria:[{name:'Impact',weight:3},{name:'Cost (lower better? no — score high=good)',weight:2},{name:'Speed',weight:2}],
             options:['Option A','Option B'], scores:{}};
  function key(o,c){return o+'::'+c;}
  function render(){
    var h='<div style="overflow-x:auto"><table><thead><tr><th>Option \\\\ Criterion</th>';
    state.criteria.forEach(function(c,ci){h+='<th>'+esc(c.name)+'<br><span class="mono" style="font-weight:400;font-size:.8em">weight '+c.weight+'</span></th>';});
    h+='<th>Score</th></tr></thead><tbody>';
    var results=[];
    state.options.forEach(function(o,oi){
      var total=0,wsum=0;
      h+='<tr><td><strong>'+esc(o)+'</strong></td>';
      state.criteria.forEach(function(c,ci){
        var v=state.scores[key(o,c.name)]; if(v===undefined)v=5;
        total+=v*c.weight; wsum+=c.weight;
        h+='<td><input type="number" min="0" max="10" value="'+v+'" data-o="'+oi+'" data-c="'+ci+'" style="width:64px"></td>';
      });
      var score=wsum?(total/wsum):0; results.push({o:o,score:score});
      h+='<td><strong>'+score.toFixed(2)+'</strong></td></tr>';
    });
    h+='</tbody></table></div>';
    results.sort(function(a,b){return b.score-a.score;});
    h+='<div class="result"><strong>Ranking:</strong><ol>';
    results.forEach(function(r){h+='<li>'+esc(r.o)+' — <strong>'+r.score.toFixed(2)+'</strong>/10</li>';});
    h+='</ol><p class="mono" style="font-size:.8rem;margin:.4em 0 0">Winner: '+esc(results[0].o)+'. Scores are 0–10 per criterion, weighted and normalised.</p></div>';
    el.querySelector('.dm-table').innerHTML=h;
    el.querySelectorAll('.dm-table input[type=number]').forEach(function(inp){
      inp.addEventListener('input',function(){
        var o=state.options[+inp.dataset.o], c=state.criteria[+inp.dataset.c];
        state.scores[key(o,c.name)]=Math.max(0,Math.min(10,+inp.value||0)); render();
      });
    });
    window._dmResults=results;
  }
  el.innerHTML=
    '<div class="tool-box">'+
    '<div class="grid c2">'+
      '<div><label>Options (one per line)</label><textarea class="dm-options" rows="4">'+state.options.join('\n')+'</textarea></div>'+
      '<div><label>Criteria — name : weight (one per line)</label><textarea class="dm-criteria" rows="4">'+state.criteria.map(function(c){return c.name+' : '+c.weight;}).join('\n')+'</textarea></div>'+
    '</div>'+
    '<button class="btn dm-build" style="margin-top:10px">Build / update matrix</button>'+
    '<div class="dm-table" style="margin-top:16px"></div>'+
    '<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:14px">'+
      '<button class="btn tools dm-png">⬇ Download result (PNG)</button>'+
      '<button class="btn ghost dm-csv">⬇ Download data (CSV)</button>'+
      '<button class="btn ghost" onclick="navShare()">↗ Share link</button>'+
    '</div></div>';
  function rebuild(){
    var opts=el.querySelector('.dm-options').value.split('\n').map(function(s){return s.trim();}).filter(Boolean);
    var crit=el.querySelector('.dm-criteria').value.split('\n').map(function(s){return s.trim();}).filter(Boolean).map(function(line){
      var p=line.split(':'); return {name:(p[0]||'Criterion').trim(), weight:Math.max(1,+((p[1]||'1').trim())||1)};
    });
    if(opts.length)state.options=opts; if(crit.length)state.criteria=crit; state.scores={}; render();
  }
  el.querySelector('.dm-build').addEventListener('click',rebuild);
  el.querySelector('.dm-png').addEventListener('click',function(){
    var r=window._dmResults||[]; var W=680,H=120+r.length*54;
    var cv=document.createElement('canvas');cv.width=W;cv.height=H;var x=cv.getContext('2d');
    x.fillStyle='#FBF7F0';x.fillRect(0,0,W,H);
    x.fillStyle='#1B1B2F';x.font='700 26px Georgia';x.fillText('Decision Matrix — ranking',24,44);
    x.font='13px monospace';x.fillStyle='#43435e';x.fillText('made with Navigator',24,66);
    var max=r.length?r[0].score:10;
    r.forEach(function(it,i){var y=100+i*54;
      x.fillStyle='#1B1B2F';x.font='600 17px Georgia';x.fillText((i+1)+'. '+it.o,24,y);
      x.fillStyle='#e6ddcd';x.fillRect(24,y+8,W-140,14);
      var w=(W-140)*(it.score/10);
      var g=x.createLinearGradient(24,0,24+w,0);g.addColorStop(0,'#4B4FCE');g.addColorStop(1,'#0E9594');
      x.fillStyle=g;x.fillRect(24,y+8,w,14);
      x.fillStyle='#1B1B2F';x.font='700 15px monospace';x.fillText(it.score.toFixed(2),W-96,y+20);
    });
    downloadCanvas(cv,'decision-matrix');
  });
  el.querySelector('.dm-csv').addEventListener('click',function(){
    var rows=['option,'+state.criteria.map(function(c){return '"'+c.name+' (w'+c.weight+')"';}).join(',')+',weighted_score'];
    (window._dmResults||[]).forEach(function(){});
    state.options.forEach(function(o){
      var vals=state.criteria.map(function(c){var v=state.scores[o+'::'+c.name];return v===undefined?5:v;});
      var total=0,ws=0;state.criteria.forEach(function(c,i){total+=vals[i]*c.weight;ws+=c.weight;});
      rows.push('"'+o+'",'+vals.join(',')+','+(ws?(total/ws).toFixed(3):0));
    });
    downloadText(rows.join('\n'),'decision-matrix.csv','text/csv');
  });
  render();
};

/* =========================================================
   MOAT ANALYZER  (7 Powers scoring -> profile + PNG)
   ========================================================= */
window.initMoatAnalyzer=function(root){
  var el=document.getElementById(root); if(!el) return;
  var powers=[
    ['Scale Economies','Per-unit cost falls as you grow; rivals can\'t match your cost without your share.'],
    ['Network Economies','Each user makes the product more valuable to other users.'],
    ['Counter-Positioning','You have a model incumbents won\'t copy (it would damage their business).'],
    ['Switching Costs','Customers would lose value moving to a rival for the next purchase.'],
    ['Branding','Customers pay more for an identical offering because of who you are.'],
    ['Cornered Resource','Preferential access to a coveted asset (patent, person, deal, deposit).'],
    ['Process Power','Routines that deliver lower cost/better product, copyable only over years.']
  ];
  var vals=powers.map(function(){return 0;});
  var html='<div class="tool-box"><p class="mono" style="font-size:.85rem;color:var(--ink-soft)">Rate your business 0–4 on each Power. 0 = none, 4 = strong & durable.</p>';
  powers.forEach(function(p,i){
    html+='<div class="trow"><label>'+p[0]+' <span style="font-weight:400;color:var(--ink-soft)">— '+p[1]+'</span></label>'+
      '<input type="range" min="0" max="4" value="0" data-i="'+i+'"><span class="ma-v mono" data-v="'+i+'">0</span></div>';
  });
  html+='<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:12px">'+
    '<button class="btn tools ma-png">⬇ Download profile (PNG)</button>'+
    '<button class="btn ghost" onclick="navShare()">↗ Share link</button></div>'+
    '<div class="ma-out result" style="margin-top:14px"></div></div>';
  el.innerHTML=html;
  function out(){
    var total=vals.reduce(function(a,b){return a+b;},0), max=powers.length*4;
    var strong=powers.filter(function(p,i){return vals[i]>=3;}).map(function(p){return p[0];});
    var none=powers.filter(function(p,i){return vals[i]===0;}).map(function(p){return p[0];});
    var verdict= total>=18?'Wide moat — multiple durable Powers.':total>=10?'Some moat — real but concentrated; widen it.':total>=4?'Thin moat — one weak lever; fragile to competition.':'No moat yet — you have a product, not a defended business.';
    var h='<strong>Moat score: '+total+' / '+max+'</strong><div class="bar" style="width:'+(100*total/max)+'%;margin:8px 0"></div>';
    h+='<p>'+verdict+'</p>';
    if(strong.length)h+='<p><strong>Your Powers:</strong> '+strong.map(function(s){return '<span class="pill">'+s+'</span>';}).join(' ')+'</p>';
    if(none.length)h+='<p class="mono" style="font-size:.8rem">Absent: '+none.join(', ')+'</p>';
    el.querySelector('.ma-out').innerHTML=h;
  }
  el.querySelectorAll('input[type=range]').forEach(function(r){
    r.addEventListener('input',function(){vals[+r.dataset.i]=+r.value;el.querySelector('[data-v="'+r.dataset.i+'"]').textContent=r.value;out();});
  });
  el.querySelector('.ma-png').addEventListener('click',function(){
    var W=560,H=560,cx=W/2,cy=300,R=190,cv=document.createElement('canvas');cv.width=W;cv.height=H;var x=cv.getContext('2d');
    x.fillStyle='#FBF7F0';x.fillRect(0,0,W,H);
    x.fillStyle='#1B1B2F';x.font='700 26px Georgia';x.fillText('Moat Profile — 7 Powers',24,42);
    x.font='13px monospace';x.fillStyle='#43435e';x.fillText('made with Navigator',24,62);
    var n=powers.length;
    function pt(i,r){var a=-Math.PI/2+i*2*Math.PI/n;return [cx+r*Math.cos(a),cy+r*Math.sin(a)];}
    for(var ring=1;ring<=4;ring++){x.strokeStyle='#e6ddcd';x.beginPath();for(var i=0;i<=n;i++){var p=pt(i%n,R*ring/4);i===0?x.moveTo(p[0],p[1]):x.lineTo(p[0],p[1]);}x.stroke();}
    x.fillStyle='rgba(75,79,206,.28)';x.strokeStyle='#4B4FCE';x.lineWidth=2;x.beginPath();
    for(var i=0;i<=n;i++){var v=vals[i%n];var p=pt(i%n,R*v/4);i===0?x.moveTo(p[0],p[1]):x.lineTo(p[0],p[1]);}x.closePath();x.fill();x.stroke();
    x.fillStyle='#1B1B2F';x.font='600 12px sans-serif';x.textAlign='center';
    for(var i=0;i<n;i++){var p=pt(i,R+26);x.fillText(powers[i][0].split(' ')[0],p[0],p[1]);}
    x.textAlign='left';downloadCanvas(cv,'moat-profile');
  });
  out();
};
})();

/* ===== Eisenhower Matrix ===== */
window.initEisenhower=function(root){
  var el=document.getElementById(root); if(!el) return;
  el.innerHTML='<div class="tool-box"><label>Your tasks (one per line)</label>'
   +'<textarea id="ei-in" rows="5" placeholder="Reply to investor email\nFix production bug\nPlan Q3 offsite\nScroll social feeds"></textarea>'
   +'<button class="btn ei-go" style="margin-top:10px">Sort tasks</button>'
   +'<div id="ei-out" style="margin-top:14px"></div>'
   +'<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:12px"><button class="btn tools ei-png">\u2b07 Download (PNG)</button><button class="btn ghost" onclick="navShare()">\u2197 Share</button></div></div>';
  var quads=[["Do now","Urgent + Important","#F0544F"],["Schedule","Important, not urgent","#2FBF71"],["Delegate","Urgent, not important","#FFC93C"],["Eliminate","Neither","#9B5DE5"]];
  var data=[[],[],[],[]];
  function render(){
    var tasks=document.getElementById('ei-in').value.split('\n').map(function(s){return s.trim();}).filter(Boolean);
    data=[[],[],[],[]];
    var h='<p class="count-note">Tap each task to set urgency &amp; importance.</p><div id="ei-list">';
    tasks.forEach(function(t,i){
      h+='<div style="display:flex;gap:8px;align-items:center;margin:6px 0;flex-wrap:wrap"><span style="flex:1;min-width:160px">'+t.replace(/</g,'&lt;')+'</span>'
        +'<label style="display:inline;font-weight:600"><input type="checkbox" data-t="'+i+'" class="ei-u"> urgent</label>'
        +'<label style="display:inline;font-weight:600"><input type="checkbox" data-t="'+i+'" class="ei-i"> important</label></div>';
    });
    h+='</div><div class="grid c2" id="ei-grid" style="margin-top:14px"></div>';
    document.getElementById('ei-out').innerHTML=h;
    el.querySelectorAll('.ei-u,.ei-i').forEach(function(cb){cb.addEventListener('change',classify);});
    window._eiTasks=tasks; classify();
  }
  function classify(){
    var tasks=window._eiTasks||[]; data=[[],[],[],[]];
    tasks.forEach(function(t,i){
      var u=el.querySelector('.ei-u[data-t="'+i+'"]').checked, im=el.querySelector('.ei-i[data-t="'+i+'"]').checked;
      var q = (u&&im)?0:(im&&!u)?1:(u&&!im)?2:3; data[q].push(t);
    });
    var g='';
    quads.forEach(function(q,i){
      g+='<div class="card" style="border-color:'+q[2]+'"><span class="chip" style="background:'+q[2]+'">'+q[0]+'</span>'
        +'<p class="count-note">'+q[1]+'</p><ul style="margin:.3em 0 0">'+(data[i].map(function(t){return '<li>'+t.replace(/</g,'&lt;')+'</li>';}).join('')||'<li class="count-note">&mdash;</li>')+'</ul></div>';
    });
    document.getElementById('ei-grid').innerHTML=g;
  }
  el.querySelector('.ei-go').addEventListener('click',render);
  el.querySelector('.ei-png').addEventListener('click',function(){
    var W=680,H=520,cv=document.createElement('canvas');cv.width=W;cv.height=H;var x=cv.getContext('2d');
    x.fillStyle='#FFFDF6';x.fillRect(0,0,W,H);x.fillStyle='#2A2140';x.font='700 24px Georgia';x.fillText('Eisenhower Matrix',22,38);
    x.font='12px monospace';x.fillStyle='#6a5f82';x.fillText('made with Navigator',22,58);
    var cols=[[40,80,'#F0544F','Do now'],[360,80,'#2FBF71','Schedule'],[40,300,'#FFC93C','Delegate'],[360,300,'#9B5DE5','Eliminate']];
    cols.forEach(function(c,i){x.fillStyle=c[2];x.fillRect(c[0],c[1],280,26);x.fillStyle='#fff';x.font='700 14px sans-serif';x.fillText(c[3],c[0]+10,c[1]+18);
      x.fillStyle='#2A2140';x.font='13px sans-serif';(data[i]||[]).slice(0,9).forEach(function(t,j){x.fillText('\u2022 '+t.slice(0,34),c[0]+8,c[1]+48+j*20);});});
    var a=document.createElement('a');a.download='eisenhower-matrix.png';a.href=cv.toDataURL();a.click();
  });
  render();
};

/* ===== Impact-Effort ===== */
window.initImpactEffort=function(root){
  var el=document.getElementById(root); if(!el) return;
  el.innerHTML='<div class="tool-box"><label>Tasks / ideas (one per line)</label>'
   +'<textarea id="ie-in" rows="4" placeholder="Launch referral program\nRewrite onboarding\nAttend conference"></textarea>'
   +'<button class="btn ie-go" style="margin-top:10px">Add & rate</button><div id="ie-rows" style="margin-top:12px"></div>'
   +'<div id="ie-plot"></div><div style="margin-top:12px"><button class="btn tools ie-png">\u2b07 Download (PNG)</button></div></div>';
  var items=[];
  function build(){
    items=document.getElementById('ie-in').value.split('\n').map(function(s){return s.trim();}).filter(Boolean).map(function(n){return {n:n,imp:5,eff:5};});
    var h='';
    items.forEach(function(it,i){h+='<div style="margin:8px 0"><strong>'+it.n.replace(/</g,'&lt;')+'</strong>'
      +'<div class="trow"><label>Impact <span class="mono" id="iv'+i+'">5</span></label><input type="range" min="1" max="10" value="5" data-k="imp" data-i="'+i+'">'
      +'<label>Effort <span class="mono" id="ev'+i+'">5</span></label><input type="range" min="1" max="10" value="5" data-k="eff" data-i="'+i+'"></div></div>';});
    document.getElementById('ie-rows').innerHTML=h;
    el.querySelectorAll('#ie-rows input').forEach(function(r){r.addEventListener('input',function(){
      items[+r.dataset.i][r.dataset.k]=+r.value;
      el.querySelector('#'+(r.dataset.k==='imp'?'iv':'ev')+r.dataset.i).textContent=r.value; plot();});});
    plot();
  }
  function plot(){
    var S=320,pad=30,g='<svg viewBox="0 0 '+S+' '+S+'" style="max-width:360px;margin-top:8px;background:#fff;border:2px solid var(--line);border-radius:14px">';
    g+='<line x1="'+pad+'" y1="'+(S/2)+'" x2="'+(S-6)+'" y2="'+(S/2)+'" stroke="#e6ddcd"/><line x1="'+(S/2)+'" y1="6" x2="'+(S/2)+'" y2="'+(S-pad)+'" stroke="#e6ddcd"/>';
    g+='<text x="'+(S-4)+'" y="'+(S/2-6)+'" font-size="9" text-anchor="end" fill="#6a5f82">effort \u2192</text><text x="'+(S/2+4)+'" y="12" font-size="9" fill="#6a5f82">\u2191 impact</text>';
    g+='<text x="'+pad+'" y="16" font-size="10" font-weight="700" fill="#2FBF71">quick wins</text>';
    items.forEach(function(it){var cx=pad+(it.eff/10)*(S-pad-10),cy=(S-pad)-(it.imp/10)*(S-pad-10);
      var qw=(it.imp>=6&&it.eff<=5);g+='<circle cx="'+cx+'" cy="'+cy+'" r="7" fill="'+(qw?'#2FBF71':'#6C4CE0')+'" opacity=".85"/>'
      +'<text x="'+(cx+9)+'" y="'+(cy+3)+'" font-size="9" fill="#2A2140">'+it.n.slice(0,16).replace(/</g,'')+'</text>';});
    g+='</svg>';document.getElementById('ie-plot').innerHTML=g;
  }
  el.querySelector('.ie-go').addEventListener('click',build);
  el.querySelector('.ie-png').addEventListener('click',function(){
    var svg=el.querySelector('svg');if(!svg)return;var xml=new XMLSerializer().serializeToString(svg);
    var img=new Image();img.onload=function(){var cv=document.createElement('canvas');cv.width=360;cv.height=360;var c=cv.getContext('2d');c.fillStyle='#fff';c.fillRect(0,0,360,360);c.drawImage(img,0,0,360,360);var a=document.createElement('a');a.download='impact-effort.png';a.href=cv.toDataURL();a.click();};
    img.src='data:image/svg+xml;base64,'+btoa(unescape(encodeURIComponent(xml)));
  });
  build();
};

/* ===== Pricing-Model Chooser ===== */
window.initPricingChooser=function(root){
  var el=document.getElementById(root); if(!el) return;
  var qs=[["How does a customer get value?",["The same amount every month","More the more they use it","Only when a specific outcome happens"]],
    ["Who buys it?",["A whole team/seats","A developer or via API","An executive buying a result"]],
    ["How predictable is usage?",["Very steady","Spiky / variable","Tied to business results"]]];
  var sel=[null,null,null];
  var h='<div class="tool-box">';
  qs.forEach(function(q,i){h+='<label>'+q[0]+'</label><div class="chips">'+q[1].map(function(o,j){return '<button class="chipbtn" data-q="'+i+'" data-o="'+j+'">'+o+'</button>';}).join('')+'</div>';});
  h+='<div class=" pc-out result" style="margin-top:14px">Answer the questions to see a recommendation.</div></div>';
  el.innerHTML=h;
  el.querySelectorAll('.chipbtn').forEach(function(b){b.addEventListener('click',function(){
    var q=+b.dataset.q;sel[q]=+b.dataset.o;
    el.querySelectorAll('.chipbtn[data-q="'+q+'"]').forEach(function(x){x.classList.toggle('active',x===b);});rec();});});
  function rec(){
    if(sel.indexOf(null)>=0)return;
    var score=[0,0,0]; sel.forEach(function(s){score[s]++;});
    var models=[["Per-seat / subscription","Charge per user per month. Best when value scales with team size and usage is steady. Predictable revenue, easy to buy.","#4361EE"],
      ["Usage-based / metered","Charge for what's consumed (API calls, tokens, GB). Best for developer/API products and spiky usage. Aligns cost to value; forecast carefully.","#F0544F"],
      ["Outcome / performance-based","Charge when the customer's result lands. Best when you can measure the outcome and an exec buys it. Highest alignment, hardest to meter.","#2FBF71"]];
    var win=score.indexOf(Math.max.apply(null,score)); var m=models[win];
    var out='<strong>Recommended: <span style="color:'+m[2]+'">'+m[0]+'</span></strong><p>'+m[1]+'</p>';
    if(score[win]<2)out+='<p class="count-note">Your answers are mixed &mdash; consider a hybrid (e.g. a platform fee + usage). Compare on the <a href="/business-models/">Business Models</a> page.</p>';
    el.querySelector('.pc-out').innerHTML=out;
  }
};

/* ===== SWOT Builder ===== */
window.initSWOT=function(root){
  var el=document.getElementById(root); if(!el) return;
  var q=[["Strengths","#2FBF71","Internal, helpful"],["Weaknesses","#F0544F","Internal, harmful"],["Opportunities","#4361EE","External, helpful"],["Threats","#9B5DE5","External, harmful"]];
  el.innerHTML='<div class="tool-box"><div class="grid c2">'+q.map(function(c,i){
    return '<div class="card" style="border-color:'+c[1]+'"><span class="chip" style="background:'+c[1]+'">'+c[0]+'</span><p class="count-note">'+c[2]+'</p>'
      +'<textarea id="sw'+i+'" rows="4" placeholder="one per line"></textarea></div>';}).join('')+'</div>'
    +'<div style="margin-top:12px"><button class="btn tools sw-png">\u2b07 Download (PNG)</button> <button class="btn ghost" onclick="navShare()">\u2197 Share</button></div></div>';
  el.querySelector('.sw-png').addEventListener('click',function(){
    var W=760,H=560,cv=document.createElement('canvas');cv.width=W;cv.height=H;var x=cv.getContext('2d');
    x.fillStyle='#FFFDF6';x.fillRect(0,0,W,H);x.fillStyle='#2A2140';x.font='700 24px Georgia';x.fillText('SWOT Analysis',22,38);
    x.font='12px monospace';x.fillStyle='#6a5f82';x.fillText('made with Navigator',22,56);
    var pos=[[30,80],[390,80],[30,320],[390,320]];
    q.forEach(function(c,i){var v=(document.getElementById('sw'+i).value||'').split('\n').filter(Boolean);
      x.fillStyle=c[1];x.fillRect(pos[i][0],pos[i][1],340,30);x.fillStyle='#fff';x.font='700 15px sans-serif';x.fillText(c[0],pos[i][0]+10,pos[i][1]+20);
      x.fillStyle='#2A2140';x.font='13px sans-serif';v.slice(0,10).forEach(function(t,j){x.fillText('\u2022 '+t.slice(0,40),pos[i][0]+8,pos[i][1]+54+j*20);});});
    var a=document.createElement('a');a.download='swot.png';a.href=cv.toDataURL();a.click();
  });
};

/* ===== RACI Matrix ===== */
window.initRACI=function(root){
  var el=document.getElementById(root); if(!el) return;
  el.innerHTML='<div class="tool-box"><div class="trow"><label>Tasks (one per line)</label></div><textarea id="ra-t" rows="4" placeholder="Write spec\nBuild feature\nQA\nLaunch"></textarea>'
    +'<div class="trow" style="margin-top:8px"><label>People (comma-separated)</label></div><input id="ra-p" placeholder="Ana, Ben, Chen, Dev">'
    +'<button class="btn ra-go" style="margin-top:10px">Build matrix</button><div id="ra-out" style="margin-top:12px;overflow:auto"></div>'
    +'<div style="margin-top:12px"><button class="btn tools ra-csv">\u2b07 Download (CSV)</button></div></div>';
  var tasks=[],ppl=[];
  el.querySelector('.ra-go').addEventListener('click',function(){
    tasks=(document.getElementById('ra-t').value||'').split('\n').map(function(s){return s.trim();}).filter(Boolean);
    ppl=(document.getElementById('ra-p').value||'').split(',').map(function(s){return s.trim();}).filter(Boolean);
    var h='<table class="raci"><tr><th>Task</th>'+ppl.map(function(p){return '<th>'+p.replace(/</g,'')+'</th>';}).join('')+'</tr>';
    tasks.forEach(function(t,i){h+='<tr><td>'+t.replace(/</g,'&lt;')+'</td>'+ppl.map(function(p,j){
      return '<td><select data-i="'+i+'" data-j="'+j+'"><option value=""></option><option>R</option><option>A</option><option>C</option><option>I</option></select></td>';}).join('')+'</tr>';});
    h+='</table><p class="count-note">R = Responsible &middot; A = Accountable (one per row) &middot; C = Consulted &middot; I = Informed</p>';
    document.getElementById('ra-out').innerHTML=h;
  });
  el.querySelector('.ra-csv').addEventListener('click',function(){
    if(!tasks.length)return;var rows=[['Task'].concat(ppl)];
    tasks.forEach(function(t,i){var r=[t];ppl.forEach(function(p,j){var s=el.querySelector('select[data-i="'+i+'"][data-j="'+j+'"]');r.push(s?s.value:'');});rows.push(r);});
    var csv=rows.map(function(r){return r.map(function(c){return '"'+(c||'').replace(/"/g,'""')+'"';}).join(',');}).join('\n');
    var a=document.createElement('a');a.download='raci.csv';a.href='data:text/csv;charset=utf-8,'+encodeURIComponent(csv);a.click();
  });
};

/* ===== Decision Tree (expected value) ===== */
window.initDecisionTree=function(root){
  var el=document.getElementById(root); if(!el) return;
  el.innerHTML='<div class="tool-box"><p class="count-note">Add options; for each, list outcomes as <code>probability%, value</code> (one per line). We compute expected value.</p><div id="dt-opts"></div>'
    +'<button class="btn ghost dt-add" style="margin-top:8px">+ Add option</button> <button class="btn dt-go">Compute</button><div id="dt-out" style="margin-top:14px"></div></div>';
  var wrap=el.querySelector('#dt-opts');
  function addOpt(n){var d=document.createElement('div');d.className='card';d.style.margin='8px 0';
    d.innerHTML='<input class="dt-name" placeholder="Option name" value="'+(n||'')+'"><textarea class="dt-out-lines" rows="3" placeholder="70%, 100000\n30%, -20000" style="margin-top:6px"></textarea>';wrap.appendChild(d);}
  addOpt('Option A');addOpt('Option B');
  el.querySelector('.dt-add').addEventListener('click',function(){addOpt('');});
  el.querySelector('.dt-go').addEventListener('click',function(){
    var res=[];el.querySelectorAll('#dt-opts .card').forEach(function(c){
      var nm=c.querySelector('.dt-name').value||'Option';var lines=(c.querySelector('.dt-out-lines').value||'').split('\n').filter(Boolean);
      var ev=0,ok=true;lines.forEach(function(l){var m=l.split(',');var p=parseFloat(m[0])/100;var v=parseFloat(m[1]);if(isNaN(p)||isNaN(v)){ok=false;return;}ev+=p*v;});
      res.push({nm:nm,ev:ev,ok:ok});});
    res.sort(function(a,b){return b.ev-a.ev;});
    var max=Math.max.apply(null,res.map(function(r){return Math.abs(r.ev);}))||1;
    var h=res.map(function(r,i){var w=Math.max(4,Math.abs(r.ev)/max*100);var col=r.ev>=0?'#2FBF71':'#F0544F';
      return '<div style="margin:8px 0"><strong>'+(i===0?'\u2605 ':'')+r.nm.replace(/</g,'')+'</strong> &mdash; EV '+(r.ev>=0?'+':'')+Math.round(r.ev).toLocaleString()
        +'<div style="height:14px;background:'+col+';width:'+w+'%;border-radius:7px;margin-top:3px"></div></div>';}).join('');
    document.getElementById('dt-out').innerHTML=h+'<p class="count-note">Expected value = &Sigma; (probability &times; value). Highest EV is starred &mdash; but weigh the downside you can\'t afford.</p>';
  });
};

/* ===== Mental-Model Finder ===== */
window.initModelFinder=function(root){
  var el=document.getElementById(root); if(!el) return;
  var M=[["First Principles Thinking","stuck copying,assumption,fundamental,rethink,innovate","/mental-models/first-principles-thinking/"],
   ["Inversion","avoid failure,what could go wrong,risk,worst case","/mental-models/inversion/"],
   ["Second-Order Thinking","consequences,side effects,long term,ripple","/mental-models/second-order-thinking/"],
   ["Opportunity Cost","tradeoff,choose,alternative,time,allocate","/mental-models/opportunity-cost/"],
   ["Circle of Competence","expertise,know,unknown,stay in lane","/mental-models/circle-of-competence/"],
   ["Margin of Safety","risk,buffer,uncertain,safe,downside","/mental-models/margin-of-safety/"],
   ["Incentives","behavior,motivation,people,reward,align","/mental-models/incentives/"],
   ["Compounding","growth,long term,patience,habit,interest","/mental-models/compounding/"],
   ["Pareto Principle","priority,80 20,focus,few,vital","/mental-models/pareto-principle/"],
   ["Occam's Razor","simple,complex,explanation,assume","/mental-models/occams-razor/"],
   ["Bottleneck / Theory of Constraints","slow,constraint,limit,throughput,process","/mental-models/bottleneck/"],
   ["Feedback Loops","system,reinforce,balance,cycle,dynamic","/mental-models/feedback-loops/"],
   ["Loss Aversion","fear,loss,decision,bias,risk","/mental-models/loss-aversion/"],
   ["Network Effects","platform,users,scale,moat,growth","/mental-models/network-effects/"],
   ["Regret Minimization","big decision,irreversible,fear,future,career","/mental-models/regret-minimization/"]];
  el.innerHTML='<div class="tool-box"><label>Describe your problem or situation</label>'
    +'<input id="mf-q" class="filter-input" placeholder="e.g. I keep making the same hiring mistake"><div id="mf-out" style="margin-top:14px"></div></div>';
  function go(){
    var q=(document.getElementById('mf-q').value||'').toLowerCase();
    if(q.length<3){document.getElementById('mf-out').innerHTML='<p class="count-note">Type a few words to get matched models.</p>';return;}
    var words=q.split(/\s+/);
    var scored=M.map(function(m){var tags=m[1].split(',');var sc=0;tags.forEach(function(t){words.forEach(function(w){if(w.length>2&&t.indexOf(w)>=0)sc++;});});
      if(m[0].toLowerCase().indexOf(q)>=0)sc+=2;return {m:m,sc:sc};}).filter(function(o){return o.sc>0;}).sort(function(a,b){return b.sc-a.sc;}).slice(0,5);
    if(!scored.length){document.getElementById('mf-out').innerHTML='<p class="count-note">No direct match &mdash; browse all models on the <a href="/mental-models/">Mental Models</a> page.</p>';return;}
    document.getElementById('mf-out').innerHTML=scored.map(function(o){return '<a class="card" style="margin:8px 0" href="'+o.m[2]+'"><span class="chip strat">Mental Model</span><h3 style="margin:.2em 0 0">'+o.m[0]+'</h3></a>';}).join('');
  }
  document.getElementById('mf-q').addEventListener('input',go);
};

/* ===== Cost-Benefit Calculator ===== */
window.initCostBenefit=function(root){
  var el=document.getElementById(root); if(!el) return;
  el.innerHTML='<div class="tool-box"><div class="grid c2">'
   +'<div><label>Benefits (label = value, one per line)</label><textarea id="cb-b" rows="5" placeholder="New revenue = 120000\nTime saved = 30000"></textarea></div>'
   +'<div><label>Costs (label = value, one per line)</label><textarea id="cb-c" rows="5" placeholder="Software = 40000\nTraining = 15000"></textarea></div>'
   +'</div><button class="btn cb-go" style="margin-top:10px">Calculate</button><div id="cb-out" class="result" style="margin-top:14px;display:none"></div></div>';
  function parse(id){var t=(document.getElementById(id).value||'').split('\n');var tot=0,rows=[];
    t.forEach(function(l){var m=l.split('=');if(m.length<2)return;var v=parseFloat(m[1].replace(/[^0-9.\-]/g,''));if(isNaN(v))return;rows.push([m[0].trim(),v]);tot+=v;});return {tot:tot,rows:rows};}
  el.querySelector('.cb-go').addEventListener('click',function(){
    var B=parse('cb-b'),C=parse('cb-c');var net=B.tot-C.tot;var ratio=C.tot?B.tot/C.tot:0;
    var col=net>=0?'#2F9E6E':'#D9695A';
    var out=document.getElementById('cb-out');out.style.display='';
    out.innerHTML='<div style="font-size:1.1rem"><strong>Net benefit: <span style="color:'+col+'">'+(net>=0?'+':'')+Math.round(net).toLocaleString()+'</span></strong></div>'
      +'<p class="count-note">Total benefits '+Math.round(B.tot).toLocaleString()+' &minus; total costs '+Math.round(C.tot).toLocaleString()
      +' &middot; benefit-to-cost ratio '+(ratio?ratio.toFixed(2):'—')+'</p>'
      +'<p>'+(net>=0?'The numbers favour going ahead. Now pressure-test the assumptions behind your biggest benefit line.':'The costs outweigh the measured benefits. Either the benefits are undercounted or this isn\'t worth it &mdash; check which before proceeding.')+'</p>';
  });
};

/* ===== Unit-Economics Calculator ===== */
window.initUnitEconomics=function(root){
  var el=document.getElementById(root); if(!el) return;
  el.innerHTML='<div class="tool-box">'
   +'<div class="trow"><label>Revenue per customer / month ($) </label><input id="ue-arpu" type="number" value="100"></div>'
   +'<div class="trow"><label>Gross margin (%) </label><input id="ue-gm" type="number" value="80"></div>'
   +'<div class="trow"><label>Monthly churn (%) </label><input id="ue-ch" type="number" value="5"></div>'
   +'<div class="trow"><label>Customer acquisition cost ($) </label><input id="ue-cac" type="number" value="400"></div>'
   +'<button class="btn ue-go" style="margin-top:10px">Calculate</button><div id="ue-out" class="result" style="margin-top:14px;display:none"></div></div>';
  el.querySelector('.ue-go').addEventListener('click',function(){
    var arpu=+document.getElementById('ue-arpu').value, gm=+document.getElementById('ue-gm').value/100,
        ch=+document.getElementById('ue-ch').value/100, cac=+document.getElementById('ue-cac').value;
    var mgm=arpu*gm; var ltv=ch>0?mgm/ch:0; var ratio=cac>0?ltv/cac:0; var payback=mgm>0?cac/mgm:0;
    var verdict = ratio>=3 ? ['Healthy','#2F9E6E'] : ratio>=1 ? ['Marginal','#C07C3E'] : ['Unsustainable','#D9695A'];
    var out=document.getElementById('ue-out');out.style.display='';
    out.innerHTML='<div style="font-size:1.1rem"><strong>LTV:CAC = <span style="color:'+verdict[1]+'">'+ratio.toFixed(1)+'</span> &middot; '+verdict[0]+'</strong></div>'
      +'<p class="count-note">Lifetime value ≈ $'+Math.round(ltv).toLocaleString()+' &middot; CAC payback ≈ '+payback.toFixed(1)+' months &middot; avg lifetime ≈ '+(ch>0?(1/ch).toFixed(1):'∞')+' months</p>'
      +'<p>'+(ratio>=3?'Rule of thumb: 3:1 or better is healthy. You can likely spend more to grow.':ratio>=1?'You recover CAC but the margin for growth is thin &mdash; lower CAC or raise retention.':'You lose money per customer. Fix churn or CAC before scaling spend.')+'</p>';
  });
};

/* ===== Scenario Planner ===== */
window.initScenario=function(root){
  var el=document.getElementById(root); if(!el) return;
  el.innerHTML='<div class="tool-box"><p class="count-note">Estimate an outcome across three scenarios. Probabilities should sum to ~100%.</p>'
   +'<div class="trow"><label style="width:90px">Worst</label> value <input id="sc-wv" type="number" value="-20000" style="max-width:120px"> prob% <input id="sc-wp" type="number" value="20" style="max-width:80px"></div>'
   +'<div class="trow"><label style="width:90px">Base</label> value <input id="sc-bv" type="number" value="50000" style="max-width:120px"> prob% <input id="sc-bp" type="number" value="55" style="max-width:80px"></div>'
   +'<div class="trow"><label style="width:90px">Best</label> value <input id="sc-tv" type="number" value="150000" style="max-width:120px"> prob% <input id="sc-tp" type="number" value="25" style="max-width:80px"></div>'
   +'<button class="btn sc-go" style="margin-top:10px">Calculate</button><div id="sc-out" class="result" style="margin-top:14px;display:none"></div></div>';
  el.querySelector('.sc-go').addEventListener('click',function(){
    var wv=+document.getElementById('sc-wv').value,wp=+document.getElementById('sc-wp').value/100;
    var bv=+document.getElementById('sc-bv').value,bp=+document.getElementById('sc-bp').value/100;
    var tv=+document.getElementById('sc-tv').value,tp=+document.getElementById('sc-tp').value/100;
    var psum=wp+bp+tp; var ev=wv*wp+bv*bp+tv*tp;
    var out=document.getElementById('sc-out');out.style.display='';
    out.innerHTML='<div style="font-size:1.1rem"><strong>Expected value ≈ <span style="color:var(--sea)">'+(ev>=0?'+':'')+Math.round(ev).toLocaleString()+'</span></strong></div>'
      +'<p class="count-note">Range '+Math.round(wv).toLocaleString()+' to '+Math.round(tv).toLocaleString()+(Math.abs(psum-1)>0.02?' &middot; ⚠ probabilities sum to '+Math.round(psum*100)+'%':'')+'</p>'
      +'<p>Expected value tells you the average bet; the <em>worst case</em> tells you whether you can afford to be wrong. Never take a positive-EV bet whose worst case you can\'t survive.</p>';
  });
};

/* ===== Porter's Five Forces Analyzer ===== */
window.initFiveForces=function(root){
  var el=document.getElementById(root); if(!el) return;
  var F=[["Competitive rivalry","How intense is head-to-head competition?"],
   ["Threat of new entrants","How easily can new competitors enter?"],
   ["Supplier power","How much leverage do your suppliers hold?"],
   ["Buyer power","How much leverage do your customers hold?"],
   ["Threat of substitutes","How easily can buyers switch to an alternative?"]];
  el.innerHTML='<div class="tool-box">'+F.map(function(f,i){
    return '<div class="trow" style="justify-content:space-between"><label style="margin:0">'+f[0]+'<br><span class="count-note">'+f[1]+'</span></label>'
      +'<span><input type="range" id="ff'+i+'" min="1" max="10" value="5" oninput="document.getElementById(\'ffv'+i+'\').textContent=this.value"> <b id="ffv'+i+'">5</b>/10</span></div>';}).join('')
    +'<button class="btn ff-go" style="margin-top:10px">Analyse</button><div id="ff-out" class="result" style="margin-top:14px;display:none"></div></div>';
  el.querySelector('.ff-go').addEventListener('click',function(){
    var vals=F.map(function(_,i){return +document.getElementById('ff'+i).value;});
    var avg=vals.reduce(function(a,b){return a+b;},0)/5;
    var attr=11-avg; // low forces => attractive
    var verdict=attr>=7?['Attractive industry','#2F9E6E']:attr>=4?['Mixed — pick your position','#C07C3E']:['Tough industry','#D9695A'];
    var strongest=F[vals.indexOf(Math.max.apply(null,vals))][0];
    var out=document.getElementById('ff-out');out.style.display='';
    out.innerHTML='<div style="font-size:1.1rem"><strong>Industry attractiveness: <span style="color:'+verdict[1]+'">'+attr.toFixed(1)+'/10 — '+verdict[0]+'</span></strong></div>'
      +'<p class="count-note">'+F.map(function(f,i){return f[0]+': '+vals[i];}).join(' &middot; ')+'</p>'
      +'<p>Your biggest pressure is <strong>'+strongest+'</strong>. High forces compress profits &mdash; strategy is about finding or building the position where they bite least. Pair with the <a href="/moats/">7 Powers</a> to turn a defensible position into a durable one.</p>';
  });
};

/* ===== Business Model Canvas ===== */
window.initBMC=function(root){
  var el=document.getElementById(root); if(!el) return;
  var B=[["kp","Key Partners"],["ka","Key Activities"],["kr","Key Resources"],["vp","Value Propositions"],
   ["cr","Customer Relationships"],["ch","Channels"],["cs","Customer Segments"],["co","Cost Structure"],["rs","Revenue Streams"]];
  el.innerHTML='<div class="tool-box"><div class="grid c3">'+B.map(function(b){
    return '<div><label>'+b[1]+'</label><textarea id="bmc-'+b[0]+'" rows="3"></textarea></div>';}).join('')+'</div>'
    +'<button class="btn bmc-go" style="margin-top:10px">Build canvas</button> <button class="btn ghost bmc-csv">\u2b07 Download (CSV)</button>'
    +'<div id="bmc-out" style="margin-top:14px"></div></div>';
  el.querySelector('.bmc-go').addEventListener('click',function(){
    var h='<table class="raci"><tr>'+B.map(function(b){return '<th>'+b[1]+'</th>';}).slice(0,3).join('')+'</tr>';
    // render as three rows of three for readability
    for(var r=0;r<3;r++){h+='<tr>';for(var c=0;c<3;c++){var b=B[r*3+c];var v=(document.getElementById('bmc-'+b[0]).value||'').replace(/</g,'&lt;').replace(/\n/g,'<br>');h+='<td style="text-align:left;vertical-align:top"><strong>'+b[1]+'</strong><br>'+v+'</td>';}h+='</tr>';}
    h+='</table>';document.getElementById('bmc-out').innerHTML=h;
  });
  el.querySelector('.bmc-csv').addEventListener('click',function(){
    var rows=B.map(function(b){return '"'+b[1]+'","'+(document.getElementById('bmc-'+b[0]).value||'').replace(/"/g,'""')+'"';});
    var a=document.createElement('a');a.download='business-model-canvas.csv';a.href='data:text/csv;charset=utf-8,'+encodeURIComponent(rows.join('\n'));a.click();
  });
};

/* ===== Pre-Mortem Worksheet ===== */
window.initPreMortem=function(root){
  var el=document.getElementById(root); if(!el) return;
  el.innerHTML='<div class="tool-box"><label>The plan / decision</label><input id="pm-plan" placeholder="e.g. Launch the new pricing tier in Q3">'
   +'<p class="count-note" style="margin-top:10px">Imagine it is a year from now and it <strong>failed</strong>. List the reasons it failed (one per line):</p>'
   +'<textarea id="pm-reasons" rows="5" placeholder="Customers didn\'t understand the value\nSales team wasn\'t trained\nCompetitor cut prices"></textarea>'
   +'<button class="btn pm-go" style="margin-top:10px">Build risk table</button> <button class="btn ghost pm-csv">\u2b07 CSV</button>'
   +'<div id="pm-out" style="margin-top:14px"></div></div>';
  el.querySelector('.pm-go').addEventListener('click',function(){
    var rs=(document.getElementById('pm-reasons').value||'').split('\n').map(function(s){return s.trim();}).filter(Boolean);
    var h='<table class="raci"><tr><th>Failure reason</th><th>Likelihood</th><th>Mitigation (write now)</th></tr>';
    rs.forEach(function(r,i){h+='<tr><td style="text-align:left">'+r.replace(/</g,'&lt;')+'</td>'
      +'<td><select id="pm-l'+i+'"><option>Low</option><option selected>Medium</option><option>High</option></select></td>'
      +'<td><input id="pm-m'+i+'" placeholder="How you\'ll prevent it" style="width:100%"></td></tr>';});
    h+='</table><p class="count-note">Prioritise the High-likelihood rows: pre-commit to a mitigation before you start.</p>';
    document.getElementById('pm-out').innerHTML=h; el._rs=rs;
  });
  el.querySelector('.pm-csv').addEventListener('click',function(){
    if(!el._rs)return;var rows=[['Plan',(document.getElementById('pm-plan').value||'')]];rows.push(['Reason','Likelihood','Mitigation']);
    el._rs.forEach(function(r,i){rows.push([r,(document.getElementById('pm-l'+i)||{}).value||'',(document.getElementById('pm-m'+i)||{}).value||'']);});
    var csv=rows.map(function(r){return r.map(function(c){return '"'+(c||'').replace(/"/g,'""')+'"';}).join(',');}).join('\n');
    var a=document.createElement('a');a.download='pre-mortem.csv';a.href='data:text/csv;charset=utf-8,'+encodeURIComponent(csv);a.click();
  });
};

/* ===== Second-Order Thinking Mapper ===== */
window.initSecondOrder=function(root){
  var el=document.getElementById(root); if(!el) return;
  el.innerHTML='<div class="tool-box"><label>The decision or action</label><input id="so-act" placeholder="e.g. We cut prices by 20%">'
   +'<div style="margin-top:10px"><label>Then what happens? (1st-order — immediate)</label><textarea id="so-1" rows="2"></textarea></div>'
   +'<div><label>And then what? (2nd-order — the consequence of that)</label><textarea id="so-2" rows="2"></textarea></div>'
   +'<div><label>And then what? (3rd-order — the long game)</label><textarea id="so-3" rows="2"></textarea></div>'
   +'<button class="btn so-go" style="margin-top:10px">Map the cascade</button><div id="so-out" style="margin-top:14px"></div></div>';
  el.querySelector('.so-go').addEventListener('click',function(){
    var act=document.getElementById('so-act').value||'The action';
    var steps=[['Decision',act,'#0C5460'],['1st order',document.getElementById('so-1').value,'#0E7C8C'],
      ['2nd order',document.getElementById('so-2').value,'#C07C3E'],['3rd order',document.getElementById('so-3').value,'#D9695A']];
    var h=steps.filter(function(s){return s[1];}).map(function(s){
      return '<div style="border-left:3px solid '+s[2]+';padding:4px 0 4px 12px;margin:8px 0"><span class="count-note" style="color:'+s[2]+'">'+s[0]+'</span><br>'+s[1].replace(/</g,'&lt;')+'</div>';}).join('');
    document.getElementById('so-out').innerHTML=h+'<p class="count-note">Most people stop at the 1st order. The edge is in the 2nd and 3rd &mdash; the effects of the effects. If the later orders reverse the early win, reconsider.</p>';
  });
};
