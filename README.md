# AI Code Audit · 学习与模型接口实验

基于 [xy200303/AiCodeAudit](https://github.com/xy200303/AiCodeAudit) 的学习 Fork：使用语言模型解析源码与依赖关系，再沿图中的路径生成审计意见。本仓保留上游的两阶段流程，用于模型接口和审计工作流实验；不应把模型推断的图或审计意见当作已验证的静态调用图与漏洞结论。

## 当前流程

1. 扫描项目目录，按配置选择源码并分段。
2. Agent 1 调用模型解析代码单元与关系，写出 GraphML。
3. Agent 2 读取图中路径并调用模型，生成审计日志。

这是命令行学习项目，没有 Web 服务。两阶段均依赖真实模型接口；审计时会向所配置的模型服务发送待分析源码。支持的文件后缀由 `config.yaml` 定义，不代表已经逐语言完成准确率评测。

## 安装与配置

使用 Python 3.11 虚拟环境作为起点；当前依赖未锁定，其他 Python/依赖组合需要自行验证。

```sh
git clone https://github.com/SleepyChaos/AiCodeAudit.git
cd AiCodeAudit
python -m venv .venv
# macOS/Linux
. .venv/bin/activate
# Windows PowerShell 使用：.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

`config.yaml` 保存源码筛选、模型名称和接口地址，`openai.api_key` 默认留空。推荐在启动终端设置以下环境变量，覆盖 YAML 中相应字段；脚本不自动读取 `.env` 文件。

```sh
# macOS/Linux：替换为自己可用的 OpenAI 兼容服务
export OPENAI_API_KEY="your-api-key"
export OPENAI_BASE_URL="https://your-provider.example/v1"
export OPENAI_MODEL="your-model-id"
```

```powershell
# Windows PowerShell
$env:OPENAI_API_KEY = "your-api-key"
$env:OPENAI_BASE_URL = "https://your-provider.example/v1"
$env:OPENAI_MODEL = "your-model-id"
```

也可在本机修改 YAML 的 `openai` 配置，但不要把真实凭据提交到版本库。`max_per_tokens` 是源码分段参数，不是供应商计费或模型输出上限的保证。

## 运行

```sh
python main.py -d ./your-project -o ./output -b 2
```

先从少量文件和低并发开始，确认服务兼容性与费用后再扩大规模。命令行参数以 `main.py` 为准：

| 参数 | 含义 | 当前默认值 |
| --- | --- | --- |
| `-d` | 待审计目录 | `./演示项目/openssh-9.9p1` |
| `-o` | 输出目录 | `./output` |
| `-b` | 一批并发调用数量 | `100` |

默认目标是随仓库保存的第三方演示项目，默认并发也较高；首次体验建议显式传入自己的小样例。运行前不需要重建演示项目。

## 输出与限制

- `<project_md5>.graphml`：模型推断的代码关系图。
- `<project_md5>_审计结果.log`：沿图路径生成的模型审计意见。
- `app.log`：本地运行日志。启动不再打印完整模型配置，但审计日志仍可能包含源码和模型回复。

程序在同名 GraphML 已存在时会跳过第一阶段。模型、分段或输入内容改变后需要使用新的输出目录或核对旧图是否仍适用；当前缓存标识基于目录结构生成，不保证识别每次源码修改。`config.yaml` 的排除目录和文件大小限制也可能使部分源码未被分析。

本仓没有完整的自动化测试套件。可以先做不调用模型的语法检查：

```sh
python -m compileall -q main.py audit config models prompt utils
```

然后用自己确认过内容的小样例检查两个阶段是否实际完成。语法检查和服务调用成功都不代表漏洞识别质量已经验证。

## 目录

```text
audit/       源码扫描与两个模型审计阶段
config/      YAML 配置加载及环境变量覆盖
models/      配置和源码数据结构
prompt/      模型提示词
utils/       图与源码处理辅助函数
演示项目/    第三方样例源码，保留各自来源与许可
output/      生成结果，不作为常规源码新增提交
```

## 来源与许可

上游项目为 [xy200303/AiCodeAudit](https://github.com/xy200303/AiCodeAudit)，本仓保留其项目结构与审计流程。当前仓库未附独立 `LICENSE` 文件，第三方演示项目和可视化库分别保留其来源条件。模型接口实验不意味着本仓原创实现了全部审计框架，也不改变第三方代码的许可。
