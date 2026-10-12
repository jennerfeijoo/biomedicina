(() => {
  'use strict';
  const core = window.CitoAssessment, $ = id => document.getElementById(id);
  const root = new URL('../../', document.currentScript.src);
  const make = (tag, text, cls) => { const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(cls)e.className=cls;return e; };
  let index, questions=[], answers={}, ratings={}, current=0, course, scope, seed, loading=false;
  const params = new URLSearchParams(location.search);
  const names = {self_assessment:'Comprensión y razonamiento',common_errors:'Análisis de errores',worked_examples:'Caso aplicado',glossary:'Reconocimiento de conceptos'};
  async function json(file) { const url=new URL(file,root);url.searchParams.set('v',String(Date.now()));const r=await fetch(url,{cache:'no-store'});if(!r.ok)throw new Error(`No se pudo cargar el recurso (${r.status}).`);return r.json(); }
  function randomSeed(){return Array.from(crypto.getRandomValues(new Uint32Array(2)),n=>n.toString(36)).join('-');}
  function selectedCourse(){return index.courses.find(c=>c.id===$('exam-course').value);}
  function updateSummary(){
    const c=selectedCourse(), value=$('exam-scope').value;
    const units=value==='final'?c.units:c.units.filter(u=>String(u.unit)===value);
    const available=value==='final'?c.final_test_available:units[0]?.unit_test_available;
    $('bank-summary').textContent=available ? `${units.reduce((s,u)=>s+u.questions,0)} preguntas candidatas en el banco. Se seleccionarán ${value==='final'?50:15} sin repetición dentro del intento. Revisión disciplinar pendiente.` :
      'Evaluación pendiente: esta selección incluye contenido de plantilla o un banco insuficiente. Consulta la auditoría y las lecciones disponibles.';
    if(available && units.every(u=>u.reserved_objectives>0)) $('bank-summary').textContent+=` La selección reserva al menos una pregunta para cada uno de los ${units.reduce((s,u)=>s+u.reserved_objectives,0)} objetivos mapeados internamente. Esto no acredita dominio.`;
    $('exam-start').disabled=!available || loading;
  }
  function updateScopes(){
    const c=selectedCourse();$('exam-scope').replaceChildren();
    const final=make('option','Examen final · 50 preguntas');final.value='final';$('exam-scope').append(final);
    for(const u of c.units){const o=make('option',`Unidad ${u.unit}: ${u.title} · 15 preguntas${u.blocked?' · pendiente':''}`);o.value=String(u.unit);$('exam-scope').append(o);}
    if(params.get('unidad') && c.units.some(u=>String(u.unit)===params.get('unidad'))) $('exam-scope').value=params.get('unidad');
    updateSummary();
  }
  function status(message){$('exam-status').textContent=message;}
  function progress(){return Object.values(answers).filter(a=>String(a).trim()).length;}
  function showQuestion(){
    const host=$('exam-session');host.replaceChildren();host.hidden=false;
    const q=questions[current];
    const heading=make('h2',`${course.title} · ${scope==='final'?'Examen final':`Unidad ${scope}`}`);host.append(heading);
    const info=make('p',`Pregunta ${current+1} de ${questions.length} · ${progress()} respondidas · Código ${seed}`);host.append(info);
    const bar=make('progress');bar.max=questions.length;bar.value=progress();bar.setAttribute('aria-label','Preguntas respondidas');host.append(bar);
    const jumpLabel=make('label','Ir a pregunta');jumpLabel.htmlFor='exam-jump';const jump=make('select');jump.id='exam-jump';
    questions.forEach((x,i)=>{const o=make('option',`${i+1}. Unidad ${x.unit}${answers[x.id]?.trim()?' · respondida':''}`);o.value=i;jump.append(o);});jump.value=current;
    jump.onchange=()=>{current=Number(jump.value);showQuestion();};host.append(jumpLabel,jump);
    const field=make('fieldset',undefined,'exam-question');const legend=make('legend',q.prompt);field.append(legend);
    field.append(make('p',`Unidad ${q.unit}: ${q.unitTitle} · ${names[q.kind]}`));
    if(q.options){
      q.options.forEach((option,i)=>{const label=make('label',undefined,'exam-option');const input=make('input');input.type='radio';input.name='answer';input.value=option;input.checked=answers[q.id]===option;input.onchange=()=>{answers[q.id]=option;info.textContent=`Pregunta ${current+1} de ${questions.length} · ${progress()} respondidas · Código ${seed}`;bar.value=progress();};label.append(input,make('span',option));field.append(label);});
    }else{
      const label=make('label','Tu respuesta y razonamiento');label.htmlFor='open-answer';const input=make('textarea');input.id='open-answer';input.value=answers[q.id]||'';input.oninput=()=>{answers[q.id]=input.value;bar.value=progress();info.textContent=`Pregunta ${current+1} de ${questions.length} · ${progress()} respondidas · Código ${seed}`;};field.append(label,input);
      field.append(make('small','Al finalizar podrás comparar tu respuesta con la solución orientativa. No se calificará automáticamente este texto.'));
    }
    host.append(field);
    const previous=make('button','Anterior');previous.disabled=current===0;previous.onclick=()=>{current--;showQuestion();};
    const next=make('button','Siguiente');next.disabled=current===questions.length-1;next.onclick=()=>{current++;showQuestion();};
    const finish=make('button','Finalizar y revisar');finish.onclick=finishExam;host.append(previous,next,finish);
    legend.tabIndex=-1;legend.focus({preventScroll:true});
  }
  function summaryText(){
    const objective=questions.filter(q=>q.options), open=questions.filter(q=>!q.options);
    const correct=objective.filter(q=>answers[q.id]===q.answer).length;
    const rated=open.filter(q=>answers[q.id]?.trim() && ratings[q.id]!==undefined);
    return `Corrección automática (reconocimiento): ${correct}/${objective.length}. Respuestas abiertas: ${rated.length}/${open.length} autoevaluadas${rated.length?`; ${rated.reduce((s,q)=>s+ratings[q.id],0)}/${rated.length*2} puntos autoasignados`:''}. Sin responder: ${questions.length-progress()}. Estas medidas no equivalen entre sí ni certifican dominio.`;
  }
  function finishExam(){
    $('exam-session').hidden=true;const host=$('exam-results');host.replaceChildren();host.hidden=false;
    const title=make('h2','Resultados y plan de repaso');title.tabIndex=-1;host.append(title);
    const score=make('p',summaryText());score.id='exam-score';score.setAttribute('aria-live','polite');host.append(score);
    host.append(make('p','Rúbrica para respuestas abiertas: 0 = ausente o incorrecta; 1 = parcialmente correcta o sin justificación suficiente; 2 = correcta, razonada y con los supuestos o límites pertinentes. La solución es orientativa: pueden existir otras formulaciones válidas.'));
    const table=make('table');table.innerHTML='<thead><tr><th scope="col">Unidad</th><th scope="col">Preguntas</th><th scope="col">Respondidas</th></tr></thead>';
    const body=make('tbody');for(const u of [...new Set(questions.map(q=>q.unit))].sort((a,b)=>a-b)){const qs=questions.filter(q=>q.unit===u), tr=make('tr');tr.append(make('th',`U${u}`),make('td',String(qs.length)),make('td',String(qs.filter(q=>answers[q.id]?.trim()).length)));body.append(tr);}table.append(body);host.append(table);
    questions.forEach((q,i)=>{
      const box=make('article',undefined,'exam-review');box.append(make('h3',`${i+1}. ${q.prompt}`));
      box.append(make('p',`Tu respuesta: ${answers[q.id]||'Sin respuesta'}`,'exam-feedback'));
      if(q.options)box.append(make('strong',answers[q.id]===q.answer?'Correcta':'Revisar'));
      box.append(make('p',`Solución orientativa: ${q.answer}`,'exam-feedback'),make('p',q.explanation,'exam-feedback'));
      const link=make('a',`Repasar unidad ${q.unit}`);link.href=new URL(`${course.path.replace(/index\.html$/,'')}unidades/unidad-${String(q.unit).padStart(2,'0')}.html#teoria`,root);box.append(link);
      if(!q.options){const label=make('label','Autoevaluación con la rúbrica');label.htmlFor=`rate-${i}`;const select=make('select');select.id=`rate-${i}`;
        for(const [value,text]of [['','Sin evaluar'],['0','0 · Ausente o incorrecta'],['1','1 · Parcial o sin justificación'],['2','2 · Correcta y justificada']]){const option=make('option',text);option.value=value;select.append(option);}
        if(!answers[q.id]?.trim()){select.value='';select.disabled=true;label.textContent='Sin respuesta · no autoevaluada';}
        select.onchange=()=>{if(select.value==='')delete ratings[q.id];else ratings[q.id]=Number(select.value);score.textContent=summaryText();};box.append(label,select);
      }
      host.append(box);
    });
    score.textContent=summaryText();
    const again=make('button','Nuevo intento (borra las respuestas)');again.onclick=()=>{$('exam-seed').value=randomSeed();host.hidden=true;questions=[];answers={};ratings={};$('exam-setup').hidden=false;status('Elige la evaluación y comienza un nuevo intento.');$('exam-course').focus();};host.append(again);
    status('Intento finalizado. Revisa los errores y vuelve a las unidades que necesitan refuerzo.');title.focus();
  }
  $('exam-setup').onsubmit=async event=>{
    event.preventDefault();if(loading)return;loading=true;updateSummary();status('Preparando la selección de preguntas…');
    try{
      course=selectedCourse();scope=$('exam-scope').value;seed=$('exam-seed').value.trim()||randomSeed();$('exam-seed').value=seed;
      const units=scope==='final'?course.units:course.units.filter(u=>String(u.unit)===scope);
      const banks=await Promise.all(units.map(async u=>{
        const sourceUrl=new URL(u.source,root);sourceUrl.searchParams.set('sha256',u.sha256);
        const response=await fetch(sourceUrl);if(!response.ok)throw new Error('No se pudo cargar una unidad. Inténtalo de nuevo.');
        const buffer=await response.arrayBuffer();const hash=[...new Uint8Array(await crypto.subtle.digest('SHA-256',buffer))].map(n=>n.toString(16).padStart(2,'0')).join('');
        if(hash!==u.sha256)throw new Error('El contenido ha cambiado y el banco debe actualizarse. No se generará un examen con versiones mezcladas.');
        return core.buildBank(JSON.parse(new TextDecoder().decode(buffer)));
      }));
      questions=core.select(banks,scope==='final'?50:15,seed);answers={};ratings={};current=0;
      $('exam-setup').hidden=true;$('exam-results').hidden=true;showQuestion();status('Responde antes de finalizar. Las soluciones se mostrarán al terminar.');
    }catch(e){status(e.message);}
    finally{loading=false;updateSummary();}
  };
  json('data/learning-audit/banks.json').then(data=>{
    index=data;$('exam-course').replaceChildren();
    for(const c of index.courses){const o=make('option',`${c.title}${c.final_test_available?'':' · final pendiente'}`);o.value=c.id;$('exam-course').append(o);}
    if(index.courses.some(c=>c.id===params.get('asignatura')))$('exam-course').value=params.get('asignatura');
    $('exam-course').onchange=updateScopes;$('exam-scope').onchange=updateSummary;updateScopes();$('exam-seed').value=randomSeed();
    const units=index.courses.flatMap(c=>c.units);$('audit-summary').textContent=`${index.courses.length} asignaturas · ${units.length} unidades auditadas. ${index.courses.filter(c=>c.final_test_available).length} finales disponibles para práctica; ${units.filter(u=>u.blocked).length} unidades con contenido de plantilla pendientes de reescritura.`;
  }).catch(e=>status(`No se pudieron preparar los bancos. ${e.message}`));
})();
