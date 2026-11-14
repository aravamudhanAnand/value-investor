/* Value Investor — static site. Data lives in data/*.json, the rulebook in framework/value-investor.md. */
(() => {
  const $ = (id) => document.getElementById(id);
  const esc = (s) => String(s ?? '—').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const money = (n, d = 2) => (n === null || n === undefined) ? '—' : '$' + Number(n).toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d });
  const bn = (m) => { if (m === null || m === undefined) return '—'; const a = Math.abs(m), s = m < 0 ? '−' : ''; return a >= 1e6 ? `${s}$${(a / 1e6).toFixed(2)}T` : a >= 1e3 ? `${s}$${(a / 1e3).toFixed(1)}B` : `${s}$${a.toFixed(0)}M`; };
  const VERDICT = { BUY_ZONE: 'Buy zone', WATCHLIST: 'Watchlist', TOO_HARD: 'Too hard', PASS: 'Pass' };
  const SHAPE = { BUY_ZONE: '▲', WATCHLIST: '◆', TOO_HARD: '?', PASS: '✕' };
  const C = { ink: '#14211c', ink2: '#3d4a44', muted: '#66736d', grid: '#ece6d8', line: '#e4ddcd', surface: '#fffdf8', accent: '#0f5a44', buy: '#15824a', watch: '#c27a1a', pass: '#b03a2e' };
  const VCOLOR = { BUY_ZONE: C.buy, WATCHLIST: C.watch, PASS: C.pass };
  const BUY_LINE = 1 / 0.7; // value per $1 that gives a 30% margin of safety
  const NS = 'http://www.w3.org/2000/svg';

  let INDEX = null, filter = 'ALL';
  const cache = {};

  /* ---------- tooltip ---------- */
  const tip = $('tip');
  function showTip(e, html) { tip.innerHTML = html; tip.style.opacity = 1; moveTip(e); }
  function moveTip(e) {
    const x = Math.min(e.clientX + 14, window.innerWidth - tip.offsetWidth - 8);
    const y = e.clientY + 16 + tip.offsetHeight > window.innerHeight ? e.clientY - tip.offsetHeight - 12 : e.clientY + 16;
    tip.style.left = x + 'px'; tip.style.top = y + 'px';
  }
  function hideTip() { tip.style.opacity = 0; }
  function bindTips(root) {
    root.querySelectorAll('[data-tip]').forEach((el) => {
      el.addEventListener('mouseenter', (e) => showTip(e, el.dataset.tip));
      el.addEventListener('mousemove', moveTip);
      el.addEventListener('mouseleave', hideTip);
      el.addEventListener('focus', () => { const r = el.getBoundingClientRect(); showTip({ clientX: r.right, clientY: r.top }, el.dataset.tip); });
      el.addEventListener('blur', hideTip);
    });
  }
  const tipAttr = (html) => `data-tip="${esc(html)}" tabindex="0"`;

  /* ---------- routing ---------- */
  let animateNext = false;
  async function route() {
    hideTip();
    const h = decodeURIComponent(location.hash.slice(1));
    if (!INDEX) INDEX = await (await fetch('data/index.json')).json();
    $('foot-asof').textContent = `Data as of ${INDEX.as_of} · Framework v${INDEX.framework_version}`;
    fillPicker();
    const isMethod = h === 'methodology';
    $('view-home').hidden = isMethod; $('view-method').hidden = !isMethod;
    $('nav-lib').classList.toggle('on', !isMethod); $('nav-method').classList.toggle('on', isMethod);
    if (isMethod) return renderMethod();
    const hit = INDEX.companies.find((c) => c.slug.toLowerCase() === h.toLowerCase());
    $('pick').value = hit ? hit.slug : '';
    $('intro').hidden = !!hit;
    if (!hit) { $('report').innerHTML = ''; document.title = 'Value Investor — business quality and fair value'; return; }
    const animate = animateNext; animateNext = false;
    await renderReport(hit.slug, animate);
  }

  /* ---------- picker ---------- */
  function fillPicker() {
    const p = $('pick');
    if (p.options.length > 1) return;
    const cs = INDEX.companies;
    p.options[0].textContent = `Select one of ${cs.length} companies…`;
    const sectors = [...new Set(cs.map((c) => c.sector))].sort();
    sectors.forEach((sec) => {
      const g = document.createElement('optgroup'); g.label = sec;
      cs.filter((c) => c.sector === sec).sort((x, y) => x.company.localeCompare(y.company)).forEach((c) => {
        const o = document.createElement('option'); o.value = c.slug; o.textContent = `${c.company} (${c.ticker})`; g.appendChild(o);
      });
      p.appendChild(g);
    });
    const n = (v) => cs.filter((c) => c.verdict === v).length;
  }
  $('pick').addEventListener('change', (e) => {
    animateNext = true;
    location.hash = e.target.value || '';
  });

  /* ---------- the assessment run-through ---------- */
  const STEPS = ['Meaning: understanding the business', 'Moat: testing the competitive advantage', 'Industry: checking the pace of change',
    'Management: reviewing the record', 'Financial health: nine checks and the ratio sheet', 'Fair value: owner cash flow and Damodaran', 'Rules of the road: final screen', 'Checklists: Graham, Buffett, Lynch, Munger, Pabrai'];
  function runThrough(name) {
    const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce) return Promise.resolve();
    const el = $('report');
    el.innerHTML = `<div class="card run"><p class="run-title">Assessing ${esc(name)} with the Value Investor framework</p>
      <ol>${STEPS.map((s, i) => `<li id="st${i}">${esc(s)}</li>`).join('')}</ol></div>`;
    return new Promise((done) => {
      let i = 0;
      const tick = () => {
        if (i > 0) $('st' + (i - 1)).className = 'done';
        if (i < STEPS.length) { $('st' + i).className = 'now'; i++; setTimeout(tick, 210); } else setTimeout(done, 180);
      };
      tick();
    });
  }

  /* ---------- report ---------- */
  const MASTERS = [
    ['graham', 'Benjamin Graham', 'The defensive investor', 'Is it statistically cheap and financially safe?'],
    ['buffett', 'Warren Buffett', 'Owner economics', 'Would you want to own the whole business for its cash?'],
    ['lynch', 'Peter Lynch', 'Know what you own', 'What kind of stock is it, and is the growth worth the price?'],
    ['munger', 'Charlie Munger', 'Inversion and incentives', 'What could kill it, and are insiders on your side?'],
    ['pabrai', 'Mohnish Pabrai', 'Dhandho', 'Heads I win, tails I don\'t lose much.'],
  ];
  const ratioRes = (p) => `<span class="res res-${p}">${p === true ? 'Meets' : p === false ? 'Misses' : 'Reference'}</span>`;
  const res = (p) => `<span class="res res-${p}">${p === true ? 'Pass' : p === false ? 'Fail' : 'n/a'}</span>`;

  const EMBLEM = {"graham": "<svg viewBox=\"0 0 24 24\" aria-hidden=\"true\"><path d=\"M12 4v16M7 20h10M5 7h14\"/><path d=\"M5 7l-3 7a3 3 0 0 0 6 0zM19 7l-3 7a3 3 0 0 0 6 0z\"/></svg>", "buffett": "<svg viewBox=\"0 0 24 24\" aria-hidden=\"true\"><path d=\"M5 14V5h3v2h2.5V5h3v2H16V5h3v9\"/><path d=\"M5 14h14\"/><path d=\"M10 14v-3a2 2 0 0 1 4 0v3\"/><path d=\"M2 18c1.7-1.3 3.3-1.3 5 0s3.3 1.3 5 0 3.3-1.3 5 0 3.3 1.3 5 0\"/></svg>", "lynch": "<svg viewBox=\"0 0 24 24\" aria-hidden=\"true\"><circle cx=\"10.5\" cy=\"10.5\" r=\"6\"/><path d=\"M15 15l6 6\"/><path d=\"M8 11.5l2-2 1.5 1.5L14 8.5\"/></svg>", "munger": "<svg viewBox=\"0 0 24 24\" aria-hidden=\"true\"><path d=\"M8 20V5M4.5 8.5L8 5l3.5 3.5\"/><path d=\"M16 4v15M12.5 15.5L16 19l3.5-3.5\"/></svg>", "pabrai": "<svg viewBox=\"0 0 24 24\" aria-hidden=\"true\"><circle cx=\"12\" cy=\"12\" r=\"8.5\"/><path d=\"M14.6 9.3c-.5-.9-1.4-1.4-2.6-1.4-1.6 0-2.7.8-2.7 2 0 2.9 5.5 1.3 5.5 4.200 0 1.200-1.200 2-2.800 2-1.300 0-2.300-.6-2.800-1.500M12 6v1.900M12 16.100V18\"/></svg>"};
  function lensCard([k, name, tag, question], L) {
    const l = L[k];
    return `<div class="card" id="lens-${k}"><h3><span><i class="m-ico inl">${EMBLEM[k]}</i>${name}</span><small>${l.passed} of ${l.total} passed</small></h3>
      <p class="h3-sub">${tag}: ${esc(question)}</p>
      ${l.category ? `<p class="lynch-cat"><span class="tag">${esc(l.category)}</span>${esc(l.category_note)}</p>` : ''}
      <details class="fold"><summary>Show the ${l.tests.length} tests</summary><table class="lens-table"><tbody>${l.tests.map((t) => `<tr><td class="lt-res">${t.pass === null ? '<span class="res res-null">No call</span>' : res(t.pass)}</td><td><b>${esc(t.name)}</b><div class="meta">${esc(t.threshold)}</div></td><td>${esc(t.value)}</td></tr>`).join('')}</tbody></table></details>
      ${k === 'munger' ? `<h4>Inversion: what could kill this business?</h4><ul>${l.inversion.map((x) => `<li>${esc(x)}</li>`).join('')}</ul>` : ''}</div>`;
  }

  async function renderReport(slug, animate) {
    const el = $('report');
    const meta = INDEX.companies.find((c) => c.slug === slug);
    const load = cache[slug] ? Promise.resolve(cache[slug]) : fetch(`data/companies/${slug}.json`).then((r) => r.json());
    const [d] = await Promise.all([load, animate ? runThrough(meta.company) : Promise.resolve()]);
    cache[slug] = d;
    if (location.hash.slice(1) !== slug) return; // user picked another company meanwhile
    const v = d.valuation, f = d.financial_health, m = d.meaning, t = v.three_numbers, L = d.lenses;
    const su = d.summary, pf = d.profile;
    document.title = `${d.company} (${d.ticker}) — Value Investor`;
    const block = (num, title, sub, score, body) => `<div class="card"><h3><span><span class="mnum">${num}</span>${esc(title)}</span><small>${score === null ? '' : score + ' / 10'}</small></h3>${sub ? `<p class="h3-sub">${esc(sub)}</p>` : ''}${body}</div>`;
    const list = (a) => (a && a.length ? '<ul>' + a.map((x) => `<li>${esc(x)}</li>`).join('') + '</ul>' : '<p class="meta">None noted.</p>');
    const hasIv = v.intrinsic_value_low !== null;
    const ivMid = hasIv ? (v.intrinsic_value_low + v.intrinsic_value_high) / 2 : null;

    el.innerHTML = `
      <div class="card" id="sec-1">
        <div class="head2">
          <div>
            <span class="verdict lg v-${d.verdict}">${VERDICT[d.verdict]}</span>
            <h2>${esc(d.company)}</h2>
            <div class="sub">${esc(d.ticker)} · ${esc(d.exchange)} · ${esc(d.sector)} · ${money(d.price)} (close ${esc(d.price_date)}) · Market cap ${esc(d.market_cap)}</div>
          </div>
          <div class="big-score"><b>${d.overall_score}</b><span>/ 100<br>overall</span></div>
        </div>
        <p class="kicker"><span class="snum">01</span>${esc(d.company)} in one sentence</p>
        <p class="sentence">${esc(su.sentence)}</p>
        <p class="lede">${esc(d.one_liner)}</p>
        <div class="three">
          <div class="tri tri-good"><h4>Strengths</h4>${list(su.strengths)}</div>
          <div class="tri tri-risk"><h4>Risks</h4>${list(su.risks)}</div>
          <div class="tri tri-swing"><h4>Swing factors</h4>${list(su.swing)}<p class="meta">What is most likely to change the verdict.</p></div>
        </div>
      </div>
      <nav class="secnav" aria-label="Report sections">${[[2, 'What it is'], [3, 'How it makes money'], [4, 'Durability'], [5, 'The numbers'], [6, 'How it is valued'], [7, 'Fair value'], [8, 'Bull and bear'], [9, 'Second opinions']].map(([n, t]) => `<button type="button" data-goto="sec-${n}"><b>0${n}</b> ${t}</button>`).join('')}</nav>

      <div class="section-title" id="sec-2"><span class="snum">02</span>What ${esc(d.company)} is<small></small></div>
      <div class="card"><p class="plain">${esc(pf.what)}</p></div>

      <div class="section-title" id="sec-3"><span class="snum">03</span>How it makes money<small></small></div>
      <div class="card"><p class="plain">${esc(pf.money)}</p>
        ${dollarBar(d)}
      </div>

      <div class="section-title" id="sec-4"><span class="snum">04</span>Can it keep making money?<small>Moat, industry and management</small></div>
      <div class="card"><h3><span><span class="mnum">M1</span>Meaning</span><small>${m.score} / 10</small></h3>
        <dl><dt>How will it keep making money?</dt><dd>${esc(m.how_it_keeps_making_money)}</dd><dt>How could it stop making money?</dt><dd>${esc(m.how_it_could_stop)}</dd></dl></div>
      ${block('M2', 'Moat', 'Is the competitive advantage durable, and is the industry stable?', d.moat.score, `
        <span class="tag">${esc(d.moat.strength)} moat</span>${d.moat.sources.map((s) => `<span class="tag">${esc(s)}</span>`).join('')}
        <p>${esc(d.moat.summary)}</p>
        <h4>Industry stability · ${d.industry.score} / 10</h4><span class="tag">${esc(d.industry.pace)}</span><p>${esc(d.industry.summary)}</p>`)}
      ${block('M3', 'Management', 'Integrity, intelligence and energy, judged from the record', d.management.score, `<p>${esc(d.management.summary)}</p>`)}
      ${block('', 'Value 3.0 rules of the road', 'The dos and don\'ts that keep you out of value traps', null, `
        <table><tbody>${d.rules_of_the_road.map((r) => `<tr><td style="width:34%">${esc(r.name)}</td><td style="width:90px">${r.pass === null ? '<span class="res res-null">Unclear</span>' : res(r.pass)}</td><td>${esc(r.value)}</td></tr>`).join('')}</tbody></table>`)}

      
      <div class="section-title" id="sec-5"><span class="snum">05</span>The numbers<small>Five-year record, financial health and where the cash goes</small></div>
      ${block('', 'Free cash flow & financial health', 'Nine checks on the income statement, balance sheet and cash flow statement', f.score, `
        <div class="minis">${mini(f.history, 'revenue', 'Revenue')}${mini(f.history, 'net_income', 'Net income')}${mini(f.history, 'fcf', 'Free cash flow')}</div>
        <table><thead><tr><th>Check</th><th>Result</th><th>Value</th><th>Target</th></tr></thead><tbody>
        ${f.checks.map((c) => `<tr><td>${esc(c.name)}</td><td>${res(c.pass)}</td><td>${esc(c.value)}</td><td>${esc(c.threshold)}</td></tr>`).join('')}
        </tbody></table>
        ${cashUse(d)}
        ${f.red_flags.length ? `<h4>Red flags</h4><div class="flags">${list(f.red_flags)}</div>` : ''}
        ${f.note ? `<div class="note">${esc(f.note)}</div>` : ''}`)}
      ${block('', 'Ratio sheet', f.ratios.length ? `${f.ratio_summary.passed} of ${f.ratio_summary.total} yardsticks met. The yardsticks describe a strong business; they are not pass-or-fail rules.` : '', null, `<details class="fold"><summary>Show the full ratio sheet</summary>
        ${f.ratios.length ? `<div style="overflow-x:auto"><table class="ratio-table"><thead><tr><th>Ratio</th><th>Value</th><th class="ys-d">Yardstick</th><th>Result</th></tr></thead><tbody>
        ${f.ratios.map((g) => `<tr class="grp"><th colspan="4" scope="colgroup">${esc(g.group)}</th></tr>` + g.rows.map((r) => `<tr><td>${esc(r.name)}<div class="meta ys-m">${esc(r.threshold)}</div></td><td class="rv">${esc(r.value)}</td><td class="meta ys-d">${esc(r.threshold)}</td><td>${ratioRes(r.pass)}</td></tr>`).join('')).join('')}
        </tbody></table></div>` : ''}
        <div class="note">${esc(f.ratio_gaps)}</div></details>`)}
      
      <div class="section-title" id="sec-6"><span class="snum">06</span>How the stock is valued<small></small></div>
      ${briefCard(d)}
      <div class="card"><h3><span><span class="mnum">M4</span>Margin of safety</span><small>${v.score} / 10</small></h3>
        <p class="verdict-title" style="margin-top:6px">${esc(valueTitle(d))}</p>
        <h4>Valuation for its lifecycle stage</h4>
        <span class="tag">Stage ${esc(v.lifecycle_stage)}</span>
        <div class="nums">
          <div class="stat"><span>${esc(v.primary_metric.name)} (primary)</span><b>${esc(v.primary_metric.value)}</b></div>
          <div class="stat"><span>${esc(v.secondary_metric.name)} (secondary)</span><b>${esc(v.secondary_metric.value)}</b></div>
          <div class="stat"><span>P/E</span><b>${t.pe ?? '—'}</b></div>
          <div class="stat"><span>Forward P/E</span><b>${t.forward_pe ?? '—'}</b></div>
          <div class="stat"><span>PEG</span><b>${t.peg ?? '—'}</b></div>
        </div>
        <div style="overflow-x:auto"><table><thead><tr><th>Multiple</th>${v.multiples.map((x) => `<th>${esc(x.name)}</th>`).join('')}</tr></thead>
        <tbody><tr><td>Value</td>${v.multiples.map((x) => `<td class="num">${esc(x.value)}</td>`).join('')}</tr></tbody></table></div>
</div>

      <div class="section-title" id="sec-7"><span class="snum">07</span>Fair value<small></small></div>
      ${fairValueCard(d)}

      <div class="section-title" id="sec-8"><span class="snum">08</span>Bull case and bear case<small></small></div>
      <div class="two">
        <div class="card case case-bull"><h3>Bull case</h3>${caseTiles(d, true)}${list(d.bull_case)}</div>
        <div class="card case case-bear"><h3>Bear case</h3>${caseTiles(d, false)}${list(d.bear_case)}</div>
      </div>

      <div class="section-title" id="sec-9"><span class="snum">09</span>Second opinions<small>The scorecard and five investors' checklists</small></div>
      <div class="card compass">
        <h3><span>The compass</span><small>scores out of 10</small></h3>
        <div class="compass-grid">
          <div>
            ${radar(d.scores)}
            <div class="legend compass-legend">
              <span><i class="sw sw-co"></i>${esc(d.ticker)}</span>
              <span><i class="sw sw-med"></i>Median of ${INDEX.companies.length}</span>
              <span><i class="sw sw-bar"></i>7 bar: wonderful-business standard</span>
              <span><i class="sw sw-price"></i>Price pillar</span>
            </div>
          </div>
          <div class="shape">${readShape(d)}</div>
        </div>
      </div>

      <h4 class="sub-title">Five investors' checklists</h4>
      <p class="section-sub">The same company against the published tests of Graham, Buffett, Lynch, Munger and Pabrai. Each test is calculated from the figures; "No call" means the test does not apply, the data was unavailable, or the result sits between pass and fail. Bonds are measured against a 10-year Treasury yield of ${d.treasury_10y.toFixed(2)}%.</p>
      <div class="two lenses">${MASTERS.map((mm) => lensCard(mm, L)).join('')}</div>

      <div class="card sources"><h3>Sources</h3><ul>${d.sources.map((s) => `<li><a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer">${esc(s.title)}</a></li>`).join('')}</ul>
        <p class="meta">Figures collected ${esc(d.as_of)}. Framework v${esc(d.framework_version)}. Meaning, moat, industry, management and the growth assumption are analyst judgment; everything else is calculated by the rules on the <a href="#methodology">Methodology</a> page.</p></div>`;
    bindTips(el);
    el.querySelectorAll('[data-goto]').forEach((b) => b.addEventListener('click', () => document.getElementById(b.dataset.goto).scrollIntoView({ behavior: 'smooth', block: 'start' })));
    if (animate) $('picker-card').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function analystLine(d) {
    const m = d.market, fv = d.valuation.fair_value;
    if (!m || !m.target) return '';
    const pp = m.target_vs_price, side = pp >= 0 ? `${Math.round(pp)}% above` : `${Math.round(-pp)}% below`;
    const vsFair = fv ? ` That is ${m.target_vs_fair >= 0 ? `${Math.round(m.target_vs_fair)}% above` : `${Math.round(-m.target_vs_fair)}% below`} this site's fair value: analysts' targets usually assume today's multiples hold, while fair value here rests only on cash the business is expected to produce.` : '';
    return `<p class="analyst">Wall Street's view: the analysts' average price target is <b>${money(m.target, 0)}</b>, ${side} the price, with a consensus rating of <b>${esc(m.rating || 'n/a')}</b> (as of ${esc(m.as_of)}).${vsFair}</p>`;
  }

  /* Peer bars: the company's main multiple against its peer group, ranked, with the median marked */
  function peerBars(d) {
    const p = d.profile, k = p.metrics[0], peers = p.peers || [];
    if (!peers.length || k.value === null) return '';
    const unit = k.unit === '%' ? '%' : 'x', f = (v) => k.unit === '%' ? `${v.toFixed(1)}%` : `${v.toFixed(1)}x`;
    const vals = peers.map((r) => r.value), sv = vals.slice().sort((a, b) => a - b), h = sv.length / 2;
    const medV = sv.length % 2 ? sv[Math.floor(h)] : (sv[h - 1] + sv[h]) / 2;
    const rank = peers.findIndex((r) => r.ticker === d.ticker) + 1, n = peers.length;
    const sfx = (i) => { const a = i % 10, b = i % 100; return b >= 11 && b <= 13 ? 'th' : a === 1 ? 'st' : a === 2 ? 'nd' : a === 3 ? 'rd' : 'th'; };
    const ord = (i) => i === 1 ? 'the highest' : i === n ? 'the lowest' : `the ${i}${sfx(i)} highest`;
    const head = !rank ? '' : Math.abs(k.value - medV) < 0.05 ? `${d.company} trades at ${f(k.value)} ${k.label.toLowerCase()}, right at the median of ${n} peers.` : `${d.company} trades at ${f(k.value)} ${k.label.toLowerCase()}, ${ord(rank)} of ${n}; the peer median is ${f(medV)}.`;
    const W = 560, row = 22, L = 60, R = 62, top = 8, H = top + n * row + 22, max = Math.max(...vals) * 1.02;
    const x = (v) => L + v / max * (W - L - R);
    let svg = `<svg viewBox="0 0 ${W} ${H}" width="100%" role="img" aria-label="${esc(head)}">`;
    peers.forEach((r, i) => {
      const y = top + i * row, me = r.ticker === d.ticker;
      svg += `<g ${tipAttr(`<b>${esc(r.company)}</b><br>${esc(k.label)}: ${f(r.value)}`)}><rect class="hit" x="0" y="${y}" width="${W}" height="${row}" fill="transparent"/>
        <text x="${L - 8}" y="${y + 15}" text-anchor="end" font-size="12" ${me ? `font-weight="700" fill="${C.ink}"` : `fill="${C.muted}"`}>${esc(r.ticker)}</text>
        <rect x="${L}" y="${y + 4}" width="${Math.max(2, x(r.value) - L)}" height="${row - 8}" rx="3" fill="${me ? C.accent : '#cfd8d3'}"/>
        <text x="${x(r.value) + 6}" y="${y + 15}" font-size="12" ${me ? `font-weight="700" fill="${C.ink}"` : `fill="${C.ink2}"`}>${f(r.value)}</text></g>`;
    });
    const mx = x(medV);
    svg += `<line x1="${mx}" x2="${mx}" y1="${top - 2}" y2="${top + n * row}" stroke="${C.ink}" stroke-width="1.5" stroke-dasharray="4 3"/>
      <text x="${mx}" y="${top + n * row + 15}" text-anchor="middle" font-size="11.5" fill="${C.ink2}">Median ${f(medV)}</text></svg>`;
    return `<div class="viz-block"><p class="viz-head">${esc(head)}</p><p class="meta">${esc(k.label)} across ${esc(p.peer_group.toLowerCase())} companies on this site</p>${svg}</div>`;
  }

  /* 52-week range: where today's price sits between the year's low and high */
  function rangeBar(d) {
    const m = d.market;
    if (!m || m.low52 === null || m.high52 === null) return '';
    const lo = m.low52, hi = m.high52, p = d.price, W = 380, H = 66, L = 6, R = 6, y = 30;
    const x = (v) => L + (v - lo) / (hi - lo || 1) * (W - L - R);
    const head = m.below_high <= 2 ? `${d.company} is trading at its 52-week high.` : m.above_low <= 2 ? `${d.company} is trading at its 52-week low.`
      : `${d.company} is ${Math.round(m.below_high)}% below its 52-week high and ${Math.round(m.above_low)}% above its low.`;
    const svg = `<svg viewBox="0 0 ${W} ${H}" width="100%" role="img" aria-label="${esc(head)}">
      <rect x="${L}" y="${y - 4}" width="${W - L - R}" height="8" rx="4" fill="${C.grid}"/>
      <text x="${L}" y="${y + 24}" font-size="12" fill="${C.ink2}">Low ${money(lo, 0)}</text>
      <text x="${W - R}" y="${y + 24}" text-anchor="end" font-size="12" fill="${C.ink2}">High ${money(hi, 0)}</text>
      <g ${tipAttr(`<b>Share price</b><br>${money(p)} · ${m.range_pos}% of the way from low to high`)}><circle class="hit" cx="${x(p)}" cy="${y}" r="14"/><circle cx="${x(p)}" cy="${y}" r="7" fill="${C.ink}" stroke="${C.surface}" stroke-width="2"/></g>
      <text x="${Math.max(L + 40, Math.min(W - R - 40, x(p)))}" y="${y - 14}" text-anchor="middle" font-size="12.5" font-weight="600" fill="${C.ink}">${money(p, 0)}</text></svg>`;
    return `<div class="viz-block"><p class="viz-head">${esc(head)}</p><p class="meta">52-week price range</p>${svg}</div>`;
  }

  /* The business in brief: what it is, how it makes money, how the stock is valued */
  function briefCard(d) {
    const p = d.profile, v = d.valuation, name = d.company;
    const fmt = (m, val) => val === null || val === undefined ? '–' : (m.unit === '%' ? `${val.toFixed(1)}%` : `${val.toFixed(1)}x`);
    const rows = p.metrics.map((m) => `<tr><td>${esc(m.label)}<div class="meta">${esc(m.note)}</div></td><td class="num"><b>${fmt(m, m.value)}</b></td><td class="num">${fmt(m, m.sector_median)}</td></tr>`).join('');
    const fv = v.fair_value;
    const fvLine = fv ? `Fair value on this site's methods: <b>${money(fv, 0)}</b> a share, against a price of ${money(d.price, 0)} (${d.price > fv ? `${Math.round((d.price / fv - 1) * 100)}% above` : `${Math.round((1 - d.price / fv) * 100)}% below`}). The working is in the Fair value section below.`
      : `No fair value is calculated for this company. ${esc(v.method)}`;
    return `<div class="card brief">
      <h3><span>How the market prices it</span><small>${esc(p.kind)}</small></h3>
      <p class="plain">${esc(p.valued)}</p>
      <div class="viz-two">${peerBars(d)}${rangeBar(d)}</div>
      <div style="overflow-x:auto"><table class="brief-table"><thead><tr><th>Measure</th><th class="num">${esc(d.ticker)}</th><th class="num">Sector median</th></tr></thead><tbody>${rows}</tbody></table></div>
      <p class="meta">Sector median: the middle value among the ${esc(d.sector.toLowerCase())} companies on this site; a dash means fewer than three have the figure. Figures as of ${esc(d.price_date)}.</p>
      ${analystLine(d)}
    </div>`;
  }

  /* Of every dollar of sales: cost of goods, running costs, operating profit */
  function dollarBar(d) {
    const x = d.dollar;
    if (!x) return '';
    const c = (v) => `${Math.round(v)}¢`;
    if (x.op_profit === null) return `<div class="viz-block"><p class="viz-head">Of every dollar of revenue, ${esc(d.company)} keeps ${c(x.net)} as net profit.</p><p class="meta">Banks and insurers do not report cost of goods, so the split is not shown.</p></div>`;
    const head = x.op_profit >= 0 ? `Of every dollar of sales, ${d.company} keeps ${c(x.op_profit)} as operating profit.` : `${d.company} spends ${c(100 - x.op_profit)} to earn each dollar of sales.`;
    const parts = [['Cost of goods', Math.max(x.cogs, 0), '#c9cfcb'], ['Running costs', Math.max(x.opex, 0), '#9fa9a4'], ['Operating profit', Math.max(x.op_profit, 0), C.accent]];
    const tot = parts.reduce((a, r) => a + r[1], 0) || 1;
    const after = `After interest and tax, net profit is ${c(x.net)}${x.net > x.op_profit + 1 ? ' (lifted by gains outside day-to-day operations)' : ''}${x.fcf === null ? '' : `; free cash flow is ${c(x.fcf)}`}. Trailing twelve months.`;
    return `<div class="viz-block"><p class="viz-head">${esc(head)}</p>
      <div class="sbar" role="img" aria-label="${esc(head)}">${parts.map((r) => `<span style="width:${r[1] / tot * 100}%;background:${r[2]}"></span>`).join('')}</div>
      <div class="sleg">${parts.map((r) => `<span><i style="background:${r[2]}"></i>${r[0]} <b>${c(r[1])}</b></span>`).join('')}</div>
      <p class="meta">${esc(after)}</p></div>`;
  }

  /* Where the cash goes: operating cash flow split into capex, dividends, buybacks and what is left */
  function cashUse(d) {
    const u = d.cash_use;
    if (!u) return '';
    const back = u.dividends + u.buybacks, c = (v) => `${v}¢`;
    const head = u.left >= 0
      ? `Of every dollar of operating cash, ${c(u.capex)} went back into the business, ${c(back)} to shareholders, and ${c(u.left)} was left over.`
      : `For every dollar of operating cash, ${d.company} spent ${c(u.capex)} on the business and ${c(back)} on shareholders: ${c(-u.left)} more than came in.`;
    const parts = [['Capital spending', u.capex, '#3f7fc4'], ['Dividends', u.dividends, '#1f8a5b'], ['Buybacks', u.buybacks, '#c88a12']];
    if (u.left > 0) parts.push(['Left for debt, acquisitions and cash', u.left, '#c9cfcb']);
    const tot = Math.max(100, parts.reduce((a, r) => a + r[1], 0));
    const notes = [`${u.first}–${u.last}, ${esc(u.ocf)} of operating cash flow in total.`];
    if (u.left < 0) notes.push('The shortfall was funded by borrowing, asset sales or cash on hand.');
    if (u.sbc) notes.push(`Stock-based pay worth a further ${u.sbc}% was paid in shares, not cash.`);
    if (!u.capex_reported) notes.push('Capital spending is not reported separately by the data source.');
    return `<div class="viz-block cash-use"><h4>Where the cash goes</h4><p class="viz-head">${esc(head)}</p>
      <div class="sbar-wrap"><div class="sbar" role="img" aria-label="${esc(head)}">${parts.filter((r) => r[1] > 0).map((r) => `<span style="width:${r[1] / tot * 100}%;background:${r[2]}"></span>`).join('')}</div>
      ${tot > 100 ? `<i class="ocf-mark" style="left:${100 / tot * 100}%"><em>Operating cash flow</em></i>` : ''}</div>
      <div class="sleg">${parts.map((r) => `<span><i style="background:${r[2]}"></i>${r[0]} <b>${r[1]}%</b></span>`).join('')}</div>
      <p class="meta">${notes.join(' ')}</p></div>`;
  }

  /* Bull and bear tiles: the calculated figures that carry each case, each led by one number */
  function caseTiles(d, bull) {
    const rows = d.financial_health.ratios.flatMap((g) => g.rows.map((r) => ({ ...r, growth: g.group.startsWith('Growth') })));
    const order = bull
      ? ['Return on invested capital', 'Return on equity', 'Gross margin', 'Operating margin', 'Free cash flow margin', 'Net profit margin', 'Net debt to EBITDA', 'Equity to assets', 'Earnings per share', 'Revenue', 'Return on retained earnings']
      : ['Net debt to EBITDA', 'Debt to equity', 'Interest cover', 'Stock-based pay', 'Earnings per share', 'Revenue', 'Free cash flow', 'Free cash flow to net income', 'Payout ratio', 'Return on invested capital', 'Return on equity', 'Equity to assets'];
    const tiles = [];
    const v = d.valuation;
    if (v.fair_value) {
      const gap = d.price / v.fair_value;
      if (!bull && gap > 1) tiles.push([`${gap.toFixed(1)}x`, 'Price to fair value', `${money(d.price, 0)} against ${money(v.fair_value, 0)}`]);
      if (bull && gap <= 1) tiles.push([`${Math.round((1 - gap) * 100)}%`, 'Below fair value', `${money(d.price, 0)} against ${money(v.fair_value, 0)}`]);
    }
    for (const name of order) {
      if (tiles.length >= 3) break;
      const r = rows.find((q) => q.name === name && q.pass === bull);
      if (!r) continue;
      const big = r.value.length <= 12 ? r.value : (r.value.match(/[+-]?\d+(\.\d+)?(%|x)/) || [null])[0];
      if (!big) continue;
      tiles.push([big, r.growth ? `${r.name} growth a year` : r.name, `Yardstick: ${r.threshold}`]);
    }
    return tiles.length ? `<div class="tiles">${tiles.map((t) => `<div class="tile-n"><b>${esc(t[0])}</b><span>${esc(t[1])}</span><em>${esc(t[2])}</em></div>`).join('')}</div>` : '';
  }

  /* Fair value: the number, how it compares with the price, and the working behind it */
  function fairValueCard(d) {
    const v = d.valuation, p = d.price, dm = v.damodaran;
    if (v.intrinsic_value_low === null) {
      return `<div class="card fv"><h3><span>Fair value</span></h3><p class="fv-none">No fair value estimate.</p><p>${esc(v.method)}</p></div>`;
    }
    const lo = v.intrinsic_value_low, hi = v.intrinsic_value_high, mid = v.fair_value, gap = (p / mid - 1) * 100;
    const gapTxt = gap >= 0 ? `${Math.round(gap)}% above fair value` : `${Math.round(-gap)}% below fair value`;
    const row = (m) => `<tr><td><b>${esc(m.name)}</b><div class="meta">${esc(m.basis)}</div></td><td class="num">${money(m.low, 0)}–${money(m.high, 0)}</td><td class="num">${money((m.low + m.high) / 2, 0)}</td></tr>`;
    const st = v.stress_case;
    return `<div class="card fv">
      <h3><span>Fair value</span><small>per share</small></h3>
      <div class="fv-grid">
        <div class="fv-main"><span>Fair value</span><b>${money(mid, 0)}</b><em>Range ${money(lo, 0)}–${money(hi, 0)}</em></div>
        <div class="stat"><span>Price (${esc(d.price_date)})</span><b>${money(p, 0)}</b><em class="${gap > 0 ? 'down' : 'up'}">${gapTxt}</em></div>
        <div class="stat"><span>Margin of safety</span><b>${v.margin_of_safety_pct}%</b><em>Target: at least 30%</em></div>
        <div class="stat"><span>Buy below</span><b>${money(v.interesting_below, 0)}</b><em>Fair value less 30%</em></div>
      </div>
      ${d.verdict === 'PASS' || d.verdict === 'TOO_HARD' ? `<p class="meta">Shown for reference: price does not decide the verdict for this company.</p>` : ''}
      ${valueBar(d)}
      ${d.market && d.market.target ? `<p class="meta">◇ Analysts' average price target, shown for comparison; it is not part of this site's fair value.</p>` : ''}
      <h4>How the fair value is built</h4>
      <div style="overflow-x:auto"><table class="fv-table"><thead><tr><th>Method</th><th class="num">Low–high</th><th class="num">Mid-point</th></tr></thead><tbody>
        ${v.methods.map(row).join('')}
        <tr class="fv-total"><td><b>Fair value</b><div class="meta">${v.methods.length > 1 ? 'Average of the methods above' : 'The one method that applies'}</div></td><td class="num">${money(lo, 0)}–${money(hi, 0)}</td><td class="num"><b>${money(mid, 0)}</b></td></tr>
        ${st ? `<tr class="fv-stress"><td><b>Stress case, not in the average</b><div class="meta">${esc(st.basis)}</div></td><td class="num">${st.low === null ? 'None' : `${money(st.low, 0)}–${money(st.high, 0)}`}</td><td class="num">${st.low === null ? '–' : money((st.low + st.high) / 2, 0)}</td></tr>` : ''}
      </tbody></table></div>
      ${dm ? `<h4>Damodaran's question: what does the price assume?</h4>
      <p>${dm.implied_growth !== null
        ? `At ${money(p, 0)}, the market is pricing in sales growth of about <b>${dm.implied_growth}% a year</b> for five years at today's ${dm.margin}% operating margin. This assessment assumes <b>${dm.growth}%</b> (${dm.growth_low}–${dm.growth_high}% across the range), which takes sales from ${esc(dm.revenue_now)} to ${esc(dm.revenue_year10)} in ten years.`
        : `${esc(dm.implied_note)} This assessment assumes sales growth of <b>${dm.growth}%</b> a year for five years (${dm.growth_low}–${dm.growth_high}% across the range), which takes sales from ${esc(dm.revenue_now)} to ${esc(dm.revenue_year10)} in ten years.`}</p>
      <div class="nums">
        <div class="stat"><span>Sales growth, years 1–5</span><b>${dm.growth}%</b></div>
        <div class="stat"><span>Operating margin</span><b>${dm.margin}%</b></div>
        <div class="stat"><span>Return on capital</span><b>${dm.roc}%</b></div>
        <div class="stat"><span>Reinvested each year</span><b>${dm.reinvestment}%</b></div>
        <div class="stat"><span>Cost of capital</span><b>${dm.cost_of_capital}%</b></div>
        <div class="stat"><span>Growth after year 10</span><b>${dm.terminal_growth}%</b></div>
      </div>
      <p class="meta">Cost of capital: equity at ${dm.cost_of_equity}% (10-year Treasury ${d.treasury_10y.toFixed(2)}% + beta ${dm.beta.toFixed(2)} × 4.5% equity risk premium), debt at ${dm.cost_of_debt}% after tax, debt weight ${dm.debt_weight}%. Beta is set from the industry's pace of change (Damodaran prefers industry betas to single-stock regressions)${d.market && d.market.beta !== null ? `; the reported five-year beta is ${d.market.beta.toFixed(2)}, shown for reference` : ''}. Growth is the analyst's judgment; change it and the value changes.</p>` : ''}
      <details class="fv-method"><summary>Full method</summary><p>${esc(v.method)}</p></details>
    </div>`;
  }

  function valueTitle(d) {
    const v = d.valuation, mos = v.margin_of_safety_pct;
    if (mos === null) return 'No fair value estimate';
    const mid = (v.intrinsic_value_low + v.intrinsic_value_high) / 2;
    if (mos >= 30) return `Price sits ${Math.round(mos)}% below fair value: inside the buy zone`;
    if (mos >= 0) return `Price sits ${Math.round(mos)}% below fair value, short of the 30% margin of safety`;
    return `The price is ${(d.price / mid).toFixed(1)}x fair value`;
  }

  /* ---------- The compass: radar of the six pillars ----------
     Five business-quality pillars, then price (margin of safety) in its own shaded sector.
     Reference ring = the 7/10 "wonderful business" bar; grey outline = median of the 20 companies. */
  const PILLARS = [
    ['meaning', 'Meaning', 'M1', 'Can the business be explained simply?'],
    ['moat', 'Moat', 'M2', 'Durable competitive advantage'],
    ['industry', 'Industry', 'M2', 'Stable, not a technology war'],
    ['management', 'Management', 'M3', 'Integrity, intelligence, energy'],
    ['financial_health', 'Financial health', 'FCF', 'Nine calculated checks'],
    ['valuation', 'Margin of safety', 'M4', 'Price versus estimated value'],
  ];
  const BAR = 7;
  function medians() {
    const med = {};
    PILLARS.forEach(([k]) => {
      const a = INDEX.companies.map((c) => c.scores[k]).sort((x, y) => x - y), n = a.length;
      med[k] = n % 2 ? a[(n - 1) / 2] : (a[n / 2 - 1] + a[n / 2]) / 2;
    });
    return med;
  }

  function radar(sc) {
    const med = medians();
    const narrow = window.innerWidth < 700;
    const R = narrow ? 104 : 145, padX = narrow ? 92 : 138, W = 2 * (R + padX), H = 2 * R + (narrow ? 104 : 120), cx = W / 2, cy = H / 2 + 4, N = PILLARS.length;
    const ang = (i) => -Math.PI / 2 + i * 2 * Math.PI / N;
    const pt = (i, r) => [cx + Math.cos(ang(i)) * r, cy + Math.sin(ang(i)) * r];
    const ring = (r) => PILLARS.map((_, i) => pt(i, r).map((n) => n.toFixed(1)).join(',')).join(' ');
    let s = `<svg viewBox="0 0 ${W} ${H}" width="100%" style="max-width:${W}px;display:block;margin:0 auto" role="img" aria-label="Radar of six pillar scores out of 10: ${PILLARS.map(([k, l]) => `${l} ${sc[k]}`).join(', ')}. Median of 20 companies and the 7 out of 10 bar shown for reference.">`;
    // price sector wash (between the bisectors either side of the Margin of safety axis)
    const iP = N - 1, mid = (a, b) => [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2];
    const sector = [[cx, cy], mid(pt(iP - 1, R), pt(iP, R)), pt(iP, R), mid(pt(iP, R), pt(0, R))];
    s += `<polygon points="${sector.map((p) => p.map((n) => n.toFixed(1)).join(',')).join(' ')}" fill="${C.watch}" opacity="0.08"/>`;
    // grid rings and spokes
    [2.5, 5, 7.5, 10].forEach((r) => (s += `<polygon points="${ring(R * r / 10)}" fill="none" stroke="${r === 10 ? C.line : C.grid}" stroke-width="1"/>`));
    PILLARS.forEach((_, i) => { const [x, y] = pt(i, R); s += `<line x1="${cx}" y1="${cy}" x2="${x}" y2="${y}" stroke="${C.grid}" stroke-width="1"/>`; });
    // the 7/10 bar
    s += `<polygon points="${ring(R * BAR / 10)}" fill="none" stroke="#b39a5b" stroke-width="1.5"/>`;
    // peer median
    s += `<polygon points="${PILLARS.map(([k], i) => pt(i, R * med[k] / 10).map((n) => n.toFixed(1)).join(',')).join(' ')}" fill="none" stroke="#98a29d" stroke-width="1.5" stroke-linejoin="round"/>`;
    // the company
    const poly = PILLARS.map(([k], i) => pt(i, R * sc[k] / 10));
    s += `<polygon points="${poly.map((p) => p.map((n) => n.toFixed(1)).join(',')).join(' ')}" fill="${C.accent}" fill-opacity="0.12" stroke="${C.accent}" stroke-width="2.5" stroke-linejoin="round"/>`;
    PILLARS.forEach(([k, l, tag, what], i) => {
      const [x, y] = poly[i], below = sc[k] < BAR;
      const [lx, ly] = pt(i, R + (narrow ? 24 : 30));
      const anchor = Math.abs(lx - cx) < 8 ? 'middle' : lx > cx ? 'start' : 'end';
      const dy = Math.abs(lx - cx) < 8 ? (ly < cy ? -12 : 6) : -6;
      const tipHtml = `<b>${tag} · ${l}: ${sc[k]} / 10</b><br>${what}<br>Median of ${INDEX.companies.length}: ${med[k]}${below ? '<br>Below the 7 bar' : ''}`;
      s += `<g ${tipAttr(tipHtml)}><circle class="hit" cx="${x}" cy="${y}" r="14"/><circle cx="${x}" cy="${y}" r="5" fill="${below ? C.pass : C.accent}" stroke="${C.surface}" stroke-width="2"/></g>`;
      s += `<text x="${lx}" y="${ly + dy}" text-anchor="${anchor}" font-size="${narrow ? 11 : 12}" fill="${C.muted}">${narrow ? '' : tag + ' · '}${l}</text>`;
      s += `<text x="${lx}" y="${ly + dy + 17}" text-anchor="${anchor}" font-size="${narrow ? 14 : 16}" font-weight="700" fill="${C.ink}">${sc[k]}${below ? ` <tspan font-size="11" font-weight="600" fill="${C.pass}">▼</tspan>` : ''}</text>`;
    });
    return s + '</svg>';
  }

  /* What the shape says, in a value investor's words */
  function readShape(d) {
    const sc = d.scores, med = medians();
    const q = PILLARS.slice(0, 5), price = PILLARS[5];
    const clear = q.filter(([k]) => sc[k] >= BAR), gaps = q.filter(([k]) => sc[k] < BAR);
    const best = q.reduce((a, b) => (sc[b[0]] > sc[a[0]] ? b : a));
    const mos = d.valuation.margin_of_safety_pct, buy = d.valuation.interesting_below;
    const hasIv = d.valuation.intrinsic_value_low !== null;
    const mid = hasIv ? (d.valuation.intrinsic_value_low + d.valuation.intrinsic_value_high) / 2 : null;
    const priceTxt = !hasIv ? 'no estimate' : mos >= 0 ? `${Math.round(mos)}% below value` : `${(d.price / mid).toFixed(1)}x value`;
    let shape, read;
    if (d.verdict === 'TOO_HARD') {
      shape = 'Too hard to call';
      read = `${d.one_liner} The scores are shown for reference only.`;
    } else if (d.verdict === 'BUY_ZONE') {
      shape = gaps.length === 0 ? 'Full compass' : 'Good business at a low price';
      read = gaps.length === 0 ? 'A wonderful business at a sensible price: every pillar clears the bar, including price.'
        : `The price offers a margin of safety, with ${gaps.map(([, l]) => l.toLowerCase()).join(' and ')} below the bar. Check the bear case before acting.`;
    } else if (d.verdict === 'PASS' && gaps.length === 0) {
      shape = 'Fails a hard rule';
      read = `The pillars look sound, but the framework screens it out. ${d.one_liner}`;
    } else if (gaps.length === 0) {
      shape = 'Wonderful business, wrong price';
      read = `The shape fills out on every quality pillar and collapses on margin of safety. Nothing is wrong with the business; the price is the problem. Patience is the strategy${buy ? `: it becomes interesting below about ${money(buy, 0)}` : ''}.`;
    } else if (d.verdict !== 'PASS') {
      shape = 'Strong business with soft spots';
      read = `Quality clears the bar except on ${gaps.map(([, l]) => l.toLowerCase()).join(' and ')}. Worth owning at the right price, but those gaps argue for a wider margin of safety than usual.`;
    } else {
      shape = 'Gaps in the business itself';
      read = `${gaps.map(([k, l]) => `${l} (${sc[k]})`).join(', ')} ${gaps.length > 1 ? 'fall' : 'falls'} below the bar. No price fixes a weak pillar: a wonderful company at a fair price starts with the company.`;
    }
    const rows = PILLARS.map(([k, l, tag]) => {
      const diff = sc[k] - med[k];
      return `<tr><td><span class="mnum">${tag}</span>${l}</td><td class="num"><b>${sc[k]}</b></td><td class="num">${med[k]}</td><td class="num ${diff > 0 ? 'up' : diff < 0 ? 'down' : ''}">${diff > 0 ? '+' : ''}${diff === 0 ? '0' : diff}</td></tr>`;
    }).join('');
    return `<p class="shape-name">${esc(shape)}</p><p class="shape-read">${esc(read)}</p>
      <p class="shape-facts">Business quality: <b>${clear.length} of 5</b> pillars clear the 7 bar · Strongest: <b>${esc(best[1])} ${sc[best[0]]}</b> · Price: <b>${priceTxt}</b></p>
      <table class="score-table"><thead><tr><th>Pillar</th><th>Score</th><th>Median of ${INDEX.companies.length}</th><th>vs median</th></tr></thead><tbody>${rows}</tbody></table>`;
  }

  /* Price vs value: one number line with the value range, the buy line and today's price */
  function valueBar(d) {
    if (d.valuation.intrinsic_value_low === null) return '';
    const v = d.valuation, W = window.innerWidth < 700 ? 440 : 900, H = 150, L = 24, Rr = 24;
    const lo = v.intrinsic_value_low, hi = v.intrinsic_value_high, buy = v.interesting_below, p = d.price;
    const mk = d.market, tg = mk && mk.target ? mk.target : null;
    const max = Math.max(p, hi, tg || 0) * 1.1;
    const x = (n) => L + n / max * (W - L - Rr);
    const by = 74;
    const clampX = (px, w) => Math.max(L + w / 2, Math.min(W - Rr - w / 2, px));
    let s = `<svg viewBox="0 0 ${W} ${H}" width="100%" role="img" aria-label="Share price ${money(p)} against fair value ${money(lo)} to ${money(hi)}; buy below ${money(buy)}">`;
    s += `<line x1="${L}" x2="${W - Rr}" y1="${by}" y2="${by}" stroke="${C.line}" stroke-width="1"/>`;
    // ticks
    const step = niceStep(max / (W < 600 ? 3 : 5));
    for (let t = 0; t <= max; t += step) s += `<line x1="${x(t)}" x2="${x(t)}" y1="${by + 14}" y2="${by + 18}" stroke="${C.line}"/><text x="${x(t)}" y="${by + 32}" text-anchor="middle" font-size="11" fill="${C.muted}">$${t.toLocaleString('en-US')}</text>`;
    // buy zone (0 .. buy line) and value range
    s += `<rect x="${x(0)}" y="${by - 9}" width="${x(buy) - x(0)}" height="18" rx="4" fill="${C.buy}" opacity="0.14" ${tipAttr(`<b>Buy zone</b><br>At or below ${money(buy, 0)}, a 30% margin of safety`)}/>`;
    s += `<rect x="${x(lo)}" y="${by - 9}" width="${Math.max(4, x(hi) - x(lo))}" height="18" rx="4" fill="${C.accent}" opacity="0.32" ${tipAttr(`<b>Fair value range</b><br>${money(lo, 0)} to ${money(hi, 0)}`)}/>`;
    s += `<line x1="${x(buy)}" x2="${x(buy)}" y1="${by - 14}" y2="${by + 14}" stroke="${C.buy}" stroke-width="2"/>`;
    // price marker
    s += `<g ${tipAttr(`<b>Share price</b><br>${money(p)} at close ${esc(d.price_date)}`)}><circle class="hit" cx="${x(p)}" cy="${by}" r="14"/><circle cx="${x(p)}" cy="${by}" r="7" fill="${C.ink}" stroke="${C.surface}" stroke-width="2"/></g>`;
    // analysts' average target: hollow diamond, labelled above (raised a row if it would collide with the price label)
    if (tg) {
      const tx = x(tg), dy = 9;
      s += `<g ${tipAttr(`<b>Analysts' average target</b><br>${money(tg)} · consensus ${esc(mk.rating || 'n/a')} · as of ${esc(mk.as_of)}`)}><circle class="hit" cx="${tx}" cy="${by}" r="14"/><path d="M${tx} ${by - dy}L${tx + dy} ${by}L${tx} ${by + dy}L${tx - dy} ${by}Z" fill="${C.surface}" stroke="${C.ink2}" stroke-width="2"/></g>`;
      const tLab = `Analysts' target ${money(tg, 0)}`, tX = clampX(tx, 170);
      const clash = Math.abs(tX - clampX(x(p), 150)) < 165;
      s += `<text x="${tX}" y="${by - (clash ? 44 : 24)}" text-anchor="middle" font-size="12.5" fill="${C.ink2}">${tLab}</text>`;
    }
    // labels: price above, value range and buy line below the axis
    s += `<text x="${clampX(x(p), 150)}" y="${by - 24}" text-anchor="middle" font-size="13" font-weight="600" fill="${C.ink}">Price ${money(p, 0)}</text>`;
    const ivLabel = `Fair value ${money(lo, 0)}–${money(hi, 0)}`, buyLabel = `Buy below ${money(buy, 0)}`;
    const ivX = clampX(x((lo + hi) / 2), 170), buyX = clampX(x(buy), 130);
    const sameRow = Math.abs(ivX - buyX) < 160;
    s += `<text x="${ivX}" y="${by + 54}" text-anchor="middle" font-size="12.5" fill="${C.ink2}">${ivLabel}</text>`;
    s += `<text x="${buyX}" y="${by + (sameRow ? 72 : 54)}" text-anchor="middle" font-size="12.5" font-weight="600" fill="${C.buy}">${buyLabel}</text>`;
    return s + '</svg>';
  }
  function niceStep(raw) { const p = Math.pow(10, Math.floor(Math.log10(raw))); const n = raw / p; return (n < 1.5 ? 1 : n < 3 ? 2 : n < 7 ? 5 : 10) * p; }

  /* Small-multiple column chart for one measure, five fiscal years + TTM */
  function mini(hist, key, label) {
    const W = 300, H = 150, m = { l: 8, r: 8, t: 26, b: 22 };
    hist = hist.filter((h) => h[key] !== null && h[key] !== undefined);
    if (!hist.length) return '';
    const vals = hist.map((h) => h[key]);
    const hi = Math.max(0, ...vals), lo = Math.min(0, ...vals), span = hi - lo || 1;
    const y = (v) => m.t + (hi - v) / span * (H - m.t - m.b);
    const band = (W - m.l - m.r) / hist.length, bw = Math.min(24, band * 0.55);
    const first = hist[0], last = hist[hist.length - 1];
    let s = `<div><div class="mini-title">${label} <span>${bn(first[key])} → ${bn(last[key])}</span></div>
      <svg viewBox="0 0 ${W} ${H}" width="100%" role="img" aria-label="${label} by year: ${hist.map((h) => `${h.period} ${bn(h[key])}`).join(', ')}">`;
    hist.forEach((h, i) => {
      const v = h[key], cx = m.l + band * i + band / 2, x0 = cx - bw / 2, y0 = y(0), y1 = y(v), ttm = h.period === 'TTM';
      const hgt = Math.abs(y1 - y0), r = Math.min(4, hgt);
      const d = v >= 0
        ? `M${x0} ${y0} V${y1 + r} Q${x0} ${y1} ${x0 + r} ${y1} H${x0 + bw - r} Q${x0 + bw} ${y1} ${x0 + bw} ${y1 + r} V${y0} Z`
        : `M${x0} ${y0} V${y1 - r} Q${x0} ${y1} ${x0 + r} ${y1} H${x0 + bw - r} Q${x0 + bw} ${y1} ${x0 + bw} ${y1 - r} V${y0} Z`;
      s += `<g ${tipAttr(`<b>${label}</b> · ${h.period}<br>${bn(v)}`)}><rect class="hit" x="${cx - band / 2}" y="${m.t}" width="${band}" height="${H - m.t - m.b}"/>`;
      s += `<path d="${d}" fill="${v < 0 ? C.pass : C.accent}" opacity="${ttm ? 0.45 : 1}"/></g>`;
      s += `<text x="${cx}" y="${H - 6}" text-anchor="middle" font-size="10.5" fill="${C.muted}" font-weight="${ttm ? 600 : 400}">${h.period}</text>`;
    });
    s += `<line x1="${m.l}" x2="${W - m.r}" y1="${y(0)}" y2="${y(0)}" stroke="#cfc6b2" stroke-width="1"/>`;
    const lx = m.l + band * (hist.length - 1) + band / 2;
    const ly = last[key] >= 0 ? y(last[key]) - 6 : y(0) - 6;
    s += `<text x="${Math.min(lx, W - 30)}" y="${Math.max(12, ly)}" text-anchor="middle" font-size="11" font-weight="600" fill="${C.ink}">${bn(last[key])}</text>`;
    return s + '</svg></div>';
  }

  /* ---------- methodology ---------- */
  async function renderMethod() {
    $('view-method').hidden = false;
    document.title = 'Methodology — Value Investor';
    const md = await (await fetch('framework/value-investor.md')).text();
    const body = md.replace(/^version:.*\n|^updated:.*\n/gm, '');
    const ver = (md.match(/^version:\s*(.+)$/m) || [])[1];
    const html = window.marked ? window.marked.parse(body) : `<pre>${esc(body)}</pre>`;
    $('method-body').innerHTML = `<p class="meta">Framework v${esc(ver)} · this page displays the rulebook file the reports are built from.</p>` + html;
    window.scrollTo(0, 0);
  }

  window.addEventListener('hashchange', route);
  let wasNarrow = window.innerWidth < 700;
  window.addEventListener('resize', () => { const n = window.innerWidth < 700; if (n !== wasNarrow) { wasNarrow = n; route(); } });
  route();
})();
