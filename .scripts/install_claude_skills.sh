#!/bin/bash
#
# install_claude_skills.sh
# 安装项目特定的 Claude Code skills 到全局 plugins 目录
#

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 获取脚本所在目录的父目录（项目根目录）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SKILLS_DIR="$PROJECT_ROOT/.skills"
PLUGINS_DIR="$HOME/.claude/plugins"

echo -e "${GREEN}📦 Claude Code Skills 安装工具${NC}"
echo "================================"
echo "项目根目录: $PROJECT_ROOT"
echo "Skills 目录: $SKILLS_DIR"
echo "插件目录: $PLUGINS_DIR"
echo ""

# 检查 skills 目录是否存在
if [ ! -d "$SKILLS_DIR" ]; then
    echo -e "${RED}❌ 错误: .skills 目录不存在${NC}"
    echo "路径: $SKILLS_DIR"
    exit 1
fi

# 检查全局 plugins 目录
if [ ! -d "$PLUGINS_DIR" ]; then
    echo -e "${YELLOW}⚠️  创建全局 plugins 目录: $PLUGINS_DIR${NC}"
    mkdir -p "$PLUGINS_DIR"
fi

# 查找所有 skill 目录
echo -e "${GREEN}🔍 扫描可用的 skills...${NC}"
echo ""

skill_count=0
for skill_dir in "$SKILLS_DIR"/*/; do
    if [ -d "$skill_dir" ]; then
        skill_name=$(basename "$skill_dir")
        skill_file="$skill_dir/SKILL.md"

        # 检查是否是有效的 skill（包含 SKILL.md）
        if [ -f "$skill_file" ]; then
            skill_count=$((skill_count + 1))
            echo -e "${GREEN}✓${NC} 发现 skill: ${YELLOW}$skill_name${NC}"

            # 创建软链接或复制到全局 plugins 目录
            target_dir="$PLUGINS_DIR/$skill_name"

            # 如果目标已存在且是软链接，先删除
            if [ -L "$target_dir" ]; then
                echo "  🔄 移除旧链接"
                rm "$target_dir"
            fi

            # 如果目标已存在且是目录，询问是否删除
            if [ -d "$target_dir" ] && [ ! -L "$target_dir" ]; then
                echo -e "  ${YELLOW}⚠️  目标目录已存在: $target_dir${NC}"
                read -p "  是否删除并重新安装? (y/N) " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    rm -rf "$target_dir"
                else
                    echo "  跳过 $skill_name"
                    echo ""
                    continue
                fi
            fi

            # 创建软链接
            echo "  🔗 链接到: $target_dir"
            ln -s "$skill_dir" "$target_dir"

            if [ -L "$target_dir" ]; then
                echo -e "  ${GREEN}✅ 安装成功${NC}"
            else
                echo -e "  ${RED}❌ 安装失败${NC}"
            fi
            echo ""
        fi
    fi
done

if [ $skill_count -eq 0 ]; then
    echo -e "${YELLOW}⚠️  未找到任何 skill${NC}"
    echo "请确保 .skills 目录包含 skill 子目录，每个子目录都有 SKILL.md 文件"
    exit 1
fi

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}✅ 安装完成！共安装 $skill_count 个 skill${NC}"
echo ""
echo "📝 已安装的 skills:"
ls -1 "$PLUGINS_DIR" | while read skill; do
    if [ -L "$PLUGINS_DIR/$skill" ]; then
        target=$(readlink "$PLUGINS_DIR/$skill")
        echo "  • $skill → $target"
    fi
done
echo ""
echo -e "${YELLOW}💡 提示: 重启 Claude Code 即可使用新安装的 skills${NC}"
