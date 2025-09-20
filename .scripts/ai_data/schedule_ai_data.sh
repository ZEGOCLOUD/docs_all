#!/usr/bin/env bash
set -euo pipefail

# 定时任务管理脚本：启动/停止 每周六 02:00 的全量更新任务
# 使用：
#   交互：./schedule_ai_data.sh
#   启动：./schedule_ai_data.sh start
#   停止：./schedule_ai_data.sh stop

BLUE='\033[0;34m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
info(){ echo -e "${BLUE}[INFO]${NC} $*"; }
success(){ echo -e "${GREEN}[OK]${NC} $*"; }
warn(){ echo -e "${YELLOW}[WARN]${NC} $*"; }
error(){ echo -e "${RED}[ERR]${NC} $*" >&2; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
LOG_FILE="$LOG_DIR/ai_data_cron.log"

ensure_log_dir(){ mkdir -p "$LOG_DIR"; }

cron_has(){ crontab -l 2>/dev/null | grep -F "$1" >/dev/null 2>&1; }

install_cron(){
  ensure_log_dir
  local entry="0 2 * * 6 cd $SCRIPT_DIR && ./run_update_ai_data.sh --all >> $LOG_FILE 2>&1"
  # 先移除旧的相同任务
  local tmpfile
  tmpfile=$(mktemp)
  crontab -l 2>/dev/null | grep -v "run_update_ai_data.sh --all" > "$tmpfile" || true
  echo "$entry" >> "$tmpfile"
  crontab "$tmpfile"
  rm -f "$tmpfile"
  success "已安装定时任务：每周六 02:00 执行 --all 模式"
  info "日志文件：$LOG_FILE"
}

remove_cron(){
  local tmpfile
  tmpfile=$(mktemp)
  crontab -l 2>/dev/null | grep -v "run_update_ai_data.sh --all" > "$tmpfile" || true
  crontab "$tmpfile" || true
  rm -f "$tmpfile"
  success "已移除定时任务（如存在）"
}

case "${1:-}" in
  start)
    install_cron
    ;;
  stop)
    remove_cron
    ;;
  *)
    echo "=== AI 数据每周任务管理 ==="
    echo "1) 启动定时任务（每周六 02:00 执行 --all）"
    echo "2) 停止定时任务"
    echo -n "请选择 [1-2]（回车=1 启动）: "
    read -r ans || true
    if [[ "${ans:-1}" == "2" ]]; then
      remove_cron
    else
      install_cron
    fi
    ;;
 esac

