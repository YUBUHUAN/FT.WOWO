# 喔喔 · Supabase 初始化

1. 打开 Supabase 项目：
   <https://supabase.com/dashboard/project/jvklkgrrzexqivwcvzeh/sql/new>
2. 把仓库里的 `cloud/schema.sql` 全部粘贴进去，点 Run。
3. 看到 `Success. No rows returned` 就完成了。
4. 回到喔喔，注册一个新账号；这个账号只属于喔喔的 Supabase 项目，和墨墨完全独立。

不要在公开场合贴数据库密码或 `service_role` key。客户端只需要项目 URL 和 publishable key，已经写在 `cloud.json` 和 `android/cloud-config.js` 里。

## 表

- `wowo_accounts`
- `wowo_sessions`
- `wowo_states`

## RPC

- `wowo_register`
- `wowo_login`
- `wowo_me`
- `wowo_get_state`
- `wowo_save_state`
- `wowo_logout`
