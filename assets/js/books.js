// Load book covers from OpenLibrary at runtime; fall back to the symbol tile.
(function(){
  if(!('IntersectionObserver' in window)) return;
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){ if(e.isIntersecting){ load(e.target); io.unobserve(e.target);} });
  },{rootMargin:"400px"});
  document.querySelectorAll('[data-book]').forEach(function(el){ io.observe(el); });
  function load(el){
    var v=el.getAttribute('data-book')||''; var p=v.split('|'); var t=(p[0]||'').trim(); var a=(p[1]||'').trim();
    if(!t) return;
    var url='https://openlibrary.org/search.json?title='+encodeURIComponent(t)+(a?'&author='+encodeURIComponent(a):'')+'&limit=1&fields=cover_i';
    fetch(url).then(function(r){return r.ok?r.json():null;}).then(function(d){
      if(d && d.docs && d.docs[0] && d.docs[0].cover_i){
        var src='https://covers.openlibrary.org/b/id/'+d.docs[0].cover_i+'-M.jpg';
        var im=new Image();
        im.onload=function(){ if(im.naturalWidth>2){ el.style.backgroundImage='url("'+src+'")'; el.classList.add('has-img'); } };
        im.src=src;
      }
    }).catch(function(){});
  }
})();
