/* Navigator — wiki.js  (multi-source portrait loader)
   Fills every .portrait[data-wiki] with a real image, trying reliable
   sources in order and falling back to the coloured monogram on failure:
     1) explicit data-img URL (any reliable source) if provided
     2) Wikipedia REST summary (originalimage / thumbnail) — usually best
     3) Wikipedia Action API   (pageimages) — broad fallback
   Uniform 4:5 frame is enforced by CSS (object-fit:cover). Lazy-loaded. */
(function(){
  var REST='https://en.wikipedia.org/api/rest_v1/page/summary/';
  var ACTION='https://en.wikipedia.org/w/api.php';
  function place(el, src){
    var img=new Image();
    img.alt=el.getAttribute('data-name')||el.getAttribute('data-wiki')||'';
    img.className=(el.className.replace('mono','').trim())||'portrait';
    img.loading='lazy';
    img.onload=function(){ el.replaceWith(img); };
    img.src=src;
  }
  function fromExplicit(el){ var u=el.getAttribute('data-img'); if(u){ place(el,u); return true; } return false; }
  function fromREST(el, title, done){
    fetch(REST+encodeURIComponent(title.replace(/ /g,'_')),{headers:{'Accept':'application/json'}})
      .then(function(r){ return r.ok?r.json():null; })
      .then(function(d){
        var src = d && ((d.originalimage&&d.originalimage.source)||(d.thumbnail&&d.thumbnail.source));
        if(src){ place(el,src); done(true); } else { done(false); }
      }).catch(function(){ done(false); });
  }
  function fromAction(el, title){
    var url=ACTION+'?action=query&format=json&origin=*&prop=pageimages&piprop=thumbnail'+
            '&pithumbsize=640&redirects=1&titles='+encodeURIComponent(title);
    fetch(url).then(function(r){return r.json();}).then(function(d){
      var pages=d&&d.query&&d.query.pages||{},k=Object.keys(pages)[0],
          thumb=k&&pages[k].thumbnail&&pages[k].thumbnail.source;
      if(thumb) place(el,thumb);
    }).catch(function(){});
  }
  function load(el){
    if(fromExplicit(el)) return;
    var title=el.getAttribute('data-wiki'); if(!title) return;
    fromREST(el, title, function(ok){ if(!ok) fromAction(el, title); });
  }
  var io=('IntersectionObserver'in window)?new IntersectionObserver(function(es){
    es.forEach(function(e){ if(e.isIntersecting){ load(e.target); io.unobserve(e.target); } });
  },{rootMargin:'400px'}):null;
  document.querySelectorAll('.portrait[data-wiki],.portrait[data-img]').forEach(function(el){
    if(io) io.observe(el); else load(el);
  });
})();
