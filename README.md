# 📊 项目营销十部 - 客户明细与跟进策略

> 🔗 在线访问：**https://allan-yuwu.github.io/kh-dashboard/**

## 功能

- 183家客户明细表（分页10条/页）
- 5大分类Tab：收费/待续/流失/历史/0客户
- 流失/历史/0客户三类策略面板（附前程无忧验证）
- 按销售/B值/分类/到期/标签筛选
- 详情展开含跟进策略

## 更新数据

```bash
# 1. 修改 data/processed_clients.json
# 2. 重新生成 HTML
python3 generate_html.py
# 3. 提交推送
git add . && git commit -m "更新数据" && git push
```

等待1-2分钟，GitHub Pages 自动刷新。
