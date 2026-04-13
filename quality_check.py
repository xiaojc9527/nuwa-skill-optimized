#!/usr/bin/env python3
"""
自动检查生成的SKILL.md是否通过Phase 4质量标准。
对照通过标准表格逐项检查，输出通过/不通过和具体原因。
增强错误处理和测试覆盖
"""
import os
import re
import argparse
from typing import Dict, List, Tuple

class QualityChecker:
    """质量检查器"""
    
    def __init__(self, skill_file: str):
        self.skill_file = skill_file
        self.requirements = {
            'mental_models': {'min': 3, 'max': 7, 'description': '心智模型数量'},  
            'decision_heuristics': {'min': 5, 'max': 10, 'description': '决策启发式数量'},
            'expression_dna': {'required': True, 'description': '表达DNA'},
            'values_anti_patterns': {'required': True, 'description': '价值观与反模式'},
            'honesty_boundaries': {'required': True, 'description': '诚实边界'},
            'sources': {'min': 10, 'description': '参考资料数量'}
        }
    
    def read_skill_file(self) -> str:
        """读取SKILL.md文件"""
        try:
            with open(self.skill_file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading {self.skill_file}: {e}")
            return ''
    
    def count_mental_models(self, content: str) -> int:
        """计算心智模型数量"""
        # 假设心智模型以特定格式标记
        patterns = [
            r'## 心智模型',
            r'Mental Models',
            r'- \[\w+\]'
        ]
        count = 0
        for pattern in patterns:
            count += len(re.findall(pattern, content))
        return count
    
    def count_decision_heuristics(self, content: str) -> int:
        """计算决策启发式数量"""
        # 假设决策启发式以特定格式标记
        patterns = [
            r'## 决策启发式',
            r'Decision Heuristics',
            r'- \w+:'
        ]
        count = 0
        for pattern in patterns:
            count += len(re.findall(pattern, content))
        return count
    
    def check_section_exists(self, content: str, section_name: str) -> bool:
        """检查特定部分是否存在"""
        patterns = [
            f'## {section_name}',
            f'### {section_name}',
            section_name
        ]
        for pattern in patterns:
            if re.search(pattern, content):
                return True
        return False
    
    def count_sources(self, content: str) -> int:
        """计算参考资料数量"""
        # 假设参考资料以特定格式标记
        patterns = [
            r'## 参考资料',
            r'References',
            r'\[\d+\]',
            r'https?://'
        ]
        count = 0
        for pattern in patterns:
            count += len(re.findall(pattern, content))
        return count
    
    def run_checks(self) -> Dict[str, Tuple[bool, str]]:
        """运行所有检查"""
        content = self.read_skill_file()
        if not content:
            return {'file_read': (False, '无法读取SKILL.md文件')}
        
        checks = {}
        
        # 检查心智模型
        mm_count = self.count_mental_models(content)
        mm_req = self.requirements['mental_models']
        if mm_count < mm_req['min']:
            checks['mental_models'] = (False, f'心智模型数量不足，需要至少{mm_req["min"]}个，当前有{mm_count}个')
        elif mm_count > mm_req['max']:
            checks['mental_models'] = (False, f'心智模型数量过多，最多{mm_req["max"]}个，当前有{mm_count}个')
        else:
            checks['mental_models'] = (True, f'心智模型数量符合要求 ({mm_count}个)')
        
        # 检查决策启发式
        dh_count = self.count_decision_heuristics(content)
        dh_req = self.requirements['decision_heuristics']
        if dh_count < dh_req['min']:
            checks['decision_heuristics'] = (False, f'决策启发式数量不足，需要至少{dh_req["min"]}个，当前有{dh_count}个')
        elif dh_count > dh_req['max']:
            checks['decision_heuristics'] = (False, f'决策启发式数量过多，最多{dh_req["max"]}个，当前有{dh_count}个')
        else:
            checks['decision_heuristics'] = (True, f'决策启发式数量符合要求 ({dh_count}个)')
        
        # 检查表达DNA
        if not self.check_section_exists(content, '表达DNA') and not self.check_section_exists(content, 'Expression DNA'):
            checks['expression_dna'] = (False, '缺少表达DNA部分')
        else:
            checks['expression_dna'] = (True, '表达DNA部分存在')
        
        # 检查价值观与反模式
        if not self.check_section_exists(content, '价值观与反模式') and not self.check_section_exists(content, 'Values and Anti-patterns'):
            checks['values_anti_patterns'] = (False, '缺少价值观与反模式部分')
        else:
            checks['values_anti_patterns'] = (True, '价值观与反模式部分存在')
        
        # 检查诚实边界
        if not self.check_section_exists(content, '诚实边界') and not self.check_section_exists(content, 'Honesty Boundaries'):
            checks['honesty_boundaries'] = (False, '缺少诚实边界部分')
        else:
            checks['honesty_boundaries'] = (True, '诚实边界部分存在')
        
        # 检查参考资料
        sources_count = self.count_sources(content)
        sources_req = self.requirements['sources']
        if sources_count < sources_req['min']:
            checks['sources'] = (False, f'参考资料数量不足，需要至少{sources_req["min"]}个，当前有{sources_count}个')
        else:
            checks['sources'] = (True, f'参考资料数量符合要求 ({sources_count}个)')
        
        return checks
    
    def generate_report(self, checks: Dict[str, Tuple[bool, str]]) -> str:
        """生成检查报告"""
        report = ['# SKILL质量检查报告', '']
        
        all_passed = all(result[0] for result in checks.values())
        report.append(f'总体结果: {"通过" if all_passed else "不通过"}')
        report.append('')
        
        for check_name, (passed, message) in checks.items():
            status = '✓' if passed else '✗'
            report.append(f'{status} {self.requirements.get(check_name, {}).get("description", check_name)}: {message}')
        
        return '\n'.join(report)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Check SKILL.md quality')
    parser.add_argument('skill_file', default='SKILL.md', nargs='?', help='Path to SKILL.md file')
    parser.add_argument('--output', default='quality_report.md', help='Output report file')
    args = parser.parse_args()
    
    checker = QualityChecker(args.skill_file)
    checks = checker.run_checks()
    report = checker.generate_report(checks)
    
    print(report)
    
    # 保存报告
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\nReport saved to {args.output}")

if __name__ == '__main__':
    main()
