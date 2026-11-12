// шапка: прозрачная на фото, светлая после прокрутки
const hdr=document.getElementById('hdr'), sticky=document.getElementById('sticky');
const onScroll=()=>{const y=scrollY;hdr.classList.toggle('solid',y>innerHeight*0.8);sticky.classList.toggle('show',y>innerHeight*0.6)};
addEventListener('scroll',onScroll,{passive:true});onScroll();

// плавное появление блоков
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12});
document.querySelectorAll('.rv').forEach((el,i)=>{el.style.transitionDelay=(i%4)*80+'ms';io.observe(el)});

// калькулятор
const NORM={glamp:1.7,base:1.7,hotel:1.7}; // млн ₽ на домик/номер — заменить нормами Юлии
const LABEL={glamp:'Домиков',base:'Домиков и номеров',hotel:'Номеров'};
const RANGE={glamp:[4,40,10],base:[6,60,16],hotel:[10,100,20]};
let fmt='glamp';
const range=document.getElementById('range'),units=document.getElementById('units'),sum=document.getElementById('sum'),ul=document.getElementById('unitLabel'),ticks=document.querySelector('.ticks');
function calc(){const n=+range.value;units.textContent=n;const v=n*NORM[fmt];sum.textContent='≈ '+(v<100?v.toFixed(0):Math.round(v/10)*10)+' млн ₽'}
function setFmt(k){fmt=k;const[a,b,c]=RANGE[k];range.min=a;range.max=b;range.value=c;ul.textContent=LABEL[k];ticks.innerHTML=`<span>${a}</span><span>${Math.round((a+b)/2)}</span><span>${b}</span>`;calc()}
if(range){
document.querySelectorAll('#fmt button').forEach(b=>b.onclick=()=>{document.querySelectorAll('#fmt button').forEach(x=>x.classList.remove('on'));b.classList.add('on');setFmt(b.dataset.k)});
range.oninput=calc;calc();
}

// квиз
const quiz=document.getElementById('quiz'),steps=[...quiz.querySelectorAll('.qstep')],bar=document.getElementById('qbar'),next=document.getElementById('qnext'),back=document.getElementById('qback'),nav=document.getElementById('qnav');
let s=0;
function show(i){s=i;steps.forEach((el,k)=>el.classList.toggle('on',k===i));bar.style.width=Math.min(100,(i+1)/6*100)+'%';back.style.visibility=i?'visible':'hidden';nav.style.display=i===6?'none':'flex';next.innerHTML=i===5?'Отправить <span class="arrow">→</span>':'Дальше <span class="arrow">→</span>'}
// data-quiz="1" — начать со второго вопроса (на странице услуги первый ответ уже известен)
document.querySelectorAll('[data-quiz]').forEach(b=>b.onclick=()=>{quiz.classList.add('open');show(+b.dataset.quiz||0)});
quiz.querySelector('.qclose').onclick=()=>quiz.classList.remove('open');
quiz.onclick=e=>{if(e.target===quiz)quiz.classList.remove('open')};
addEventListener('keydown',e=>{if(e.key==='Escape')quiz.classList.remove('open')});
quiz.querySelectorAll('.opts').forEach(g=>g.querySelectorAll('.opt').forEach(o=>o.onclick=()=>{g.querySelectorAll('.opt').forEach(x=>x.classList.remove('sel'));o.classList.add('sel');if(s<5)setTimeout(()=>show(s+1),280)}));
next.onclick=()=>show(Math.min(6,s+1));back.onclick=()=>show(Math.max(0,s-1));

// вкладки услуг: глэмпинги / отели
function openTab(k){document.querySelectorAll('.tabs button').forEach(b=>b.classList.toggle('on',b.dataset.tab===k));document.querySelectorAll('.tabpane').forEach(p=>{p.classList.toggle('on',p.dataset.pane===k);if(p.dataset.pane===k)p.querySelectorAll('.rv').forEach(el=>el.classList.add('in'))})}
document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>openTab(b.dataset.tab));
document.querySelectorAll('[data-go]').forEach(a=>a.addEventListener('click',()=>openTab(a.dataset.go)));
