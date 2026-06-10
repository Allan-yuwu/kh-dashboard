#!/bin/bash
# Batch collect competitor data for B50+ clients
# Usage: bash batch_competitor.sh

export PATH="$HOME/.local/bin:$PATH"
OUTDIR="/Users/allan/Library/Mobile Documents/com~apple~CloudDocs/Ai助理/小客同学/kehu-dashboard/competitor-data"
mkdir -p "$OUTDIR"

# Remaining B50+ clients (skip done: 地素时尚, 伊顿, 飞利浦)
CLIENTS=(
  "上海良信电器股份有限公司"
  "钛和检测认证集团股份有限公司"
  "钛和检测认证集团有限公司"
  "远景动力技术（江苏）有限公司"
  "上海罗莱生活科技有限公司"
  "上海朗阁教育科技股份有限公司"
  "上海盈石商务咨询有限公司"
  "浙江天正电气股份有限公司"
  "倍乐生商贸（中国）有限公司"
  "赛诺菲（中国）投资有限公司上海分公司"
  "益科德（上海）有限公司"
)

for client in "${CLIENTS[@]}"; do
  safe=$(echo "$client" | sed 's/[（）()]/ /g' | tr -d ' ')
  echo "=== $(date): Processing $client ==="
  
  # Liepin
  autoglm run --task "在猎聘搜索${client}公司主页，看招聘职位数和HR信息" --start-url "https://www.liepin.com" 2>&1 | tee "$OUTDIR/liepin-${safe}.log"
  sleep 5
  
  # Boss via Baidu
  autoglm run --task "在百度搜${client}Boss直聘公司主页，看招聘职位数和HR" --start-url "https://www.baidu.com" 2>&1 | tee "$OUTDIR/boss-${safe}.log"
  sleep 5
done

echo "=== ALL DONE ==="
