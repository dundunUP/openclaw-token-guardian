# OpenClaw-Token-Guardian 🛡️

**AI 接入协议专属：国产大模型 API 成本“物理熔断器”**

防止 Agent 逻辑死循环导致账单“背刺”。本工具专为 OpenClaw 自动化集群设计，支持 DeepSeek、通义千问、文心一言等国内主流模型计费逻辑。

---

## 🌟 核心功能

- **实时成本审计**：基于 2026 年最新大模型单价，毫秒级计算每步 Token 消耗。
- **物理级熔断 (Kill-Switch)**：当累计消耗触及硬限额（Hard Limit）时，立即强行终止进程，防止损失扩大。
- **阶梯式预警**：达到预算 80% 时自动触发告警日志，提醒人工接入。
- **本地化重定向**：预留 `local_fallback` 接口，支持在高成本时自动引导任务至本地算力（如 Mac Mini M4）。

---

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone 
cd openclaw-token-guardian
```

### 2. 安装环境依赖
```bash
pip install -r requirements.txt
```

### 3. 运行演示模式 (Simulation)
你可以直接运行演示脚本，观察守护者如何在模拟任务达到 20 元预算时执行强制断电：
```bash
python main.py
```

### ⚙️ 核心配置 (config.yaml)
你可以通过修改 config.yaml 来定义你的“财务防线”：

```yaml
sentry_settings:
  currency: "CNY"
  hard_limit: 20.0       # 单次任务最高预算（人民币）
  soft_warning: 15.0     # 触发警告的临界值
```

## 📖 进阶指南：如何集成至 OpenClaw (v2026.3+)

如果你正在运行 OpenClaw 自动化任务流，请按照以下 Markdown 结构指引注入 Token-Guardian 拦截器：

### 第一步：引入守护者类
在你的任务执行脚本（如 task_executor.py 或 agent_flow.py）开头引入：

```python
from guardian import TokenGuardian

# 初始化守护者实例（建议在主循环外完成）
guardian = TokenGuardian(config_path="./config.yaml")
task_total_cost = 0.0
```

### 第二步：在任务循环中执行实时审计
在每个 Agent 步骤（Step）完成后，传入 Token 消耗数据进行熔断检查：
```python
# 假设 response.usage 是 OpenClaw 标准输出的消耗统计
# 数据格式示例: {"model": "qwen-max", "input_tokens": 1200, "output_tokens": 500}

if response.usage:
    # 1. 实时计算本次步骤的成本
    current_step_cost = guardian.audit_cost(response.usage)
    
    # 2. 累加至当前任务总成本
    task_total_cost += current_step_cost
    
    # 3. 执行物理级熔断检测
    # 一旦总成本超过 config.yaml 中的 hard_limit，
    # 系统将直接执行 sys.exit(1)，强行掐断后续所有 API 请求。
    guardian.enforce_policy(task_total_cost)
    
    print(f"DEBUG: [Token-Guardian] 当前任务累计消耗: {task_total_cost} CNY")
```

🛡️ 开源协议
本项目采用 MIT License 协议。

📢 交流与反馈
本工具由 「 AI 接入协议 」 公众号作者开源提供。

如果你在 OpenClaw 部署、算力收租或 Agent 自动化中有任何问题，欢迎关注公众号交流。

公众号：AI 接入协议

作者：dundunUp

风险提示：本工具仅作为辅助止损手段，请务必同时在云服务商后台设置每日消费限额。
