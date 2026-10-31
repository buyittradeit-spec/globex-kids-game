#!/usr/bin/env python3
"""Build the Clanker Imposter Classroom Edition from the home version.
Usage: python3 build_classroom.py <src index.html> <three.min.js> <out.html>"""
import sys

src, three_path, out = sys.argv[1:4]
h = open(src, encoding='utf-8').read()
three = open(three_path, encoding='utf-8').read()


def rep(old, new, count=1):
    global h
    n = h.count(old)
    assert n == count, f'expected {count} of {old[:70]!r}, found {n}'
    h = h.replace(old, new)


# ---------- title, offline engine, separate saved settings ----------
rep('<title>Clanker Imposter — Globex Kids</title>',
    '<title>Clanker Imposter — Classroom Edition</title>')
rep('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>',
    '<script>/* three.js r128 — MIT License — Copyright © 2010-2021 three.js authors — https://threejs.org */\n'
    + three.replace('</script', '<\\/script') + '\n</script>')
rep("const SAVE_KEY = 'clankerImposter.settings.v1';",
    "const SAVE_KEY = 'clankerImposter.classroom.v1';")

# ---------- CSS: projector mode, round clock, report card, printing ----------
rep('  #problem { font-size: 52px; font-weight: 800; margin: 10px 0; }',
    '''  #problem { font-size: 52px; font-weight: 800; margin: 10px 0; }
  body.proj #problem { font-size: 84px; white-space: nowrap; } body.proj #quizQ { font-size: 84px !important; }
  body.proj #answer { font-size: 60px; min-height: 80px; width: 320px; }
  body.proj #nbScreen .panel, body.proj #quizScreen .panel { max-width: 720px !important; }
  body.proj .toast { font-size: 24px; }
  body.proj .pill { font-size: 20px; }
  body.proj #mtgScreen .panel, body.proj #endScreen .panel { zoom: 1.25; }
  #classHint { display: none; font-size: 22px; font-weight: 800; color: #ffcc33; margin-bottom: 6px; }
  body.proj #classHint { display: block; }
  #roundClock { display: none; }
  .tset { margin: 6px 0 4px; font-weight: 700; }
  .tset select { font: 700 16px 'Trebuchet MS'; border-radius: 10px; padding: 4px 8px; }
  #report { text-align: left; max-width: 560px; margin: 8px auto; font-size: 16px; }
  #report table { border-collapse: collapse; width: 100%; margin: 6px 0; }
  #report td, #report th { border: 1px solid rgba(255,255,255,.35); padding: 4px 8px; text-align: center; }
  #report .miss { columns: 2; font-size: 15px; }
  @media print {
    body * { visibility: hidden !important; }
    #report, #report * { visibility: visible !important; color: #000 !important; }
    #report { position: absolute; left: 0; top: 0; max-width: none; width: 100%; }
    #report td, #report th { border-color: #000; }
  }''')

# ---------- HUD round clock ----------
rep('  <div class="pill" id="pauseBtn" style="pointer-events:auto;cursor:pointer">⏸ Pause</div>',
    '  <div class="pill" id="roundClock">⏱ 10:00</div>\n'
    '  <div class="pill" id="pauseBtn" style="pointer-events:auto;cursor:pointer">⏸ Pause</div>')

# ---------- start screen: teacher settings ----------
rep('<div style="opacity:.85;margin-bottom:10px">A Globex Kids game, designed by kids! 🏭</div>',
    '<div style="opacity:.85;margin-bottom:4px">A Globex Kids game, designed by kids! 🏭</div>\n'
    '    <div style="color:#ffcc33;font-weight:800;margin-bottom:10px">🍎 CLASSROOM EDITION</div>')
rep('''      <div style="font-weight:700">Math in the notebooks:</div>''',
    '''      <div class="tset">📚 Grade level:
        <select id="gradeSel"><option value="2">2nd grade</option><option value="3" selected>3rd grade</option><option value="4">4th grade</option><option value="5">5th grade</option></select></div>
      <div style="font-weight:700">Math in the notebooks:</div>''')
rep('''    <div id="twoHelp" class="how"''',
    '''    <div style="background:rgba(255,255,255,.08);border-radius:12px;padding:6px 10px;margin:8px 0">
      <div style="font-weight:800;color:#ffcc33">🍎 Teacher settings</div>
      <div class="tset">⏱ Round length:
        <select id="roundSel"><option value="0">No limit</option><option value="5">5 minutes</option><option value="10" selected>10 minutes</option><option value="15">15 minutes</option><option value="20">20 minutes</option></select></div>
      <div class="tset">🎫 Hall passes &amp; detention:
        <select id="passSel"><option value="on" selected>On</option><option value="off">Off</option></select></div>
      <div class="tset">😠 Big Brock the bully:
        <select id="bullySel"><option value="on">On</option><option value="off" selected>Off</option></select></div>
      <label class="tset" style="display:block"><input type="checkbox" id="projChk"> 📽️ Projector mode: big text for the whole class</label>
    </div>
    <div id="twoHelp" class="how"''')
rep('<div class="credit">Version 1.3 · Globex Kids · All art, music and lyrics are original</div>',
    '<div class="credit">Classroom Edition 1.0 · Globex Kids · Works offline · All art, music and lyrics are original</div>')

# music defaults to Off in classrooms (first run only; saved choices win afterwards)
rep('''        <option>Country</option><option>Rock</option><option>Chill</option><option>Arcade</option><option>Off</option>
      </select>
      <label style="font-size:15px;margin-left:8px"><input type="checkbox" id="singChk">''',
    '''        <option>Country</option><option>Rock</option><option>Chill</option><option>Arcade</option><option selected>Off</option>
      </select>
      <label style="font-size:15px;margin-left:8px"><input type="checkbox" id="singChk">''')

# ---------- about screen ----------
rep('<li><b>No chat with strangers.</b>',
    '<li><b>Works offline.</b> This Classroom Edition never connects to the internet; it is one file that runs in any web browser.</li>\n      <li><b>No chat with strangers.</b>')

# ---------- notebook: projector hint + end-screen report ----------
rep('<div id="endSub" style="font-size:20px;margin:10px 0"></div>',
    '<div id="endSub" style="font-size:20px;margin:10px 0"></div>\n    <div id="report"></div>\n'
    '    <button class="btn gray" id="printBtn" style="font-size:16px;padding:8px 16px">🖨️ Print class report</button>')

# ---------- game setup ----------
rep("  G = { diff, twoP, humans, emCool: 12,",
    "  const grade = +$('gradeSel').value || 3, roundMin = +$('roundSel').value || 0;\n"
    "  G = { grade, timeLeft: roundMin * 60, roundMin, noPass: $('passSel').value === 'off', noBully: $('bullySel').value === 'off',\n"
    "    stats: { ops: { '+': [0, 0], '-': [0, 0], 'x': [0, 0], '/': [0, 0] }, missed: [], quizzes: [0, 0] },\n"
    "    diff, twoP, humans, emCool: 12,")
rep("  initExtras(); initItems(); initNerd();",
    "  initExtras(); initItems(); initNerd();\n"
    "  document.body.classList.toggle('proj', $('projChk').checked);\n"
    "  $('roundClock').style.display = G.timeLeft > 0 ? 'block' : 'none'; clockHud();")

# ---------- grade-level math ----------
rep('''function makeProblem() {
  const op = pick(G.ops); let a, b, r;
  if (op === '+') { a = randi(2, 30); b = randi(2, 20); r = a + b; }
  if (op === '-') { a = randi(5, 30); b = randi(1, a); r = a - b; }
  if (op === 'x') { a = randi(2, 10); b = randi(1, 5); if (Math.random() < .5) [a, b] = [b, a]; r = a * b; }
  if (op === '/') { b = randi(2, 5); r = randi(1, 10); a = b * r; if (Math.random() < .3) { b = randi(6, 10); r = randi(1, 5); a = b * r; } }
  const sym = { '+': '+', '-': '−', 'x': '×', '/': '÷' }[op];
  return { text: `${a} ${sym} ${b} = ?`, r };
}''',
    '''// Grade-level notebook problems (whole-number answers only)
//  2nd: add & subtract within 100, early multiplication (to 5 × 5) and division facts
//  3rd: add & subtract within 1,000, multiplication & division facts within 100
//  4th: add & subtract to 10,000, 2-digit × 1-digit, divide by 1 digit (no remainders)
//  5th: 2-digit × 2-digit, divide by 2 digits (no remainders), add & subtract to 100,000
const GRADE_MATH = {
  2: { '+': () => { const a = randi(10, 60), b = randi(5, 39); return [a, b, a + b]; },
       '-': () => { const a = randi(20, 99), b = randi(5, a); return [a, b, a - b]; },
       'x': () => { const a = randi(1, 5), b = randi(2, 5); return [a, b, a * b]; },
       '/': () => { const b = randi(2, 5), r = randi(1, 5); return [b * r, b, r]; } },
  3: { '+': () => { const a = randi(100, 599), b = randi(10, 399); return [a, b, a + b]; },
       '-': () => { const a = randi(100, 999), b = randi(10, a); return [a, b, a - b]; },
       'x': () => { const a = randi(2, 10), b = randi(2, 10); return [a, b, a * b]; },
       '/': () => { const b = randi(2, 10), r = randi(1, 10); return [b * r, b, r]; } },
  4: { '+': () => { const a = randi(1000, 5999), b = randi(100, 3999); return [a, b, a + b]; },
       '-': () => { const a = randi(1000, 9999), b = randi(100, a); return [a, b, a - b]; },
       'x': () => { const a = randi(12, 99), b = randi(2, 9); return [a, b, a * b]; },
       '/': () => { const b = randi(2, 9), r = randi(11, 99); return [b * r, b, r]; } },
  5: { '+': () => { const a = randi(10000, 59999), b = randi(1000, 39999); return [a, b, a + b]; },
       '-': () => { const a = randi(10000, 99999), b = randi(1000, a); return [a, b, a - b]; },
       'x': () => { const a = randi(12, 49), b = randi(11, 25); return [a, b, a * b]; },
       '/': () => { const b = randi(11, 25), r = randi(10, 60); return [b * r, b, r]; } },
};
// Theo's quick-fire quiz: fast facts at each grade
const GRADE_QUICK = {
  2: { '+': () => { const a = randi(1, 9), b = randi(1, 9); return [a, b, a + b]; }, '-': () => { const a = randi(5, 18), b = randi(1, Math.min(9, a)); return [a, b, a - b]; }, 'x': () => { const a = randi(1, 5), b = randi(1, 5); return [a, b, a * b]; } },
  3: { '+': () => { const a = randi(10, 50), b = randi(1, 9); return [a, b, a + b]; }, '-': () => { const a = randi(10, 50), b = randi(1, 9); return [a, b, a - b]; }, 'x': () => { const a = randi(2, 9), b = randi(2, 9); return [a, b, a * b]; }, '/': () => { const b = randi(2, 9), r = randi(1, 9); return [b * r, b, r]; } },
  4: { '+': () => { const a = randi(10, 90), b = randi(10, 90); return [a, b, a + b]; }, '-': () => { const a = randi(50, 99), b = randi(10, 49); return [a, b, a - b]; }, 'x': () => { const a = randi(2, 12), b = randi(2, 12); return [a, b, a * b]; }, '/': () => { const b = randi(2, 12), r = randi(2, 12); return [b * r, b, r]; } },
  5: { '+': () => { const a = randi(10, 90), b = randi(10, 90); return [a, b, a + b]; }, '-': () => { const a = randi(100, 199), b = randi(10, 99); return [a, b, a - b]; }, 'x': () => { const a = randi(3, 12), b = randi(3, 12); return [a, b, a * b]; }, '/': () => { const b = randi(3, 12), r = randi(3, 12); return [b * r, b, r]; } },
};
const OP_SYM = { '+': '+', '-': '−', 'x': '×', '/': '÷' };
const fmtN = n => n >= 10000 ? n.toLocaleString('en-US') : String(n);
function makeProblem() {
  const op = pick(G.ops), [a, b, r] = (GRADE_MATH[G.grade] || GRADE_MATH[3])[op]();
  return { text: `${fmtN(a)} ${OP_SYM[op]} ${fmtN(b)} = ?`, r, op };
}''')
rep('''function quickQ() {
  const ops = G.ops.filter(o => o !== '/'); const op = pick(ops.length ? ops : ['+']); let a, b, r;
  if (op === '+') { a = randi(1, 9); b = randi(1, 9); r = a + b; }
  if (op === '-') { a = randi(5, 15); b = randi(1, Math.min(9, a)); r = a - b; }
  if (op === 'x') { a = randi(2, 5); b = randi(1, 5); r = a * b; }
  return { text: `${a} ${{ '+': '+', '-': '−', 'x': '×' }[op]} ${b} = ?`, r };
}''',
    '''function quickQ() {
  const Q = GRADE_QUICK[G.grade] || GRADE_QUICK[3], ops = G.ops.filter(o => Q[o]), op = pick(ops.length ? ops : ['+']), [a, b, r] = Q[op]();
  return { text: `${a} ${OP_SYM[op]} ${b} = ?`, r, op };
}''')
rep("  else if (ans.length < 4) ans += k;", "  else if (ans.length < 6) ans += k;")
rep("  } else if (z.ans.length < 3) z.ans += k;", "  } else if (z.ans.length < 4) z.ans += k;")
rep("  $('problem').textContent = prob.text; $('answer').textContent = '';",
    "  $('problem').textContent = prob.text; $('answer').textContent = '';\n"
    "  $('problem').style.fontSize = prob.text.length > 13 ? (document.body.classList.contains('proj') ? '60px' : '34px') : '';\n"
    "  $('classHint').textContent = G.twoP ? '' : '📣 Class, what\\'s the answer?';")
rep('<div id="problem">7 + 5 = ?</div>', '<div id="classHint"></div>\n    <div id="problem">7 + 5 = ?</div>')

# ---------- record answers for the report ----------
rep('''  if (+ans === prob.r) {
    SFX.ding(); G.nbOpen.done = true;''',
    '''  const okA = +ans === prob.r; recordAns(prob, okA, ans);
  if (okA) {
    SFX.ding(); G.nbOpen.done = true;''')
rep('''    if (+z.ans === z.q.r) { z.got++;''',
    '''    recordAns(z.q, +z.ans === z.q.r, z.ans, true);
    if (+z.ans === z.q.r) { z.got++;''')

# ---------- hall passes / detention off ----------
rep('''      if (h.passT > 0) { t.say = pick(['Thanks! 👍', 'Walk, don\\'t run!', 'Carry on! 📋']); t.sayT = 2; continue; }''',
    '''      if (h.passT > 0 || G.noPass) { t.say = pick(['Thanks! 👍', 'Walk, don\\'t run!', 'Carry on! 📋', 'Good morning! 👋']); t.sayT = 2; continue; }''')
rep('''    n.say = "I'm telling the Principal! 📢"; n.sayT = 3;
    h.detCount++;''',
    '''    n.say = "I'm telling the Principal! 📢"; n.sayT = 3;
    if (G.noPass) { n.say = 'Study those facts! 📚'; toast('🤓 Theo: "Not quite! Keep practicing those facts!" 📚'); return; }
    h.detCount++;''')

# ---------- bully off ----------
rep('''  // ----- Big Brock -----
  const b = G.bully; b.sayT -= dt; b.cd -= dt;''',
    '''  // ----- Big Brock -----
  const b = G.bully; if (G.noBully) { b.x = -9000; b.y = -9000; b.path = []; return; }
  b.sayT -= dt; b.cd -= dt;''')

# ---------- round clock + end screen report ----------
rep('''function endGame(kidsWin, msg) {
  G.over = true; G.paused = true; $('huntWarn').style.display = 'none';
  $('endTitle').textContent = kidsWin ? '🏆 KIDS WIN!' : '🤖 THE CLANKER WINS!';''',
    '''function clockHud() { if (!G || !(G.roundMin > 0)) return; const s = Math.max(0, Math.ceil(G.timeLeft)); $('roundClock').textContent = `⏱ ${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`; $('roundClock').style.borderColor = s <= 60 ? '#e74c3c' : ''; }
function tickClock(dt) {
  if (!(G.roundMin > 0) || G.over) return;
  const before = Math.ceil(G.timeLeft); G.timeLeft -= dt; const s = Math.ceil(G.timeLeft);
  if (s !== before) { clockHud(); if (s === 60) toast('⏱ One minute left!'); }
  if (G.timeLeft <= 0) {
    const done = G.notebooks.filter(n => n.done).length, half = done >= G.notebooks.length / 2;
    endGame(half, `The class solved <b>${done}</b> of ${G.notebooks.length} notebooks${half ? ' — that beats the Clankers!' : '.'}<br>The Clanker${clankers().length > 1 ? 's were' : ' was'} ${clankerNames()}.`, "🔔 TIME'S UP!");
  }
}
function recordAns(q, ok, given, quiz) {
  if (!G || !G.stats || !q) return; const s = G.stats, o = s.ops[q.op];
  if (o) o[ok ? 0 : 1]++;
  if (quiz) s.quizzes[ok ? 0 : 1]++;
  if (!ok) s.missed.push(`${q.text.replace('?', q.r)} (said ${given})`);
}
function reportHTML() {
  const s = G.stats, names = { '+': '➕ Addition', '-': '➖ Subtraction', 'x': '✖️ Multiplication', '/': '➗ Division' };
  const done = G.notebooks.filter(n => n.done).length, mins = Math.max(1, Math.round(G.t / 60));
  let rows = '', tr = 0, tw = 0;
  for (const k of ['+', '-', 'x', '/']) { const [r, w] = s.ops[k]; tr += r; tw += w; if (r + w) rows += `<tr><td style="text-align:left">${names[k]}</td><td>${r}</td><td>${w}</td><td>${Math.round(100 * r / (r + w))}%</td></tr>`; }
  if (!rows) rows = '<tr><td colspan="4">No problems answered yet.</td></tr>';
  else rows += `<tr><th style="text-align:left">Total</th><th>${tr}</th><th>${tw}</th><th>${Math.round(100 * tr / (tr + tw))}%</th></tr>`;
  const miss = s.missed.slice(-16).map(m => `<div>• ${m}</div>`).join('');
  return `<div style="font-weight:800;font-size:18px">📋 Class Report · Clanker Imposter · Grade ${G.grade} · ${new Date().toLocaleDateString()}</div>
    <div>Notebooks solved: <b>${done} / ${G.notebooks.length}</b> · Time played: <b>${mins} min</b> · Theo's quick facts: ${s.quizzes[0]} right, ${s.quizzes[1]} missed</div>
    <table><tr><th style="text-align:left">Skill</th><th>Right</th><th>Missed</th><th>Score</th></tr>${rows}</table>
    ${miss ? `<div style="font-weight:700;margin-top:6px">Problems to review:</div><div class="miss">${miss}</div>` : '<div>⭐ No missed problems!</div>'}`;
}
function endGame(kidsWin, msg, title) {
  G.over = true; G.paused = true; $('huntWarn').style.display = 'none';
  $('endTitle').textContent = title || (kidsWin ? '🏆 KIDS WIN!' : '🤖 THE CLANKER WINS!');
  $('report').innerHTML = reportHTML();''')
rep("      updateTeachers(dt); updateSabotage(dt); updateItems(dt); updateNerd(dt);",
    "      updateTeachers(dt); updateSabotage(dt); updateItems(dt); updateNerd(dt); tickClock(dt);")

# ---------- remember the teacher settings; grade sets sensible default operations ----------
rep("const CHOICE_IDS = ['playersSel', 'kidsSel', 'diffSel', 'clankSel', 'musicSel'], CHECK_IDS = ['opAdd', 'opSub', 'opMul', 'opDiv', 'singChk'];",
    "const CHOICE_IDS = ['playersSel', 'kidsSel', 'diffSel', 'clankSel', 'musicSel', 'gradeSel', 'roundSel', 'passSel', 'bullySel'], CHECK_IDS = ['opAdd', 'opSub', 'opMul', 'opDiv', 'singChk', 'projChk'];\n"
    "$('gradeSel').addEventListener('change', () => { const g = +$('gradeSel').value; $('opAdd').checked = $('opSub').checked = true; $('opMul').checked = $('opDiv').checked = g >= 3; saveChoices(); });\n"
    "$('printBtn').onclick = () => window.print();")

open(out, 'w', encoding='utf-8').write(h)
print('wrote', out, len(h) // 1024, 'KB')
