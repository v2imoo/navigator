/* Navigator — wiki.js  (portrait loader, runtime)
   Fills every .portrait[data-wiki] with a real photo, most-reliable source first:
     1) explicit data-img URL (any source) if provided
     2) Wikipedia Action API (origin=* — reliably CORS-enabled) pageimages
     3) Wikipedia REST summary (originalimage / thumbnail) as a backup
   Falls back to the coloured monogram if all fail. Lazy-loaded. */
(function(){
  var ACTION='https://en.wikipedia.org/w/api.php';
  var REST='https://en.wikipedia.org/api/rest_v1/page/summary/';

  function place(el, src){
    if(!src) return;
    var img=new Image();
    img.alt=el.getAttribute('data-name')||el.getAttribute('data-wiki')||'';
    img.className=(el.className.replace('mono','').replace(/\s+/g,' ').trim())||'portrait';
    img.loading='lazy'; img.decoding='async'; img.referrerPolicy='no-referrer';
    img.onload=function(){ if(el.parentNode) el.replaceWith(img); };
    img.src=src;
  }

  function viaAction(title, cb){
    var url=ACTION+'?action=query&format=json&origin=*&prop=pageimages&piprop=thumbnail'+
            '&pithumbsize=640&redirects=1&titles='+encodeURIComponent(title);
    fetch(url).then(function(r){return r.ok?r.json():null;}).then(function(d){
      var p=d&&d.query&&d.query.pages||{},k=Object.keys(p)[0];
      cb(k&&p[k].thumbnail&&p[k].thumbnail.source||null);
    }).catch(function(){ cb(null); });
  }

  function viaREST(title, cb){
    fetch(REST+encodeURIComponent(title.replace(/ /g,'_'))).then(function(r){return r.ok?r.json():null;})
    .then(function(d){ cb(d&&((d.thumbnail&&d.thumbnail.source)||(d.originalimage&&d.originalimage.source))||null); })
    .catch(function(){ cb(null); });
  }

  function load(el){
    var explicit=el.getAttribute('data-img');
    if(explicit){ place(el, explicit); return; }
    var title=el.getAttribute('data-wiki'); if(!title) return;
    viaAction(title, function(src){
      if(src){ place(el, src); }
      else viaREST(title, function(s2){ place(el, s2); });
    });
  }

  var io=('IntersectionObserver' in window) ? new IntersectionObserver(function(es){
    es.forEach(function(e){ if(e.isIntersecting){ load(e.target); io.unobserve(e.target); } });
  },{rootMargin:'500px'}) : null;

  function boot(){
    document.querySelectorAll('.portrait[data-wiki],.portrait[data-img]').forEach(function(el){
      if(io) io.observe(el); else load(el);
    });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
