
// ===== панель «Варианты оформления» (только в прототипе) =====
(function(){
  var HERO=[['forest','Шатёр в лесу'],['room','Номер «Кенсингтон»'],['bath','Номер с ванной'],['teal','Номер «Алеон»'],['apart','Апартаменты'],['lobby','Лобби'],['rest','Ресторан'],['bar','Бар-кафе'],['concept','Концепция у реки'],['land','Участок на рассвете'],['cycle','Смена фото'],['video:wellness','Видео: велнес-отель'],['video:poselok','Видео: посёлок-отель'],['video:park','Видео: парк-отель'],['split','Текст и фото']];
  var PAL=[['cream','Молочный'],['white','Белый'],['stone','Тёплый серый'],['sage','Шалфей']];
  var hasHero=!!document.querySelector('.hero-media');
  function get(k,d){try{return localStorage.getItem('bk-'+k)||d}catch(e){return d}}
  function put(k,v){try{localStorage.setItem('bk-'+k,v)}catch(e){}}
  var cycleT=null;
  var el=document.createElement('div');el.className='vpanel';
  var html='<div class="vbox">';
  if(hasHero){html+='<h5>Первый экран</h5><div class="vrow">'+HERO.map(function(x){return '<button class="v" data-h="'+x[0]+'">'+x[1]+'</button>'}).join('')+'</div>'}
  html+='<h5>Цвет фона</h5><div class="vrow">'+PAL.map(function(x){return '<button class="v" data-p="'+x[0]+'">'+x[1]+'</button>'}).join('')+'</div>';
  html+='<h5>Пометки</h5><div class="vrow"><button class="v on" data-todo>Жёлтым — что подтвердить</button></div>';
  html+='<p>Видео — отрывки ваших видеопрезентаций (это визуализации). Все фото — в библиотеке: photos.html. Панель есть только в прототипе.</p></div><button class="vtoggle">Варианты оформления</button>';
  el.innerHTML=html;document.body.appendChild(el);
  function mark(){
    el.querySelectorAll('[data-h]').forEach(function(b){b.classList.toggle('on',b.dataset.h===document.body.dataset.heroFull)});
    el.querySelectorAll('[data-p]').forEach(function(b){b.classList.toggle('on',b.dataset.p===(document.body.dataset.pal||'cream'))});
  }
  function setHero(v){
    var vv=v.split(':');document.body.dataset.hero=vv[0];document.body.dataset.heroFull=v;put('hero',v);
    var vid=document.querySelector('.h-video');
    if(vid){if(vv[0]==='video'){var nm=vv[1]||'wellness';if(vid.dataset.v!==nm||!vid.getAttribute('src')){vid.dataset.v=nm;vid.poster='img/hero-'+nm+'.jpg';vid.preload='auto';vid.src='img/hero-'+nm+'.mp4';vid.load();}var p=vid.play();if(p&&p.catch)p.catch(function(){})}else vid.pause()}
    clearInterval(cycleT);
    [].slice.call(document.querySelectorAll('.hero-media img[data-src]')).forEach(function(i){if(v==='cycle'||v==='split'?/h-(forest|room|teal|apart|rest|concept)/.test(i.className):i.classList.contains('h-'+vv[0])){i.src=i.dataset.src;i.removeAttribute('data-src')}});
    var imgs=[].slice.call(document.querySelectorAll('.hero-media img'));
    imgs.forEach(function(i){i.classList.remove('on')});
    if(v==='cycle'&&imgs.length){imgs=imgs.filter(function(i){return /h-(forest|room|teal|apart|rest|concept)/.test(i.className)})}if(v==='cycle'&&imgs.length){var k=0;imgs[0].classList.add('on');cycleT=setInterval(function(){imgs[k].classList.remove('on');k=(k+1)%imgs.length;imgs[k].classList.add('on')},7000)}
    mark();
  }
  function setPal(v){document.body.dataset.pal=v;put('pal',v);mark()}
  var tb=el.querySelector('[data-todo]');if(tb)tb.onclick=function(){document.body.classList.toggle('notodo');tb.classList.toggle('on',!document.body.classList.contains('notodo'))};
  el.querySelector('.vtoggle').onclick=function(){el.classList.toggle('open')};
  el.querySelectorAll('[data-h]').forEach(function(b){b.onclick=function(){setHero(b.dataset.h)}});
  el.querySelectorAll('[data-p]').forEach(function(b){b.onclick=function(){setPal(b.dataset.p)}});
  var saved=get('hero','forest');if(!HERO.some(function(x){return x[0]===saved}))saved='forest';if(hasHero)setHero(saved);
  setPal(get('pal','cream'));
})();

// видео в карточках исследований: грузим и запускаем, когда карточка на экране
(function(){
  var vs=[].slice.call(document.querySelectorAll('.vid video'));
  if(!vs.length||!('IntersectionObserver' in window))return;
  var io=new IntersectionObserver(function(es){es.forEach(function(e){var v=e.target;if(e.isIntersecting){if(!v.getAttribute('src'))v.src=v.dataset.src;var p=v.play();if(p&&p.catch)p.catch(function(){})}else v.pause()})},{threshold:.4});
  vs.forEach(function(v){io.observe(v)});
})();
