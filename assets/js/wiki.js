// People photos + company logos.
// 1) baked local file  /assets/img/wiki/{slug}.jpg   (from tools/fetch_images.py — no network)
// 2) live Wikipedia API (only if the local file is missing)
// 3) coloured monogram (never a broken image)
(function(){
  if(!('IntersectionObserver' in window)) return;
  function slug(s){ return s.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/(^-|-$)/g,''); }
  function bg(el,src){ el.style.backgroundImage='url("'+src+'")'; el.classList.add('has-img'); }

  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){ if(e.isIntersecting){ load(e.target); io.unobserve(e.target); } });
  },{rootMargin:"500px"});
  document.querySelectorAll('[data-wiki]').forEach(function(el){ io.observe(el); });

  function load(el){
    var name=el.getAttribute('data-wiki'); if(!name) return;
    var local='/assets/img/wiki/'+slug(name)+'.jpg';
    var im=new Image();
    im.onload=function(){ if(im.naturalWidth>1){ bg(el,local); } else api(el,name); };
    im.onerror=function(){ api(el,name); };
    im.src=local;
  }
  function api(el,name){
    var u='https://en.wikipedia.org/w/api.php?action=query&format=json&origin=*&redirects=1'
        + '&prop=pageimages&piprop=thumbnail&pithumbsize=400&titles='+encodeURIComponent(name);
    fetch(u).then(function(r){return r.ok?r.json():null;}).then(function(d){
      if(!d||!d.query) return; var p=d.query.pages, k=Object.keys(p)[0], t=p[k].thumbnail;
      if(t&&t.source){ var im=new Image(); im.onload=function(){bg(el,t.source);}; im.src=t.source; }
    }).catch(function(){});
  }
})();
