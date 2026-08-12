// Load photos/logos from Wikipedia via the MediaWiki Action API (origin=* = anonymous CORS).
// Falls back silently to the monogram tile. Fixing THIS file updates every page's images.
(function(){
  if(!('IntersectionObserver' in window)) return;
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){ if(e.isIntersecting){ load(e.target); io.unobserve(e.target); } });
  },{rootMargin:"500px"});
  document.querySelectorAll('[data-wiki]').forEach(function(el){ io.observe(el); });

  function paint(el,src){
    var im=new Image();
    im.onload=function(){ if(im.naturalWidth>1){ el.style.backgroundImage='url("'+src+'")'; el.classList.add('has-img'); } };
    im.src=src;
  }
  function load(el){
    var name=el.getAttribute('data-wiki'); if(!name) return;
    var api='https://en.wikipedia.org/w/api.php?action=query&format=json&origin=*&redirects=1'
          + '&prop=pageimages&piprop=thumbnail&pithumbsize=400&titles='+encodeURIComponent(name);
    fetch(api).then(function(r){ return r.ok?r.json():null; }).then(function(d){
      if(!d||!d.query||!d.query.pages) return;
      var pages=d.query.pages, k=Object.keys(pages)[0], p=pages[k];
      if(p&&p.thumbnail&&p.thumbnail.source){ paint(el,p.thumbnail.source); }
    }).catch(function(){});
  }
})();
