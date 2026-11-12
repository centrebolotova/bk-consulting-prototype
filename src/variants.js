
// ===== панель «Варианты оформления» (только в прототипе) =====
(function(){
  var HERO=[['forest','Шатёр в лесу'],['cabin','Домик в берёзах'],['city','Городской отель'],['room','Интерьер'],['land','Участок на рассвете'],['concept','Концепция у реки'],['cycle','Смена фото'],['video','Видео'],['split','Текст и фото'],['type','Без фото']];
  var PAL=[['cream','Молочный'],['white','Белый'],['stone','Тёплый серый'],['sage','Шалфей']];
  var hasHero=!!document.querySelector('.hero-media');
  function get(k,d){try{return localStorage.getItem('bk-'+k)||d}catch(e){return d}}
  function put(k,v){try{localStorage.setItem('bk-'+k,v)}catch(e){}}
  var cycleT=null;
  var el=document.createElement('div');el.className='vpanel';
  var html='<div class="vbox">';
  if(hasHero){html+='<h5>Первый экран</h5><div class="vrow">'+HERO.map(function(x){return '<button class="v" data-h="'+x[0]+'">'+x[1]+'</button>'}).join('')+'</div>'}
  html+='<h5>Цвет фона</h5><div class="vrow">'+PAL.map(function(x){return '<button class="v" data-p="'+x[0]+'">'+x[1]+'</button>'}).join('')+'</div>';
  html+='<p>Видео — отрывок вашей видеопрезентации велнес-отеля. Панель есть только в прототипе.</p></div><button class="vtoggle">Варианты оформления</button>';
  el.innerHTML=html;document.body.appendChild(el);
  function mark(){
    el.querySelectorAll('[data-h]').forEach(function(b){b.classList.toggle('on',b.dataset.h===document.body.dataset.hero)});
    el.querySelectorAll('[data-p]').forEach(function(b){b.classList.toggle('on',b.dataset.p===(document.body.dataset.pal||'cream'))});
  }
  function setHero(v){
    document.body.dataset.hero=v;put('hero',v);
    var vid=document.querySelector('.h-video');
    if(vid){if(v==='video'){if(!vid.getAttribute('src'))vid.src=vid.dataset.src;var p=vid.play();if(p&&p.catch)p.catch(function(){})}else vid.pause()}
    clearInterval(cycleT);
    var imgs=[].slice.call(document.querySelectorAll('.hero-media img'));
    imgs.forEach(function(i){i.classList.remove('on')});
    if(v==='cycle'&&imgs.length){var k=0;imgs[0].classList.add('on');cycleT=setInterval(function(){imgs[k].classList.remove('on');k=(k+1)%imgs.length;imgs[k].classList.add('on')},7000)}
    mark();
  }
  function setPal(v){document.body.dataset.pal=v;put('pal',v);mark()}
  el.querySelector('.vtoggle').onclick=function(){el.classList.toggle('open')};
  el.querySelectorAll('[data-h]').forEach(function(b){b.onclick=function(){setHero(b.dataset.h)}});
  el.querySelectorAll('[data-p]').forEach(function(b){b.onclick=function(){setPal(b.dataset.p)}});
  if(hasHero)setHero(get('hero','forest'));
  setPal(get('pal','cream'));
})();

// видео в карточках исследований: грузим и запускаем, когда карточка на экране
(function(){
  var vs=[].slice.call(document.querySelectorAll('.vid video'));
  if(!vs.length||!('IntersectionObserver' in window))return;
  var io=new IntersectionObserver(function(es){es.forEach(function(e){var v=e.target;if(e.isIntersecting){if(!v.getAttribute('src'))v.src=v.dataset.src;var p=v.play();if(p&&p.catch)p.catch(function(){})}else v.pause()})},{threshold:.4});
  vs.forEach(function(v){io.observe(v)});
})();
