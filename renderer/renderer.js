let sessions = [];
let summary = [];
let chartInstance = null;

document.getElementById('select-folder').onclick = async () => {
  const folder = await window.api.selectFolder();
  if (!folder) return;
  document.getElementById('folder-path').textContent = folder;
  const sessionObjs = await window.api.readJsonFolder(folder);
  sessions = sessionObjs;
  summary = sessionObjs.map(s => {
    const meta = s.data.meta || {};
    const events = s.data.events || [];
    const overall_tph = meta.overall_tph || {};
    const tons = overall_tph.tons || 0;
    const tph = overall_tph.tons_per_hour || 0;
    const duration = meta.duration_seconds || 0;
    const miningRefined = events.filter(e => e.type === 'mining_refined').length;
    const commander = meta.commander || '';
    const ring = meta.ring || (meta.location && meta.location.body) || '';
    const content_summary = meta.content_summary || {High:0,Medium:0,Low:0};
    return {
      file: s.file,
      start: meta.start_time || '',
      end: meta.end_time || '',
      duration: +duration,
      tons: +tons,
      tph: +tph || 0,
      refined: miningRefined,
      commander,
      ring,
      content_summary
    };
  });
  renderSummaryTable();
  renderAggregates();
  clearChart();
  clearEventLog();
};

function renderSummaryTable() {
  const tbody = document.querySelector('#summary-table tbody');
  tbody.innerHTML = '';
  summary.forEach((s, i) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${s.file}</td>
    <td>${s.start}</td><td>${s.end}</td><td>${s.duration}</td>
    <td>${s.tons}</td><td>${s.tph}</td><td>${s.refined}</td><td>${s.commander}</td>`;
    tr.onclick = () => renderEventLog(i);
    tbody.appendChild(tr);
  });
}

function renderAggregates() {
  if (!summary.length) { document.getElementById('aggregates').innerHTML = ''; return; }
  const totalTons = summary.reduce((a,s)=>a+s.tons,0);
  const avgTons = totalTons/summary.length;
  const totalDur = summary.reduce((a,s)=>a+s.duration,0);
  const avgTPH = summary.reduce((a,s)=>a+s.tph,0)/summary.length;
  const totalRefined = summary.reduce((a,s)=>a+s.refined,0);
  document.getElementById('aggregates').innerHTML = `
    <b>Total Tons:</b> ${totalTons} &nbsp; 
    <b>Avg Tons/Session:</b> ${avgTons.toFixed(2)} &nbsp;
    <b>Total Duration (s):</b> ${totalDur} &nbsp;
    <b>Avg TPH:</b> ${avgTPH.toFixed(2)} &nbsp;
    <b>Total Refined Events:</b> ${totalRefined}
  `;
}

function clearChart() {
  if (chartInstance) {
    chartInstance.destroy();
    chartInstance = null;
  }
  document.getElementById('dashboard-chart').getContext('2d').clearRect(0,0,800,350);
}

function clearEventLog() {
  document.getElementById('event-log').textContent = '';
}

document.getElementById('show-chart').onclick = () => {
  if (!summary.length) return;
  const type = document.getElementById('chart-type').value;
  renderChart(type);
};

function renderChart(type) {
  clearChart();
  const ctx = document.getElementById('dashboard-chart').getContext('2d');
  if (type === 'tons') {
    chartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: summary.map(s=>s.file),
        datasets:[{label:"Tons mined", data:summary.map(s=>s.tons), backgroundColor:"royalblue"}]
      },
      options: {responsive:false, plugins:{title:{display:true,text:"Tons mined per session"}}, scales:{x: {ticks:{autoSkip:false, maxRotation:90, minRotation:60}}}}
    });
  } else if (type === 'tph') {
    chartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: summary.map((_,i)=>`Session ${i+1}`),
        datasets: [{label:"TPH", data: summary.map(s=>s.tph), backgroundColor:"seagreen"}]
      },
      options: {responsive:false, plugins:{title:{display:true,text:"TPH per session"}}, scales:{x: {ticks:{autoSkip:false}}}}
    });
  } else if (type === 'refined') {
    chartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: summary.map(s=>s.file),
        datasets: [{label:"Refined Events", data: summary.map(s=>s.refined), backgroundColor:"firebrick"}]
      },
      options: {responsive:false, plugins:{title:{display:true,text:"Refined events per session"}}, scales:{x: {ticks:{autoSkip:false, maxRotation:90, minRotation:60}}}}
    });
  } else if (type === 'pie') {
    // Sum content types
    const high = summary.reduce((a,s)=>a+(s.content_summary.High||0),0);
    const medium = summary.reduce((a,s)=>a+(s.content_summary.Medium||0),0);
    const low = summary.reduce((a,s)=>a+(s.content_summary.Low||0),0);
    chartInstance = new Chart(ctx, {
      type: 'pie',
      data: {
        labels: ["High","Medium","Low"],
        datasets: [{data:[high,medium,low], backgroundColor:["gold","skyblue","grey"]}]
      },
      options: {responsive:false, plugins:{title:{display:true,text:"Asteroid content summary (all sessions)"}}}
    });
  }
}

function renderEventLog(idx) {
  if (!sessions[idx]) return;
  const events = sessions[idx].data.events || [];
  const log = events.map(e => {
    const ts = e.timestamp || '';
    const typ = e.type || '';
    const details = JSON.stringify(e.details || {});
    return `${ts} | ${typ} | ${details}`;
  }).join('\n');
  document.getElementById('event-log').textContent = log || 'No events found.';
}