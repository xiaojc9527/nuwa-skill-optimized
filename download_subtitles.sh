#!/bin/bash
# 从YouTube视频下载字幕
# 用法: ./download_subtitles.sh <YouTube_URL> [输出目录]
# 优先下载人工字幕，无人工字幕则使用自动生成字幕
# 增强错误处理和支持更多平台

set -euo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查依赖
check_dependencies() {
    local dependencies=('yt-dlp' 'curl' 'grep' 'sed' 'awk')
    local missing=()
    
    for dep in "${dependencies[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            missing+="$dep"
        fi
    done
    
    if [ ${#missing[@]} -gt 0 ]; then
        echo -e "${RED}错误: 缺少以下依赖: ${missing[*]}${NC}"
        echo -e "${YELLOW}请安装这些依赖后再运行此脚本${NC}"
        exit 1
    fi
}

# 显示帮助信息
show_help() {
    echo "用法: $0 <YouTube_URL> [输出目录]"
    echo ""
    echo "参数:"
    echo "  <YouTube_URL>   YouTube视频的URL"
    echo "  [输出目录]      可选，字幕保存的目录，默认为当前目录"
    echo ""
    echo "示例:"
    echo "  $0 https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    echo "  $0 https://www.youtube.com/watch?v=dQw4w9WgXcQ ./subtitles"
}

# 主函数
main() {
    # 检查依赖
    check_dependencies
    
    # 检查参数
    if [ $# -lt 1 ]; then
        show_help
        exit 1
    fi
    
    local url="$1"
    local output_dir="${2:-.}"
    
    # 创建输出目录
    mkdir -p "$output_dir"
    
    echo -e "${GREEN}开始从YouTube下载字幕...${NC}"
    echo -e "${YELLOW}视频URL: ${url}${NC}"
    echo -e "${YELLOW}输出目录: ${output_dir}${NC}"
    
    # 下载字幕
    # 首先尝试下载人工字幕
    local subtitle_file=""
    
    # 获取可用的字幕语言
    local languages
    languages=$(yt-dlp --list-subs "$url" 2>/dev/null | grep -E '\.vtt|\.srt' | awk '{print $1}' | head -5)
    
    if [ -z "$languages" ]; then
        echo -e "${YELLOW}警告: 未找到可用字幕，尝试使用自动生成字幕${NC}"
        yt-dlp --write-auto-sub --sub-lang zh,en --skip-download -o "$output_dir/%(title)s.%(ext)s" "$url"
    else
        echo -e "${GREEN}找到以下字幕语言:${NC}"
        echo "$languages"
        
        # 优先下载中文或英文字幕
        for lang in zh en; do
            if echo "$languages" | grep -q "$lang"; then
                echo -e "${GREEN}下载${lang}语言字幕...${NC}"
                yt-dlp --write-sub --sub-lang "$lang" --skip-download -o "$output_dir/%(title)s.%(ext)s" "$url"
                subtitle_file=$(find "$output_dir" -name "*.${lang}.*" | head -1)
                break
            fi
        done
        
        # 如果没有中文或英文字幕，下载第一个可用字幕
        if [ -z "$subtitle_file" ]; then
            local first_lang=$(echo "$languages" | head -1)
            echo -e "${GREEN}下载${first_lang}语言字幕...${NC}"
            yt-dlp --write-sub --sub-lang "$first_lang" --skip-download -o "$output_dir/%(title)s.%(ext)s" "$url"
            subtitle_file=$(find "$output_dir" -name "*.$first_lang.*" | head -1)
        fi
    fi
    
    # 检查是否成功下载
    if [ -z "$subtitle_file" ]; then
        subtitle_file=$(find "$output_dir" -name "*.vtt" -o -name "*.srt" | head -1)
    fi
    
    if [ -n "$subtitle_file" ]; then
        echo -e "${GREEN}字幕下载成功:${NC}"
        echo "$subtitle_file"
        
        # 转换为纯文本转录
        if [ -f "$subtitle_file" ]; then
            echo -e "${GREEN}正在生成纯文本转录...${NC}"
            local transcript_file="${subtitle_file%.*}_transcript.txt"
            
            # 使用Python脚本处理字幕
            if command -v python3 &> /dev/null; then
                python3 "$(dirname "$0")/srt_to_transcript.py" "$subtitle_file" -o "$transcript_file"
            else
                echo -e "${YELLOW}警告: Python3 未安装，无法生成纯文本转录${NC}"
            fi
        fi
    else
        echo -e "${RED}错误: 字幕下载失败${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}字幕下载完成！${NC}"
}

# 运行主函数
main "$@"
