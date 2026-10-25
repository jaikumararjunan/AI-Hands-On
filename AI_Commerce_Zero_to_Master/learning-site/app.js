const tracks={
 fresher:{focus:'Understand flow and vocabulary; run one service at a time.',challenge:'Explain what/why before changing code.'},
 '3y':{focus:'Implement APIs, tests, data cleaning, retries and basic ML.',challenge:'Debug failures and add one feature safely.'},
 '5y':{focus:'Own service boundaries, events, caching, security and CI/CD.',challenge:'Design trade-offs and production SLOs.'},
 '7y':{focus:'Lead domain architecture, data/AI platform integration and resilience.',challenge:'Migration plans, cost, scale and governance.'},
 '7plus':{focus:'Principal/architect view: organization, platform strategy, risk and evolution.',challenge:'Choose boundaries, standards, operating model and multi-year roadmap.'}
};
const sections={
 Overview:{flow:`CUSTOMER
  |
Web/Mobile -> Edge/CDN/WAF -> BFF/API Gateway
  |
Shopping -> Checkout/Payment -> Order/Fulfillment
  |                 |
  +-> Events/CDC -> Data Lake -> Warehouse/Lakehouse
                          |
                    BI + ML/DL + GenAI
                          |
                  Agents/MCP/RAG tools`,cards:[['Theory','Learn business capabilities before frameworks.'],['Practical','Trace one order from search to refund.'],['Hands-on','Start Java + Python; call health and search APIs.']]},
 Payments:{flow:`Checkout -> create payment intent -> customer authentication?
        -> authorize -> async webhook -> capture -> order paid
        -> refund/dispute/reconciliation later`,cards:[['Safety','Use provider tokens/hosted fields; never store PAN/CVV in this lab.'],['Reliability','Idempotency key + webhook de-duplication + timeout/retry policy.'],['Hands-on','POST /api/payments/intents, confirm/capture, then mock a webhook.']]},
 Data:{flow:`Operational DB -> Outbox/CDC -> Kafka
 -> Bronze(raw) -> Silver(clean/conformed) -> Gold(marts)
 -> Warehouse/Lakehouse -> features -> ML/BI/agents`,cards:[['Historical','Raw immutable history supports audit/replay.'],['Warehouse','Star schema and marts serve BI.'],['Future','Feature snapshots feed forecasts, churn, recommendations and agents.']]},
 AI:{flow:`Events + warehouse + catalog + knowledge
 -> features/embeddings
 -> ML/DL + vector search + RAG
 -> LangGraph agent -> governed tools/MCP`,cards:[['ML','fraud, churn, return risk, pricing, demand'],['DL','two-tower recommendations, sequence forecasting, autoencoders'],['GenAI','RAG, support copilot, seller copilot, marketing content, MCP tools']]},
 Production:{flow:`DEV -> QA -> UAT -> PREPROD -> PROD
 same immutable artifact; different config/secrets/scale
 traces + metrics + logs + SLOs + feature/model evaluation`,cards:[['Fast','CDN/cache, async events, bounded calls, connection pools.'],['Responsive','Budgets per dependency; fallback/degrade instead of cascading failure.'],['Observable','Trace checkout across Java, payment adapter, Kafka and Python AI.']]},
 MockData:{flow:`ONE SYNTHETIC WORLD
Customer -> Cart -> Order -> Payment -> Inventory -> Shipment -> Return
   |          |         |          |           |
Search/Click  Events   ML/DL     RAG/Vector   Logs/Traces/Metrics

Profiles: tiny -> small -> medium -> large -> xlarge
Scenarios: normal -> peak/fraud/payment/inventory/returns -> mixed-chaos`,cards:[['Ground','Run tiny + normal; inspect IDs and joins manually.'],['Developer','Use small profiles to debug APIs, events and failure scenarios.'],['Architect','Use larger/chaos profiles to reason about capacity, SLOs, queues, failure domains and cost.']]},
 Labs:{flow:`Lab 1 mock data + joins
Lab 2 payments
Lab 3 Bronze/Silver/Gold
Lab 4 marketing decision
Lab 5 vector/RAG
Lab 6 MCP
Lab 7 failure injection
Lab 8 production review`,cards:[['Code','Read -> run -> modify -> break -> debug -> explain.'],['Interview','For every line: what, why, failure, verification.'],['Architect','For every service: ownership, data, SLO, security, cost, evolution.']]}
};
let current='Overview';
function render(){const a=tracks[document.querySelector('#audience').value];document.querySelector('#tabs').innerHTML=Object.keys(sections).map(k=>`<button class="${k===current?'active':''}" data-tab="${k}">${k}</button>`).join('');const s=sections[current];document.querySelector('#content').innerHTML=`<div class="card"><span class="tag">Audience focus</span><b>${a.focus}</b><p>${a.challenge}</p></div><h2>${current}</h2><div class="flow">${s.flow}</div><div class="grid">${s.cards.map(c=>`<article class="card lab"><h3>${c[0]}</h3><p>${c[1]}</p></article>`).join('')}</div>`;document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>{current=b.dataset.tab;render()})}
document.querySelector('#audience').onchange=render;render();
