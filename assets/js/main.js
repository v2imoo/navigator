// NAVIGATOR — core UI
(function(){
  // Mobile drawer
  var burger=document.getElementById('menuBtn'), drawer=document.getElementById('drawer');
  function open(){drawer.classList.add('open');document.body.style.overflow='hidden';}
  function close(){drawer.classList.remove('open');document.body.style.overflow='';}
  if(burger){burger.addEventListener('click',open);}
  if(drawer){
    drawer.addEventListener('click',function(e){if(e.target===drawer||e.target.hasAttribute('data-close'))close();});
    document.addEventListener('keydown',function(e){if(e.key==='Escape')close();});
  }
  // Accessibility: hyperlegible font toggle (persists on device only)
  try{ if(localStorage.getItem('nav-a11y')==='1')document.body.classList.add('a11y'); }catch(e){}
  var a11y=document.getElementById('a11yToggle');
  if(a11y){a11y.addEventListener('click',function(){
    document.body.classList.toggle('a11y');
    try{localStorage.setItem('nav-a11y',document.body.classList.contains('a11y')?'1':'0');}catch(e){}
  });}
  // Copy-link helper
  window.navShare=function(txt){
    var url=location.href;
    if(navigator.share){navigator.share({title:document.title,url:url}).catch(function(){});}
    else if(navigator.clipboard){navigator.clipboard.writeText(url);alert('Link copied to clipboard');}
  };
})();
