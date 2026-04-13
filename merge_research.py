#!/usr/bin/env python3
"""
合并6个Agent的调研结果，生成Phase 1.5调研Review检查点的摘要表格。
扫描 references/research/ 目录
使用asyncio提升并行处理效率
"""
import asyncio
import os
import json
import csv
from typing import Dict, List, Any

async def read_research_file(file_path: str) -> Dict[str, Any]:
    """异步读取调研文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return {}

async def process_agent_research(agent_dir: str) -> Dict[str, Any]:
    """处理单个Agent的调研结果"""
    agent_data = {}
    tasks = []
    
    for root, _, files in os.walk(agent_dir):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                tasks.append(read_research_file(file_path))
    
    results = await asyncio.gather(*tasks)
    
    for result in results:
        agent_data.update(result)
    
    return agent_data

async def merge_research() -> Dict[str, Any]:
    """合并所有Agent的调研结果"""
    research_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'references', 'research')
    
    if not os.path.exists(research_dir):
        print(f"Research directory not found: {research_dir}")
        return {}
    
    agent_dirs = [d for d in os.listdir(research_dir) if os.path.isdir(os.path.join(research_dir, d))]
    
    tasks = []
    for agent_dir_name in agent_dirs:
        agent_dir_path = os.path.join(research_dir, agent_dir_name)
        tasks.append(process_agent_research(agent_dir_path))
    
    agent_results = await asyncio.gather(*tasks)
    
    # 合并结果
    merged_data = {}
    for i, result in enumerate(agent_results):
        agent_name = agent_dirs[i]
        merged_data[agent_name] = result
    
    return merged_data

def generate_summary_table(merged_data: Dict[str, Any], output_file: str = 'research_summary.csv'):
    """生成摘要表格"""
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Agent', 'Source Count', 'Key Insights', 'Confidence Score'])
        
        for agent, data in merged_data.items():
            source_count = len(data.get('sources', []))
            key_insights = len(data.get('key_insights', []))
            confidence = data.get('confidence_score', 0)
            writer.writerow([agent, source_count, key_insights, confidence])

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Merge research results from multiple agents')
    parser.add_argument('--output', default='research_summary.csv', help='Output file path')
    args = parser.parse_args()
    
    print("Merging research results...")
    merged_data = asyncio.run(merge_research())
    
    if merged_data:
        generate_summary_table(merged_data, args.output)
        print(f"Summary table generated: {args.output}")
        
        # 保存合并后的完整数据
        with open('merged_research.json', 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, ensure_ascii=False, indent=2)
        print("Merged research data saved to merged_research.json")
    else:
        print("No research data found to merge")

if __name__ == '__main__':
    main()
