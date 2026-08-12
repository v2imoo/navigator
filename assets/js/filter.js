(function(){
  document.querySelectorAll('[data-filter-root]').forEach(function(root){
    var input=root.querySelector('[data-filter-input]');
    var cards=[].slice.call(root.querySelectorAll('.fcard'));
    var btns=[].slice.call(root.querySelectorAll('[data-cat]'));
    var active='';
    function apply(){
      var q=((input&&input.value)||'').trim().toLowerCase();
      var shown=0;
      cards.forEach(function(c){
        var okq=!q||c.getAttribute('data-name').indexOf(q)>=0;
        var okc=!active|| c.getAttribute('data-cat')===active || (active.length===1 && c.getAttribute('data-letter')===active);
        var vis=okq&&okc; c.style.display=vis?'':'none'; if(vis)shown++;
      });
      var count=root.querySelector('[data-filter-count]'); if(count)count.textContent=shown;
    }
    if(input)input.addEventListener('input',apply);
    btns.forEach(function(b){ b.addEventListener('click',function(){
      var v=b.getAttribute('data-cat'); active=(active===v)?'':v;
      btns.forEach(function(x){ x.classList.toggle('active', x.getAttribute('data-cat')===active); });
      apply();
    });});
  });
})();
