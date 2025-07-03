#!/usr/bin/env python3
"""
文档批量处理脚本
功能：
1. 检查和处理指定目录中所有文档的代码块格式（去除 ``` 标记）
2. 只修改内容，不移动文件
"""

import os
import re
from pathlib import Path

def find_code_blocks(content):
    """查找所有代码块"""
    # 匹配 ```language 和 ``` 的代码块
    pattern = r'```[a-zA-Z0-9_]*\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)
    return matches

def convert_code_blocks(content):
    """将代码块转换为缩进格式"""
    # 匹配 ```language 和 ``` 的代码块
    pattern = r'```[a-zA-Z0-9_]*\n(.*?)```'
    
    def replace_code_block(match):
        code_content = match.group(1)
        # 将代码内容转换为4空格缩进
        lines = code_content.split('\n')
        indented_lines = ['    ' + line for line in lines]
        return '\n'.join(indented_lines)
    
    return re.sub(pattern, replace_code_block, content, flags=re.DOTALL)

def process_directory(directory_path):
    """处理指定目录中的所有 Markdown 文档"""
    docs_dir = Path(directory_path)
    
    if not docs_dir.exists():
        print(f"❌ 目录不存在: {docs_dir}")
        return
    
    print(f"=== 处理目录: {docs_dir} ===")
    
    # 处理所有 .md 文件
    md_files = list(docs_dir.glob('*.md'))
    
    if not md_files:
        print(f"❌ 目录中没有找到 .md 文件: {docs_dir}")
        return
    
    total_files = 0
    total_code_blocks = 0
    
    for md_file in md_files:
        total_files += 1
        print(f"\n处理文档: {md_file.name}")
        
        # 读取文档内容
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查代码块
        code_blocks = find_code_blocks(content)
        if code_blocks:
            print(f"  发现 {len(code_blocks)} 个代码块")
            total_code_blocks += len(code_blocks)
            
            # 转换代码块格式
            new_content = convert_code_blocks(content)
            
            # 写回原文件
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"  已转换并保存到: {md_file}")
        else:
            print(f"  无代码块需要转换")
    
    print(f"\n=== 处理完成 ===")
    print(f"总文件数: {total_files}")
    print(f"总代码块数: {total_code_blocks}")

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1:
        # 使用命令行参数指定的目录
        directory = sys.argv[1]
    else:
        # 默认处理 docs/website 目录
        directory = 'docs/website'
    
    process_directory(directory)

if __name__ == '__main__':
    main()