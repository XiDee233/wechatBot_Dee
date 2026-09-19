# 本地部署与版本管理

此仓库基于 https://github.com/fanyuantaier/wechatbot-new ，原始版本 2.2.5，提交 5b85e3e。保留原项目 GPL 许可证。

## 启动

Windows 下使用 Python 3.11 创建 `.venv311`，安装 `requirements-installed.txt` 中的依赖，然后双击 `启动配置界面.bat`。首次启动会复制 `config.example.py` 为本地配置，并复制 `examples/prompts` 中的默认提示词。

配置页面：http://127.0.0.1:5000/ 。在正常 Windows 桌面运行并保持微信登录。

## 本地改动

- 网页通过当前 Python 解释器启动机器人，避免使用缺少依赖的系统 Python。
- 模型列表显示真实 DeepSeek 模型名称。
- 主聊天增加 DeepSeek 官方思考模式开关，保存后动态读取，只发送最终回答。
- 独立启动入口绑定本机地址，不结束占用端口的其他程序。

## 版本记录

`git status` 查看改动；`git diff` 查看差异；`git add 文件名` 后用 `git commit -m "说明"` 保存一个版本。

真实 `config.py`、个人 `prompts`、聊天记录、记忆、日志、备份和 Python 环境均不跟踪。Git 备份不会包含这些私人数据，请单独妥善保管；不要强制添加这些文件。
