# Codex model matrix — Sol / Terra / Luna only

**Không dùng** id mơ hồ `gpt-5.6`. Pin family id:

| Id | Vai trò |
|----|--------|
| `gpt-5.6-sol` | Flagship — plan, judge, security, main orchestrator |
| `gpt-5.6-terra` | Everyday coding / design / contracts / spike |
| `gpt-5.6-luna` | Fast, hẹp, high-volume — scaffold, devops, QA, learning |

## Per role

| Role | Model | Effort |
|------|--------|--------|
| Main / orchestrator | `gpt-5.6-sol` | high |
| `architect_planner` | `gpt-5.6-sol` | high |
| `judge` | `gpt-5.6-sol` | high |
| `security` | `gpt-5.6-sol` | high |
| `spike` | `gpt-5.6-terra` | medium |
| `contract` | `gpt-5.6-terra` | medium |
| `designer` | `gpt-5.6-terra` | medium |
| `frontend` | `gpt-5.6-terra` | medium |
| `backend` | `gpt-5.6-terra` | medium |
| `database` | `gpt-5.6-terra` | medium |
| `scaffold` | `gpt-5.6-luna` | low |
| `devops` | `gpt-5.6-luna` | low |
| `qa` | `gpt-5.6-luna` | low |
| `learning` | `gpt-5.6-luna` | low |

## Defaults in config.toml

```toml
model = "gpt-5.6-sol"
model_reasoning_effort = "high"

[agents]
default_subagent_model = "gpt-5.6-terra"
default_subagent_reasoning_effort = "medium"
```

## Heuristic nhanh

- **Sol** — sai một phát đắt (kiến trúc, review, bảo mật).
- **Terra** — viết/sửa code và design hàng ngày.
- **Luna** — boilerplate, CI, test máy móc, proposal learning.

Parallel workers: 1× Sol orchestrator + nhiều Terra/Luna, tránh spawn toàn Sol.
