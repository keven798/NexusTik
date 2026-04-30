# GitHub 推送指南

## 创建GitHub仓库

由于GitHub MCP工具暂时无法连接，请按以下步骤手动创建仓库并推送代码：

### 1. 在GitHub上创建仓库

1. 访问 https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `抖音电商数据分析`
   - **Description**: `抖音电商数据分析平台 - 整合销售智能分析、短视频数据看板、客户细分与留存分析的完整解决方案`
   - **Visibility**: Public (或 Private)
   - **Initialize with README**: 不勾选 (因为我们已有README.md)

3. 点击 "Create repository"

### 2. 本地初始化并推送

在项目根目录打开终端，执行以下命令：

```bash
# 进入项目目录
cd "d:\agent AI电商数据分析\抖音电商数据分析"

# 初始化Git仓库
git init

# 添加所有文件
git add .

# 提交文件
git commit -m "Initial commit: 抖音电商数据分析平台

- 销售智能分析看板 (Dash + Plotly)
- 抖音短视频数据看板 (React + ECharts)
- 客户分析看板 (Streamlit + Plotly)
- 一键启动脚本
- 完整文档"

# 添加远程仓库 (替换为你的GitHub用户名)
git remote add origin https://github.com/你的用户名/抖音电商数据分析.git

# 推送代码
git branch -M main
git push -u origin main
```

### 3. 验证推送

1. 访问 `https://github.com/你的用户名/抖音电商数据分析`
2. 确认所有文件已上传
3. 检查README是否正确显示

## 项目结构

推送完成后，GitHub仓库将包含以下内容：

```
抖音电商数据分析/
├── README.md                          # 项目说明
├── requirements.txt                   # Python依赖
├── sales-intelligence-dashboard/      # 销售智能分析
│   └── app.py
├── douyin-video-dashboard/            # 抖音短视频看板
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── index.css
│       └── utils/
│           └── mockData.js
├── customer-analytics-dashboard/      # 客户分析
│   └── app.py
├── scripts/                           # 脚本工具
│   ├── setup.py
│   └── start_all.py
└── docs/                              # 文档
    └── GitHub推送指南.md
```

## 后续更新

如果后续有代码更新，执行：

```bash
# 添加修改的文件
git add .

# 提交修改
git commit -m "更新说明"

# 推送到GitHub
git push origin main
```

## 注意事项

1. **敏感信息**: 确保不要推送包含API密钥、密码等敏感信息的文件
2. **大文件**: 如果数据文件较大，考虑使用Git LFS或不上传
3. **依赖**: 确保requirements.txt和package.json完整

## 获取帮助

如果在推送过程中遇到问题：

1. 检查Git配置：`git config --list`
2. 检查远程仓库：`git remote -v`
3. 查看状态：`git status`
4. 参考GitHub文档：https://docs.github.com/

---

**项目已准备就绪，可以开始推送！** 🚀
