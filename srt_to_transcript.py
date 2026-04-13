#!/usr/bin/env python3
"""
将SRT/VTT字幕文件清洗为干净的纯文本transcript。
去除时间戳、序号、重复行、HTML标签，输出可直接阅读的文本。
增强对不同格式字幕的兼容性
"""
import os
import re
import argparse
from typing import List, Tuple

def clean_srt_content(content: str) -> str:
    """清理SRT格式内容"""
    # 移除序号
    content = re.sub(r'^\d+\s*$', '', content, flags=re.MULTILINE)
    
    # 移除时间戳
    content = re.sub(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', '', content)
    
    return content

def clean_vtt_content(content: str) -> str:
    """清理VTT格式内容"""
    # 移除WEBVTT头部
    content = re.sub(r'^WEBVTT\s*$', '', content, flags=re.MULTILINE)
    
    # 移除时间戳
    content = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*$', '', content, flags=re.MULTILINE)
    
    # 移除样式信息
    content = re.sub(r'NOTE.*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'STYLE.*$', '', content, flags=re.MULTILINE)
    
    return content

def remove_html_tags(text: str) -> str:
    """移除HTML标签"""
    return re.sub(r'<[^>]+>', '', text)

def remove_duplicate_lines(lines: List[str]) -> List[str]:
    """移除重复行"""
    seen = set()
    unique_lines = []
    
    for line in lines:
        line = line.strip()
        if line and line not in seen:
            seen.add(line)
            unique_lines.append(line)
    
    return unique_lines

def process_subtitle_file(input_file: str) -> Tuple[str, str]:
    """处理字幕文件"""
    try:
        with open(input_file, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {input_file}: {e}")
        return '', ''
    
    # 根据文件扩展名选择处理方式
    ext = os.path.splitext(input_file)[1].lower()
    
    if ext == '.srt':
        content = clean_srt_content(content)
    elif ext == '.vtt':
        content = clean_vtt_content(content)
    else:
        # 尝试自动检测格式
        if 'WEBVTT' in content:
            content = clean_vtt_content(content)
        else:
            content = clean_srt_content(content)
    
    # 移除HTML标签
    content = remove_html_tags(content)
    
    # 分割为行并清理
    lines = content.split('\n')
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line]
    
    # 移除重复行
    lines = remove_duplicate_lines(lines)
    
    # 生成纯文本转录
    transcript = '\n'.join(lines)
    
    # 生成摘要（前10行）
    summary = '\n'.join(lines[:10]) + ('\n...' if len(lines) > 10 else '')
    
    return transcript, summary

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Convert subtitle files to clean transcript')
    parser.add_argument('input_file', help='Path to subtitle file (SRT or VTT)')
    parser.add_argument('--output', '-o', help='Output transcript file')
    parser.add_argument('--summary', '-s', action='store_true', help='Show summary of the transcript')
    args = parser.parse_args()
    
    transcript, summary = process_subtitle_file(args.input_file)
    
    if transcript:
        # 确定输出文件路径
        if args.output:
            output_file = args.output
        else:
            base_name = os.path.splitext(args.input_file)[0]
            output_file = f'{base_name}_transcript.txt'
        
        # 保存转录结果
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(transcript)
        print(f'Transcript saved to {output_file}')
        
        # 显示摘要
        if args.summary:
            print('\nTranscript summary:')
            print('=' * 50)
            print(summary)
            print('=' * 50)
    else:
        print('Failed to process subtitle file')

if __name__ == '__main__':
    main()
