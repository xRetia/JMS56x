# driver — JMS56x UAS → BOT 覆盖驱动（Windows x64）

部分场景（老系统、数据恢复、某些工具软件）需要设备以 **BOT（Bulk-Only Transport）** 模式工作，而 JMS56x 默认以 **UAS** 模式加载。本驱动通过覆盖 INF 强制切换，不引入任何新内核。

> **语言：** [English](README.md) · 中文

## 作用

- 覆盖 `VID_152D` 下全部 JMS56x 常见 PID：0561 / 0562 / 0567 / 1561 / 2561 / 2566 / 2590 / 3562 / 3569 / 8561 / 9561 / 9562 / 9566 / 9567
- **不引入任何新 `.sys`**，仅复用系统自带的 `usbstor.sys`（BOT 存储类驱动）
- 安装后设备管理器显示 **JMicron JMS56x USB 3.0 to SATA Adapter (BOT Mode)**

## 文件说明

| 文件 | 用途 |
| --- | --- |
| `install.bat` | 经 `gsudo64.exe` 提权，导入签名证书到受信任根，`pnputil /add-driver jms56xbot.inf /install` |
| `uninstall.bat` | 提权后移除驱动包（调用 `remove-driver.ps1`）并删除证书 |
| `remove-driver.ps1` | 查找与 `jms56xbot.inf` 对应的 `oem*.inf` 发布包并删除 |
| `jms56xbot.inf` | 覆盖 INF（USB 类，复用 `usbstor.inf` 的 BOT 安装段） |
| `jms56xbot.cat` | INF 配套目录文件 |
| `JMS561TestSigner.cer` | 自签名测试证书（CN=JMS561 Test Signer） |
| `gsudo64.exe` | 便携提权工具（缓存凭证模式） |

## 安装

右键 `install.bat` → **以管理员身份运行**（或双击，脚本自动提权），完成后重新插拔设备即可生效。

## 卸载

右键 `uninstall.bat` → **以管理员身份运行**，重新插拔后恢复 UAS 模式。

## 说明

- 证书为**自签名测试证书**，Windows 可能提示"未知发布者"，属正常现象。
- 验证：signtool `/pa`（应用策略）通过；`/kp`（内核策略 / DSE）因自签链无法链到微软根而失败——属预期，且本 INF 不含新 `.sys`，不受影响。
- INF 覆盖全家 PID（含 UAS 与 BOT 变体）；上报 `197B:0562`（家族默认 ID）与 `152D` 系列 PID 的设备均会被匹配。