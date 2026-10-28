# 喔喔 × 墨墨 好友绑定初始化

在 **Momo 的 Supabase 项目** SQL Editor 里按顺序运行：

1. `cloud/wowo_schema.sql`（来自 Wowo 仓库，创建 `wowo_*` 表与 RPC）
2. `cloud/friends.sql`（好友码、申请、绑定函数）

运行完后，Wowo 与 Momo 共用 Momo 项目，但账号表仍然分开。

说明：旧 Wowo Supabase 项目只保留为备份；新版 Wowo 的账号会写入 Momo 项目。旧 Wowo 项目如果已有账号，需要迁移或重新注册。
