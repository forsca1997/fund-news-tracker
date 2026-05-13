import feedparser
import datetime
import os
import pytz

# 配置 RSS 订阅源 (你可以随时在这里添加更多财经网站的 RSS)
RSS_FEEDS = {
    "FT中文网 (每日头条)": "http://www.ftchinese.com/rss/feed",
    "36氪 (财经)": "https://36kr.com/feed",
    "联合早报 (财经)": "https://www.zaobao.com/realtime/finance/rss",
}

def fetch_news():
    # 设置时区为北京时间
    tz = pytz.timezone('Asia/Shanghai')
    today = datetime.datetime.now(tz)
    date_str = today.strftime("%Y-%m-%d")

    # 创建 news 文件夹用于存放每日简报
    os.makedirs("news", exist_ok=True)
    filename = f"news/{date_str}.md"

    # 初始化 Markdown 内容
    content = f"# 全球财经与基金新闻简报 ({date_str})\n\n"
    content += "> 💡 *投资有风险，入市需谨慎。这是由 GitHub Actions 自动抓取的新闻聚合。*\n\n"

    for source, url in RSS_FEEDS.items():
        content += f"## 📰 {source}\n\n"
        try:
            feed = feedparser.parse(url)
            # 限制每个源只获取前 10 条最新新闻
            for entry in feed.entries[:10]:
                title = entry.title
                link = entry.link
                # 尝试获取发布时间
                pub_date = entry.get('published', '')
                content += f"- **[{title}]({link})** <small>{pub_date}</small>\n"
        except Exception as e:
            content += f"- 抓取失败: {e}\n"
        content += "\n"

    # 写入当天的 Markdown 文件
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully generated {filename}")

    # 更新 README.md，将最新新闻链接自动添加到主页
    update_readme(date_str, filename)

def update_readme(date_str, filename):
    readme_path = "README.md"
    link_str = f"- [{date_str} 财经新闻简报]({filename})\n"

    # 读取现有的 README
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    else:
        lines = ["# 基金新闻追踪 (Fund News Tracker)\n\n", "这里记录了每日自动抓取的全球财经与宏观新闻。\n\n", "## 历史新闻\n\n"]

    # 找到 "## 历史新闻" 并在其后方插入最新一天的链接
    try:
        insert_idx = lines.index("## 历史新闻\n") + 1
        # 避免重复插入同一天的链接
        if len(lines) <= insert_idx or lines[insert_idx] != link_str:
            lines.insert(insert_idx, link_str)
    except ValueError:
        # 如果 README 中没有 "## 历史新闻" 这个标题，则追加到末尾
        lines.extend(["\n## 历史新闻\n", link_str])

    with open(readme_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("Successfully updated README.md")

if __name__ == "__main__":
    fetch_news()
