# Simple-Allow-Paste v2.6 🚀

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Simple-Allow-Paste** 是一款为突破网页及软件“粘贴限制”而设计的轻量化自动化工具。它不依赖剪贴板，而是通过 Windows 消息队列直接驱动目标窗口，实现高效、稳定的模拟输入。

---

## ✨ 核心特性

- 🛡️ **突破检测**：完全弃用 `WM_PASTE` 消息和剪贴板逻辑，绕过CTRL+V粘贴行为监控。
- ⌨️ **硬件级仿真**：基于 `PostMessageW` 异步注入 Unicode 字符，支持中文、特殊符号，且不占用当前键盘焦点。
- 🛑 **即时响应**：支持 `Q` 键全局热键监听，输入过程可随时中止。
- 🎨 **现代 UI**：基于 `CustomTkinter` 打造的响应式深色模式界面。
- 扯不下去了
---

## 🚀 快速开始

### 方案 A：直接运行 (推荐)
前往 [Releases](https://github.com/你的用户名/Simple-Allow-Paste/releases) 下载最新的 `.exe` 文件即可运行。

### 方案 B：源码运行
1. 克隆仓库：
   ```bash
   git clone [https://github.com/你的用户名/Simple-Allow-Paste.git](https://github.com/你的用户名/Simple-Allow-Paste.git)
