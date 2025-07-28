# Academic Papers Downloader

一个自动化下载学术论文的 Python 命令行工具。该脚本可以解析 Markdown 格式的论文列表，并按照分类和年份组织下载的 PDF 文件。

## ✨ 功能特性

- **📁 智能文件组织**: 自动按照 `分类/年份/论文标题.pdf` 的目录结构保存文件
- **📊 实时进度显示**: 使用进度条显示下载进度，支持文件级和整体进度
- **⚡ 断点续传**: 自动跳过已下载的文件，避免重复下载
- **🔄 会话保持**: 使用 requests Session 提高下载效率
- **❌ 错误处理**: 优雅处理下载失败，提供详细的错误报告
- **🎯 灵活输入**: 支持 Markdown 格式的论文列表

## 📋 系统要求

- Python 3.6+
- 依赖包：`requests`, `tqdm`

## 🚀 安装

1. **克隆仓库**
   ```bash
   git clone <repository_url>
   cd papers_download
   ```

2. **安装依赖**
   ```bash
   pip install requests tqdm
   ```

## 📖 使用方法

### 基本用法

```bash
python download.py papers.md --out downloads
```

### 命令行参数

- `input`: 输入的 Markdown 文件路径（必需）
- `--out`: 输出目录，默认为 `downloads`

### 输入文件格式

脚本支持以下 Markdown 格式：

```markdown
## 分类名称

- [年份] 论文标题 [[paper](论文URL)]
- [年份] 论文标题 [[documentation](文档URL)]
```

**示例：**

```markdown
## Survey

- [2025] Foundation Model Driven Robotics: A Comprehensive Review [[paper](https://arxiv.org/pdf/2507.10087)]
- [2025] A Survey on Vision-Language-Action Models [[paper](https://arxiv.org/pdf/2507.01925)]

## Reinforcement Learning

- [2024] Deep Q-Networks for Robotic Control [[paper](https://arxiv.org/pdf/example.pdf)]
```

## 📂 输出结构

下载的文件将按以下结构组织：

```
output_directory/
├── Survey/
│   ├── 2025/
│   │   ├── Foundation_Model_Driven_Robotics_A_Comprehensive_Review.pdf
│   │   └── A_Survey_on_Vision_Language_Action_Models.pdf
│   └── 2024/
│       └── ...
└── Reinforcement_Learning/
    └── 2024/
        └── Deep_Q_Networks_for_Robotic_Control.pdf
```

## 🎯 使用示例

1. **下载到默认目录**
   ```bash
   python download.py papers.md
   ```

2. **指定输出目录**
   ```bash
   python download.py papers.md --out ./my_papers
   ```

3. **下载到当前目录**
   ```bash
   python download.py papers.md --out .
   ```

## 🔧 工作原理

1. **解析阶段**: 脚本首先解析 Markdown 文件，提取分类、年份、标题和 URL
2. **预处理**: 统计需要下载的文件数量（跳过已存在的文件）
3. **下载阶段**: 
   - 为每个论文创建对应的目录结构
   - 使用会话保持提高下载效率
   - 实时显示下载进度
   - 处理下载错误并记录失败信息
4. **报告阶段**: 显示下载结果和失败文件列表

## 📊 输出信息

脚本运行时会显示：

- 📥 总体下载进度条
- ⏭️ 跳过已下载的文件
- 📄 当前下载的文件名
- 📥 单个文件下载进度（带大小信息）
- ❌ 下载失败的文件及原因
- 🎉 下载完成摘要

## ⚠️ 注意事项

- 脚本会自动创建必要的目录结构
- 已存在的文件将被跳过，不会重复下载
- 部分 URL 可能因为访问限制而下载失败（如 403 Forbidden、404 Not Found）
- 论文标题会自动转换为文件系统友好的格式（ASCII 字符，下划线分隔）

## 🐛 故障排除

### 常见错误

1. **ModuleNotFoundError**: 确保已安装 `requests` 和 `tqdm`
   ```bash
   pip install requests tqdm
   ```

2. **403/404 错误**: 某些 URL 可能需要特定的访问权限或已失效
3. **超时错误**: 网络连接问题，脚本会自动重试

### 调试提示

- 检查输入文件格式是否正确
- 确认网络连接正常
- 查看错误报告中的详细信息

## 📄 许可证

[在此添加许可证信息]

---

如有问题或建议，请提交 Issue 或 Pull Request。
