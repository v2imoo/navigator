// Load real photos/logos from Wikipedia at runtime; fall back to the monogram tile.
(function(){
  if(!('IntersectionObserver' in window)) return;
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){ if(e.isIntersecting){ load(e.target); io.unobserve(e.target); } });
  },{rootMargin:"300px"});
  document.querySelectorAll('[data-wiki]').forEach(function(el){ io.observe(el); });
  function load(el){
    var name=el.getAttribute('data-wiki'); if(!name) return;
    fetch('https://en.wikipedia.org/api/rest_v1/page/summary/'+encodeURIComponent(name))
      .then(function(r){ return r.ok?r.json():null; })
      .then(function(d){
        if(d && d.thumbnail && d.thumbnail.source){
          var src=d.thumbnail.source.replace(/\/\d+px-/,'/400px-');
          var im=new Image();
          im.onload=function(){ el.style.backgroundImage='url("'+src+'")'; el.classList.add('has-img'); };
          im.src=src;
        }
      }).catch(function(){});
  }
})();
