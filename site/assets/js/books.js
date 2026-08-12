// Book covers.  1) baked /assets/img/books/{slug}.jpg  2) OpenLibrary  3) tile.
(function(){
  if(!('IntersectionObserver' in window)) return;
  function slug(s){ return s.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/(^-|-$)/g,''); }
  function bg(el,src){ el.style.backgroundImage='url("'+src+'")'; el.classList.add('has-img'); }

  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){ if(e.isIntersecting){ load(e.target); io.unobserve(e.target); } });
  },{rootMargin:"600px"});
  document.querySelectorAll('[data-book]').forEach(function(el){ io.observe(el); });

  function load(el){
    var t=(el.getAttribute('data-book')||'').split('|')[0].trim(); if(!t) return;
    var local='/assets/img/books/'+slug(t)+'.jpg';
    var im=new Image();
    im.onload=function(){ if(im.naturalWidth>2){ bg(el,local); } else api(el,t); };
    im.onerror=function(){ api(el,t); };
    im.src=local;
  }
  function api(el,t){
    fetch('https://openlibrary.org/search.json?limit=1&fields=cover_i&title='+encodeURIComponent(t))
      .then(function(r){return r.ok?r.json():null;}).then(function(d){
        var doc=d&&d.docs&&d.docs[0];
        if(doc&&doc.cover_i){ var s='https://covers.openlibrary.org/b/id/'+doc.cover_i+'-M.jpg';
          var im=new Image(); im.onload=function(){bg(el,s);}; im.src=s; }
      }).catch(function(){});
  }
})();
