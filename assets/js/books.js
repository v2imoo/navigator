// Load book covers from OpenLibrary (CORS-enabled). Falls back silently to the tile.
(function(){
  if(!('IntersectionObserver' in window)) return;
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){ if(e.isIntersecting){ load(e.target); io.unobserve(e.target); } });
  },{rootMargin:"600px"});
  document.querySelectorAll('[data-book]').forEach(function(el){ io.observe(el); });

  function paint(el,id){
    var src='https://covers.openlibrary.org/b/id/'+id+'-M.jpg';
    var im=new Image();
    im.onload=function(){ if(im.naturalWidth>2){ el.style.backgroundImage='url("'+src+'")'; el.classList.add('has-img'); } };
    im.src=src;
  }
  function tryQuery(el,url,next){
    fetch(url).then(function(r){ return r.ok?r.json():null; }).then(function(d){
      var doc=d&&d.docs&&d.docs[0];
      if(doc&&doc.cover_i){ paint(el,doc.cover_i); }
      else if(next){ next(); }
    }).catch(function(){ if(next) next(); });
  }
  function load(el){
    var t=(el.getAttribute('data-book')||'').split('|')[0].trim(); if(!t) return;
    var byTitle='https://openlibrary.org/search.json?limit=1&fields=cover_i&title='+encodeURIComponent(t);
    var byQuery='https://openlibrary.org/search.json?limit=1&fields=cover_i&q='+encodeURIComponent(t);
    tryQuery(el,byTitle,function(){ tryQuery(el,byQuery,null); });
  }
})();
