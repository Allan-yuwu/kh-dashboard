#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate HTML from processed_clients.json"""

import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load data
with open(os.path.join(SCRIPT_DIR, 'data', 'processed_clients.json'), 'r', encoding='utf-8') as f:
    clients = json.load(f)

# Sort: charged first, then by B value desc
cat_order = {'收费客户': 0, '待续客户': 1, '流失客户': 2, '历史客户': 3, '0客户': 4}
clients.sort(key=lambda c: (cat_order.get(c['category'], 5), -c.get('b_value', 0)))

# Stats
stats = {'收费客户': 0, '待续客户': 0, '流失客户': 0, '历史客户': 0, '0客户': 0}
b50 = 0
expired = 0
for c in clients:
    stats[c['category']] = stats.get(c['category'], 0) + 1
    if c.get('b_range') == 'B50+':
        b50 += 1
    if c.get('expire_days') is not None and c['expire_days'] < 0:
        expired += 1

sales_map = {}
for c in clients:
    s = c['sales']
    if s not in sales_map:
        sales_map[s] = {'total': 0, '收费客户': 0, '待续客户': 0, '流失客户': 0, '历史客户': 0, '0客户': 0}
    sales_map[s]['total'] += 1
    sales_map[s][c['category']] += 1

sales_colors = {'黄盼': '#1a73e8', '叶竟仁': '#34a853', '赵悦': '#ff9800', '李根': '#c62828'}

# Generate HTML
lines = []
def w(s=""): lines.append(s)

w('<!DOCTYPE html>')
w('<html lang="zh-CN">')
w('<head>')
w('<meta charset="UTF-8">')
w('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
w('<title>项目营销十部 - 客户明细与跟进策略</title>')
w('<style>')
w('*{box-sizing:border-box;margin:0;padding:0}')
w('body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;background:#f5f7fa;color:#333;line-height:1.6}')
w('.header{background:linear-gradient(135deg,#1a237e,#3949ab,#1a73e8);color:#fff;padding:24px 20px;text-align:center}')
w('.header h1{font-size:24px;margin-bottom:8px}')
w('.header p{opacity:.9;font-size:13px}')
w('.container{max-width:1480px;margin:0 auto;padding:20px}')
w('.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px;margin-bottom:20px}')
w('.stat-card{background:#fff;border-radius:12px;padding:16px 14px;box-shadow:0 2px 8px rgba(0,0,0,.06);text-align:center}')
w('.stat-card .label{font-size:12px;color:#666;margin-bottom:6px}')
w('.stat-card .value{font-size:26px;font-weight:700}')
w('.stat-card .sub{font-size:11px;color:#999;margin-top:4px}')
w('.alert{background:#fff3e0;border-left:4px solid #ff9800;padding:14px 18px;border-radius:8px;margin-bottom:20px;display:flex;align-items:center;gap:12px}')
w('.alert .icon{font-size:20px}')
w('.alert .text{font-size:13px;color:#e65100}')
w('.sales-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;margin-bottom:20px}')
w('.sales-card{background:#fff;border-radius:12px;padding:16px;box-shadow:0 2px 8px rgba(0,0,0,.06)}')
w('.sales-card h4{display:flex;align-items:center;gap:10px;font-size:15px;margin-bottom:12px}')
w('.sales-card .avatar{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-size:14px;font-weight:600}')
w('.sales-card .metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}')
w('.sales-card .metric{text-align:center;padding:8px;background:#f8f9fa;border-radius:8px}')
w('.sales-card .metric .num{font-size:18px;font-weight:700}')
w('.sales-card .metric .lbl{font-size:11px;color:#888}')
w('.table-section{background:#fff;border-radius:12px;padding:20px;margin-bottom:20px;box-shadow:0 2px 8px rgba(0,0,0,.06)}')
w('.table-section h3{font-size:16px;margin-bottom:16px;color:#1a237e}')
w('.table-wrap{overflow-x:auto}')
w('table{width:100%;border-collapse:collapse;font-size:13px}')
w('th{padding:10px 12px;text-align:left;font-weight:600;color:#555;background:#f5f7fa;border-bottom:2px solid #e0e0e0;white-space:nowrap}')
w('td{padding:10px 12px;border-bottom:1px solid #eee;vertical-align:middle}')
w('tr:hover td{background:#f8f9fa}')
w('.client-name{font-weight:600;color:#1a237e}')
w('.toggle-btn{padding:4px 12px;border-radius:4px;border:1px solid #1a73e8;background:#fff;color:#1a73e8;cursor:pointer;font-size:12px}')
w('.toggle-btn:hover{background:#1a73e8;color:#fff}')
w('.tag{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:500}')
w('.tag-ok{background:#e8f5e9;color:#2e7d32}')
w('.tag-mid{background:#e0f2f1;color:#00695c}')
w('.tag-bad{background:#fff8e1;color:#f57f17}')
w('.b-badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600;color:#fff}')
w('.b50{background:#c62828}.b20{background:#ff9800}.b10{background:#1a73e8}.b5{background:#7c4dff}.b2{background:#00bfa5}.b0{background:#9e9e9e}')
w('.exp-badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px}')
w('.exp-ok{background:#e8f5e9;color:#2e7d32}')
w('.exp-soon{background:#fff3e0;color:#e65100}')
w('.exp-bad{background:#ffebee;color:#c62828}')
w('.effect-bar{display:flex;height:6px;border-radius:3px;overflow:hidden;margin-top:4px;width:80px}')
w('.effect-bar .g{background:#34a853}.effect-bar .m{background:#f9ab00}.effect-bar .b{background:#c62828}')
w('.num{font-family:monospace}.num.p{color:#34a853;font-weight:600}.num.n{color:#c62828}.num.z{color:#bbb}')
w('.detail-row{display:none}')
w('.detail-row.on{display:table-row}')
w('.detail-cell{padding:0!important;background:#f8f9fa;border-bottom:2px solid #e0e0e0}')
w('.detail-content{padding:20px}')
w('.detail-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-bottom:14px}')
w('.detail-item{background:#fff;padding:10px 12px;border-radius:8px}')
w('.detail-item .label{font-size:11px;color:#888;margin-bottom:4px}')
w('.detail-item .value{font-size:14px;font-weight:600}')
w('.detail-item .value.pos{color:#34a853}')
w('.strategy-box{background:#fff;padding:14px 16px;border-radius:8px;border-left:3px solid #1a73e8}')
w('.strategy-box h5{font-size:13px;color:#1a73e8;margin-bottom:8px}')
w('.strategy-box p{font-size:12px;color:#555;line-height:1.7}')
w('.filter-bar{display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap;align-items:center}')
w('.filter-bar select,.filter-bar input{padding:6px 10px;border-radius:6px;border:1px solid #ddd;font-size:13px}')
w('.filter-bar .cnt{margin-left:auto;font-size:13px;color:#666}')
w('.tabs{display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap}')
w('.tab{padding:8px 16px;border-radius:20px;border:1px solid #ddd;background:#fff;cursor:pointer;font-size:13px}')
w('.tab.on{background:#1a73e8;color:#fff;border-color:#1a73e8}')
w('@media(max-width:768px){.stats{grid-template-columns:repeat(2,1fr)}.sales-cards{grid-template-columns:1fr}.detail-grid{grid-template-columns:repeat(2,1fr)}}')
w('</style>')
w('</head>')
w('<body>')

# Header
w(f'<div class="header"><h1>📊 项目营销十部 - 客户明细与跟进策略</h1><p>数据更新时间：2026-06-03 | 总客户：183家 | 收费{stats["收费客户"]} | 待续{stats["待续客户"]} | 流失{stats["流失客户"]} | 历史{stats["历史客户"]} | 0客户{stats["0客户"]}</p></div>')
w('<div class="container">')

# Alert
w('<div class="alert"><div class="icon">🚨</div><div class="text"><strong>紧急提醒：</strong>10家待续客户90天内到期，10家已流失<br>待续客户需在会员到期前激活使用并推动续费；流失客户需紧急挽回</div></div>')

# Stats cards
w('<div class="stats">')
w(f'<div class="stat-card" style="border-top:3px solid #34a853"><div class="label">💰 收费客户</div><div class="value" style="color:#34a853">{stats["收费客户"]}</div><div class="sub">26A有收入</div></div>')
w(f'<div class="stat-card" style="border-top:3px solid #00bfa5"><div class="label">🔄 待续客户</div><div class="value" style="color:#00bfa5">{stats["待续客户"]}</div><div class="sub">会员期内待续费</div></div>')
w(f'<div class="stat-card" style="border-top:3px solid #c62828"><div class="label">💔 流失客户</div><div class="value" style="color:#c62828">{stats["流失客户"]}</div><div class="sub">已过期未续约</div></div>')
w(f'<div class="stat-card" style="border-top:3px solid #7c4dff"><div class="label">📜 历史客户</div><div class="value" style="color:#7c4dff">{stats["历史客户"]}</div><div class="sub">曾合作过</div></div>')
w(f'<div class="stat-card" style="border-top:3px solid #f9ab00"><div class="label">❄️ 0客户</div><div class="value" style="color:#f9ab00">{stats["0客户"]}</div><div class="sub">从未合作</div></div>')
w(f'<div class="stat-card" style="border-top:3px solid #c62828"><div class="label">🔥 B50+高价值</div><div class="value" style="color:#c62828">{b50}</div><div class="sub">需重点维护</div></div>')
w(f'<div class="stat-card"><div class="label">⏰ 已过期</div><div class="value" style="color:#c62828">{expired}</div><div class="sub">到期日已过</div></div>')
w('</div>')

# Sales cards
w('<div class="sales-cards">')
for name in ['黄盼', '叶竟仁', '赵悦', '李根']:
    info = sales_map.get(name, {'total':0,'收费客户':0,'待续客户':0,'流失客户':0,'历史客户':0,'0客户':0})
    color = sales_colors.get(name, '#1a73e8')
    w(f'<div class="sales-card"><h4><div class="avatar" style="background:{color}">{name[0]}</div>{name}</h4>')
    w('<div class="metrics">')
    w(f'<div class="metric"><div class="num">{info["total"]}</div><div class="lbl">总客户</div></div>')
    w(f'<div class="metric"><div class="num" style="color:#34a853">{info["收费客户"]}</div><div class="lbl">收费</div></div>')
    w(f'<div class="metric"><div class="num" style="color:#00bfa5">{info["待续客户"]}</div><div class="lbl">待续</div></div>')
    w(f'<div class="metric"><div class="num" style="color:#c62828">{info["流失客户"]}</div><div class="lbl">流失</div></div>')
    w(f'<div class="metric"><div class="num" style="color:#7c4dff">{info["历史客户"]}</div><div class="lbl">历史</div></div>')
    w(f'<div class="metric"><div class="num" style="color:#f9ab00">{info["0客户"]}</div><div class="lbl">0客户</div></div>')
    w('</div></div>')
w('</div>')

# Client table
w('<div class="table-section"><h3>📋 客户明细列表</h3>')
w('<div class="filter-bar">')
w('<select id="fs" onchange="A()"><option value="">全部销售</option>')
for name in ['黄盼', '叶竟仁', '赵悦', '李根']:
    w(f'<option>{name}</option>')
w('</select>')
w('<select id="fb" onchange="A()"><option value="">全部B值</option><option>B50+</option><option>B20</option><option>B10</option><option>B5</option><option>B2</option><option>B0</option></select>')
w('<select id="fc" onchange="A()"><option value="">全部分类</option><option>收费客户</option><option>待续客户</option><option>流失客户</option><option>历史客户</option><option>0客户</option></select>')
w('<select id="fe" onchange="A()"><option value="">全部到期</option><option value="x">已过期</option><option value="s">90天内到期</option></select>')
w('<select id="ft" onchange="A()"><option value="">全部效果</option><option>效果好</option><option>效果较好</option><option>效果一般</option></select>')
w('<input type="text" id="fq" placeholder="搜索客户..." oninput="A()">')
w('<span class="cnt" id="cnt">共 183 条</span>')
w('</div>')
w('<div class="tabs">')
tabs = [('all','全部'),('c','💰 收费'),('r','🔄 待续'),('u','💔 流失'),('h','📜 历史'),('z','❄️ 0客户'),('b5','🔥 B50+')]
for i,(k,v) in enumerate(tabs):
    cls = 'tab on' if i == 0 else 'tab'
    w(f'<button class="{cls}" onclick="T(\'{k}\')">{v}</button>')
w('</div>')
w('<div class="table-wrap"><table><thead><tr>')
for h in ['客户名称','销售','B值','网站26A','网站25A','到期日','效果','分类','操作']:
    w(f'<th>{h}</th>')
w('</tr></thead><tbody id="tb"></tbody></table></div></div>')
w('</div>')  # container

# JS
w('<script>')
w('const D=' + json.dumps(clients, ensure_ascii=False) + ';')
w('let CD=[...D],AF="",AA=!0,AT="all";')
w('function N(n){if(!n||n===0)return\'<span class="num z">-\</span>\';const s=Math.round(n).toLocaleString();return`<span class="num ${n>0?"p":"n"}">${n>0?"+":""}${s}</span>`}')
w('function BB(r){const m={"B50+":"b50","B20":"b20","B10":"b10","B5":"b5","B2":"b2","B0":"b0"};return`<span class="b-badge ${m[r]||"b0"}">${r}</span>`}')
w('function EB(d){if(d===null||d===undefined)return\'<span class="exp-badge">-\</span>\';if(d<0)return`<span class="exp-badge exp-bad">已过期${-d}天</span>`;if(d<=90)return`<span class="exp-badge exp-soon">${d}天后到期</span>`;return`<span class="exp-badge exp-ok">${d}天后到期</span>`}')
w('function CT(c,l){const m={"收费客户":"tag-ok","待续客户":"tag-mid","流失客户":"tag-bad","历史客户":"tag-ok","0客户":"tag-bad"};return`<span class="tag ${m[c]||"tag-bad"}">${l}</span>`}')
w("function R(d){const tb=document.getElementById('tb');tb.innerHTML='';d.forEach((c,i)=>{const tr=document.createElement('tr');let tg='tag-mid';if(c.tag==='效果好')tg='tag-ok';else if(c.tag==='效果一般')tg='tag-bad';tr.innerHTML=`<td><div class=\"client-name\">${c.name}</div><small>ID:${c.client_id}</small></td><td>${c.sales}</td><td>${BB(c.b_range)}<div style=\"font-size:11px;color:#888;margin-top:2px\">${Math.round(c.b_value).toLocaleString()}</div></td><td>${N(c.web26)}</td><td>${N(c.web25)}</td><td>${EB(c.expire_days)}<div style=\"font-size:11px;color:#888;margin-top:2px\">${c.expire||'-'}</div></td><td><span class=\"tag ${tg}\">${c.tag||'-'}</span><div class=\"effect-bar\">${c.total_pos>0?`<div class=\"g\" style=\"width:${(c.effect_good/c.total_pos*100)||0}%\"></div><div class=\"m\" style=\"width:${(c.effect_ok/c.total_pos*100)||0}%\"></div><div class=\"b\" style=\"width:${(c.effect_bad/c.total_pos*100)||0}%\"></div>`:''}</div></td><td>${CT(c.category,c.cat_label)}</td><td><button class=\"toggle-btn\" onclick=\"K(${i})\">详情</button></td>`;tb.appendChild(tr);const dt=document.createElement('tr');dt.className='detail-row';dt.id=`d-${i}`;dt.innerHTML=`<td colspan=\"9\" class=\"detail-cell\"><div class=\"detail-content\"><div class=\"detail-grid\"><div class=\"detail-item\"><div class=\"label\">网站25A</div><div class=\"value ${c.web25>0?'pos':''}\">${c.web25>0?Math.round(c.web25).toLocaleString():'-'}</div></div><div class=\"detail-item\"><div class=\"label\">网站26A</div><div class=\"value ${c.web26>0?'pos':''}\">${c.web26>0?Math.round(c.web26).toLocaleString():'-'}</div></div><div class=\"detail-item\"><div class=\"label\">24及以前网站A</div><div class=\"value\">${c.web24>0?Math.round(c.web24).toLocaleString():'-'}</div></div><div class=\"detail-item\"><div class=\"label\">2023 DP</div><div class=\"value\">${c.dp2023>0?Math.round(c.dp2023).toLocaleString():'-'}</div></div><div class=\"detail-item\"><div class=\"label\">2024 DP</div><div class=\"value\">${c.dp2024>0?Math.round(c.dp2024).toLocaleString():'-'}</div></div><div class=\"detail-item\"><div class=\"label\">2025 DP</div><div class=\"value ${c.dp2025>0?'pos':''}\">${c.dp2025>0?Math.round(c.dp2025).toLocaleString():'-'}</div></div><div class=\"detail-item\"><div class=\"label\">2023 51jobDP</div><div class=\"value\">${c.jobdp2023>0?Math.round(c.jobdp2023).toLocaleString():'-'}</div></div><div class=\"detail-item\"><div class=\"label\">2024 51jobDP</div><div class=\"value\">${c.jobdp2024>0?Math.round(c.jobdp2024).toLocaleString():'-'}</div></div><div class=\"detail-item\"><div class=\"label\">2025 51jobDP</div><div class=\"value ${c.jobdp2025>0?'pos':''}\">${c.jobdp2025>0?Math.round(c.jobdp2025).toLocaleString():'-'}</div></div><div class=\"detail-item\"><div class=\"label\">效果好职位</div><div class=\"value\">${c.effect_good||'-'}</div></div><div class=\"detail-item\"><div class=\"label\">效果较好职位</div><div class=\"value\">${c.effect_ok||'-'}</div></div><div class=\"detail-item\"><div class=\"label\">效果一般职位</div><div class=\"value\">${c.effect_bad||'-'}</div></div></div><div class=\"strategy-box\"><h5>🎯 跟进策略</h5><p>${c.strategy}</p></div></div></td>`;tb.appendChild(dt)});document.getElementById('cnt').textContent=`共 ${d.length} 条`}")
w('function K(i){const r=document.getElementById(`d-${i}`);r.classList.toggle("on");const b=r.previousElementSibling.querySelector(".toggle-btn");b.textContent=r.classList.contains("on")?"收起":"详情"}')
w('function A(){const s=document.getElementById("fs").value;const b=document.getElementById("fb").value;const c=document.getElementById("fc").value;const e=document.getElementById("fe").value;const t=document.getElementById("ft").value;const q=document.getElementById("fq").value.toLowerCase();CD=D.filter(d=>{if(s&&d.sales!==s)return!1;if(b&&d.b_range!==b)return!1;if(c&&d.category!==c)return!1;if(e==="x"&&(!d.expire_days||d.expire_days>=0))return!1;if(e==="s"&&(!d.expire_days||d.expire_days<0||d.expire_days>90))return!1;if(t&&d.tag!==t)return!1;if(q&&!d.name.toLowerCase().includes(q))return!1;if(AT==="c"&&d.category!=="收费客户")return!1;if(AT==="r"&&d.category!=="待续客户")return!1;if(AT==="u"&&d.category!=="流失客户")return!1;if(AT==="h"&&d.category!=="历史客户")return!1;if(AT==="z"&&d.category!=="0客户")return!1;if(AT==="b5"&&d.b_range!=="B50+")return!1;return!0});R(CD)}')
w("function T(t){AT=t;document.querySelectorAll('.tab').forEach(x=>x.classList.remove('on'));const m={all:0,c:1,r:2,u:3,h:4,z:5,b5:6};document.querySelectorAll('.tab')[m[t]].classList.add('on');A()}")
w("R(CD);")
w('</script>')
w('</body>')
w('</html>')

html_content = '\n'.join(lines)

output_path = os.path.join(SCRIPT_DIR, '项目营销十部客户明细.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Generated: {len(html_content)} chars")
print(f"Stats: 收费{stats['收费客户']} 待续{stats['待续客户']} 流失{stats['流失客户']} 历史{stats['历史客户']} 0客户{stats['0客户']} B50+{b50} 已过期{expired}")
