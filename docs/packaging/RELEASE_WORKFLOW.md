# MonoPixel Editor 版本发布工作流

> 🚀 完整的版本发布流程指南

本文档提供从开发到发布的完整工作流程。

---

## 📑 目录

1. [版本号管理](#版本号管理)
2. [发布前准备](#发布前准备)
3. [打包和测试](#打包和测试)
4. [创建 GitHub Release](#创建-github-release)
5. [发布后工作](#发布后工作)
6. [回滚流程](#回滚流程)

---

## 版本号管理

### 1.1 语义化版本

使用 [语义化版本 2.0.0](https://semver.org/lang/zh-CN/) 规范：

```
主版本号.次版本号.修订号 (MAJOR.MINOR.PATCH)

例如: 1.2.3
```

**版本号递增规则**：

| 类型 | 何时递增 | 示例 |
|------|---------|------|
| **主版本号** | 不兼容的 API 修改 | 1.0.0 → 2.0.0 |
| **次版本号** | 向下兼容的功能性新增 | 1.0.0 → 1.1.0 |
| **修订号** | 向下兼容的问题修正 | 1.0.0 → 1.0.1 |

**先行版本**：
```
1.0.0-alpha.1   # Alpha 版本
1.0.0-beta.1    # Beta 版本
1.0.0-rc.1      # Release Candidate
```

---

### 1.2 更新版本号

**需要更新的文件**：

1. **src/main.py**
```python
__version__ = "1.0.0"
```

2. **README.md**
```markdown
# MonoPixel Editor v1.0.0
```

3. **docs/PROJECT_OVERVIEW.md**
```markdown
- **版本**: 1.0.0
```

4. **MonoPixelEditor.spec**（可选）
```python
VERSION = '1.0.0'
```

**自动化脚本**（推荐）：

**update_version.py**：
```python
#!/usr/bin/env python3
import sys
import re
from pathlib import Path

def update_version(new_version):
    """更新所有文件中的版本号"""
    files = {
        'src/main.py': r'__version__ = "[^"]+"',
        'README.md': r'# MonoPixel Editor v[0-9.]+',
        'docs/PROJECT_OVERVIEW.md': r'- \*\*版本\*\*: [0-9.]+',
    }

    for file_path, pattern in files.items():
        path = Path(file_path)
        if not path.exists():
            print(f"Warning: {file_path} not found")
            continue

        content = path.read_text(encoding='utf-8')

        if 'main.py' in file_path:
            new_content = re.sub(pattern, f'__version__ = "{new_version}"', content)
        elif 'README.md' in file_path:
            new_content = re.sub(pattern, f'# MonoPixel Editor v{new_version}', content)
        elif 'PROJECT_OVERVIEW.md' in file_path:
            new_content = re.sub(pattern, f'- **版本**: {new_version}', content)

        path.write_text(new_content, encoding='utf-8')
        print(f"✓ Updated {file_path}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python update_version.py <version>")
        print("Example: python update_version.py 1.0.1")
        sys.exit(1)

    new_version = sys.argv[1]
    update_version(new_version)
    print(f"\n✓ Version updated to {new_version}")
```

**使用**：
```bash
python update_version.py 1.0.1
```

---

## 发布前准备

### 2.1 代码质量检查

**步骤 1**：运行所有测试
```bash
# 单元测试
pytest tests/unit/ -v

# 测试覆盖率
pytest tests/ --cov=src --cov-report=html

# 检查覆盖率 >= 80%
```

**步骤 2**：代码风格检查（可选）
```bash
# 使用 black 格式化
black src/

# 使用 flake8 检查
flake8 src/

# 使用 mypy 类型检查
mypy src/
```

**步骤 3**：清理调试代码
```bash
# 搜索 print 语句
grep -r "print(" src/

# 搜索 TODO 注释
grep -r "TODO" src/

# 搜索 FIXME 注释
grep -r "FIXME" src/
```

---

### 2.2 更新文档

**步骤 1**：更新 CHANGELOG.md（如果有）
```markdown
# Changelog

## [1.0.1] - 2024-02-10

### Added
- 新增功能 A
- 新增功能 B

### Changed
- 改进功能 C
- 优化性能 D

### Fixed
- 修复 Bug E
- 修复 Bug F

### Removed
- 移除废弃功能 G
```

**步骤 2**：更新用户手册
- 添加新功能说明
- 更新截图（如果需要）
- 更新快捷键列表

**步骤 3**：更新 README.md
- 更新功能列表
- 更新安装说明
- 更新系统要求

---

### 2.3 Git 提交和标签

**步骤 1**：提交所有更改
```bash
# 查看状态
git status

# 添加所有更改
git add .

# 提交
git commit -m "chore: prepare for release v1.0.1"
```

**步骤 2**：创建 Git 标签
```bash
# 创建带注释的标签
git tag -a v1.0.1 -m "Release version 1.0.1"

# 查看标签
git tag -l

# 查看标签详情
git show v1.0.1
```

**步骤 3**：推送到远程
```bash
# 推送代码
git push origin main

# 推送标签
git push origin v1.0.1

# 或推送所有标签
git push origin --tags
```

---

## 打包和测试

### 3.1 多平台打包

**Windows**：
```bash
# 激活虚拟环境
.venv\Scripts\activate

# 清理旧文件
rmdir /s /q build dist

# 打包
pyinstaller MonoPixelEditor.spec

# 重命名
ren dist\MonoPixelEditor.exe MonoPixelEditor-1.0.1-Windows.exe
```

**macOS**：
```bash
# 激活虚拟环境
source .venv/bin/activate

# 清理旧文件
rm -rf build dist

# 打包
pyinstaller MonoPixelEditor.spec

# 创建 DMG（可选）
create-dmg \
  --volname "MonoPixel Editor" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --icon "MonoPixelEditor.app" 200 190 \
  --hide-extension "MonoPixelEditor.app" \
  --app-drop-link 600 185 \
  "MonoPixelEditor-1.0.1-macOS.dmg" \
  "dist/"
```

**Linux**：
```bash
# 激活虚拟环境
source .venv/bin/activate

# 清理旧文件
rm -rf build dist

# 打包
pyinstaller MonoPixelEditor.spec

# 创建 AppImage（可选）
./appimagetool-x86_64.AppImage MonoPixelEditor.AppDir MonoPixelEditor-1.0.1-Linux.AppImage
```

---

### 3.2 测试打包文件

**基础测试**：
- [ ] 应用程序正常启动
- [ ] 主窗口正确显示
- [ ] 界面样式正确
- [ ] 所有菜单项可用

**功能测试**：
- [ ] 所有绘图工具正常
- [ ] 图层系统正常
- [ ] 撤销/重做正常
- [ ] 导出功能正常
- [ ] 保存/加载项目正常

**兼容性测试**：
- [ ] 在干净系统上测试（无 Python 环境）
- [ ] 在不同操作系统版本测试
- [ ] 在不同屏幕分辨率测试

---

### 3.3 生成校验和

**Windows**：
```bash
certutil -hashfile MonoPixelEditor-1.0.1-Windows.exe SHA256 > checksums.txt
```

**macOS/Linux**：
```bash
shasum -a 256 MonoPixelEditor-1.0.1-macOS.dmg >> checksums.txt
shasum -a 256 MonoPixelEditor-1.0.1-Linux.AppImage >> checksums.txt
```

---

## 创建 GitHub Release

### 4.1 准备发布说明

**release_notes.md**：
```markdown
# MonoPixel Editor v1.0.1

## 🎉 新功能

- ✨ 新增功能 A - 详细说明
- ✨ 新增功能 B - 详细说明

## 🔧 改进

- 🎨 改进功能 C - 详细说明
- ⚡ 优化性能 D - 详细说明

## 🐛 Bug 修复

- 🐛 修复 Bug E - 详细说明
- 🐛 修复 Bug F - 详细说明

## 📦 下载

### Windows
- [MonoPixelEditor-1.0.1-Windows.exe](link)
  - SHA256: `abc123...`
  - 大小: 65 MB

### macOS
- [MonoPixelEditor-1.0.1-macOS.dmg](link)
  - SHA256: `def456...`
  - 大小: 75 MB

### Linux
- [MonoPixelEditor-1.0.1-Linux.AppImage](link)
  - SHA256: `ghi789...`
  - 大小: 70 MB

## 📋 系统要求

- **Windows**: Windows 10/11 (64-bit)
- **macOS**: macOS 10.14 或更高版本
- **Linux**: Ubuntu 18.04 或更高版本（或等效发行版）

## 📚 文档

- [用户手册](docs/USER_MANUAL.md)
- [开发文档](docs/DEVELOPMENT.md)
- [打包指南](docs/BUILD_GUIDE.md)

## 🔄 升级说明

从 v1.0.0 升级到 v1.0.1：
1. 下载新版本
2. 替换旧的可执行文件
3. 项目文件完全兼容，无需转换

## ⚠️ 已知问题

- 问题 A - 临时解决方案
- 问题 B - 计划在 v1.0.2 修复

## 🙏 致谢

感谢所有贡献者和用户的反馈！

---

**完整更新日志**: [v1.0.0...v1.0.1](https://github.com/user/repo/compare/v1.0.0...v1.0.1)
```

---

### 4.2 创建 Release

**方法 1**：通过 GitHub 网页界面

1. 访问 GitHub 仓库
2. 点击 "Releases" → "Draft a new release"
3. 选择标签：`v1.0.1`
4. 填写发布标题：`MonoPixel Editor v1.0.1`
5. 粘贴发布说明
6. 上传文件：
   - MonoPixelEditor-1.0.1-Windows.exe
   - MonoPixelEditor-1.0.1-macOS.dmg
   - MonoPixelEditor-1.0.1-Linux.AppImage
   - checksums.txt
7. 勾选 "Set as the latest release"
8. 点击 "Publish release"

**方法 2**：使用 GitHub CLI

```bash
# 安装 GitHub CLI
# https://cli.github.com/

# 登录
gh auth login

# 创建 Release
gh release create v1.0.1 \
  --title "MonoPixel Editor v1.0.1" \
  --notes-file release_notes.md \
  MonoPixelEditor-1.0.1-Windows.exe \
  MonoPixelEditor-1.0.1-macOS.dmg \
  MonoPixelEditor-1.0.1-Linux.AppImage \
  checksums.txt
```

---

### 4.3 验证 Release

**检查清单**：
- [ ] Release 页面正确显示
- [ ] 所有文件已上传
- [ ] 下载链接可用
- [ ] 发布说明格式正确
- [ ] 标签正确关联
- [ ] 设置为最新版本

---

## 发布后工作

### 5.1 更新文档网站

如果有文档网站（如 GitHub Pages）：
```bash
# 更新文档
cd docs
# 更新内容
git add .
git commit -m "docs: update for v1.0.1"
git push
```

---

### 5.2 发布公告

**GitHub Discussions**：
```markdown
# MonoPixel Editor v1.0.1 发布！

我们很高兴地宣布 MonoPixel Editor v1.0.1 正式发布！

## 主要更新
- 新增功能 A
- 修复 Bug B

## 下载
[GitHub Releases](https://github.com/user/repo/releases/tag/v1.0.1)

## 反馈
欢迎在 Issues 中报告问题或提出建议！
```

**社交媒体**（可选）：
- Twitter/X
- Reddit
- 技术论坛

---

### 5.3 监控反馈

**关注渠道**：
- GitHub Issues
- GitHub Discussions
- 用户反馈邮件

**快速响应**：
- 24 小时内回复严重 Bug
- 48 小时内回复一般问题
- 记录功能请求

---

### 5.4 准备下一个版本

**创建里程碑**：
```bash
# 在 GitHub 上创建 v1.0.2 里程碑
# 添加计划的 Issues
```

**更新开发分支**：
```bash
# 创建开发分支（如果使用）
git checkout -b develop
git push origin develop
```

---

## 回滚流程

### 6.1 何时回滚

**严重问题**：
- 应用无法启动
- 数据丢失或损坏
- 严重的安全漏洞

**回滚决策**：
- 评估问题严重程度
- 评估修复时间
- 如果修复时间 > 4 小时，考虑回滚

---

### 6.2 回滚步骤

**步骤 1**：标记问题版本
```bash
# 在 GitHub Release 中添加警告
# 编辑 Release，添加：
⚠️ **警告**: 此版本存在严重问题，请使用 v1.0.0
```

**步骤 2**：恢复上一个版本为最新
```bash
# 在 GitHub Release 中
# 将 v1.0.0 设置为 "Latest release"
```

**步骤 3**：发布回滚公告
```markdown
# 紧急通知：v1.0.1 回滚

由于发现严重问题，我们已将 v1.0.1 回滚。

## 问题描述
[详细描述问题]

## 建议操作
- 如果已安装 v1.0.1，请降级到 v1.0.0
- 下载链接：[v1.0.0](link)

## 后续计划
我们正在修复问题，预计在 [时间] 发布 v1.0.2

对此造成的不便深表歉意。
```

**步骤 4**：修复问题
```bash
# 创建修复分支
git checkout -b hotfix/v1.0.2 v1.0.0

# 修复问题
# ...

# 测试
pytest tests/

# 提交
git commit -m "fix: critical bug in v1.0.1"

# 合并到主分支
git checkout main
git merge hotfix/v1.0.2

# 发布 v1.0.2
```

---

## 发布检查清单

### 发布前
- [ ] 所有测试通过
- [ ] 代码已提交
- [ ] 版本号已更新
- [ ] 文档已更新
- [ ] CHANGELOG 已更新
- [ ] Git 标签已创建
- [ ] 标签已推送

### 打包
- [ ] Windows 打包完成
- [ ] macOS 打包完成
- [ ] Linux 打包完成
- [ ] 所有平台测试通过
- [ ] 校验和已生成

### 发布
- [ ] GitHub Release 已创建
- [ ] 文件已上传
- [ ] 发布说明已填写
- [ ] 设置为最新版本
- [ ] 下载链接已验证

### 发布后
- [ ] 发布公告已发布
- [ ] 文档网站已更新
- [ ] 监控反馈渠道
- [ ] 准备下一个版本

---

## 发布时间表示例

### 小版本发布（v1.0.x）

| 时间 | 任务 |
|------|------|
| T-7天 | 功能冻结，开始测试 |
| T-5天 | 更新文档 |
| T-3天 | 创建 RC 版本 |
| T-1天 | 最终测试 |
| T | 发布 |
| T+1天 | 监控反馈 |

### 大版本发布（v2.0.0）

| 时间 | 任务 |
|------|------|
| T-30天 | 功能冻结 |
| T-21天 | Alpha 版本 |
| T-14天 | Beta 版本 |
| T-7天 | RC 版本 |
| T-3天 | 最终测试 |
| T | 发布 |
| T+7天 | 监控反馈，准备补丁 |

---

## 自动化发布

### GitHub Actions 自动发布

**.github/workflows/release.yml**：
```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build-and-release:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [windows-latest, macos-latest, ubuntu-latest]

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pyinstaller

      - name: Build
        run: pyinstaller MonoPixelEditor.spec

      - name: Rename (Windows)
        if: matrix.os == 'windows-latest'
        run: |
          $version = $env:GITHUB_REF -replace 'refs/tags/v', ''
          Rename-Item dist\MonoPixelEditor.exe "MonoPixelEditor-$version-Windows.exe"

      - name: Upload to Release
        uses: softprops/action-gh-release@v1
        with:
          files: dist/*
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 参考资源

- [语义化版本](https://semver.org/lang/zh-CN/)
- [GitHub Releases 文档](https://docs.github.com/en/repositories/releasing-projects-on-github)
- [GitHub CLI 文档](https://cli.github.com/manual/)

---

**版本发布工作流 v1.0**

© 2024 MonoPixel. All rights reserved.
