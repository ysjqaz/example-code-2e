# Issue 跟踪器：GitHub Issues

本仓库的 issue 存放在 GitHub Issues 中。

## 工作流

- **创建 issue**：`gh issue create --title "<标题>" --body "<描述>"`
- **查看 issue**：`gh issue list`、`gh issue view <编号>`
- **关闭 issue**：`gh issue close <编号>`
- **添加标签**：`gh issue edit <编号> --add-label "<标签>"`

## PR 作为请求渠道

默认关闭。如需将外部 PR 纳入分诊队列，可将此标志设为 `on`。

- PRs as a request surface: `off`
