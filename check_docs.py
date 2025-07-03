#!/usr/bin/env python3
"""
文档检查脚本
检查指定目录中所有文档的代码块格式
"""

import re
from pathlib import Path

def check_code_blocks(content):
    """检查文档中的代码块"""
    # 检查是否还有 ``` 标记
    triple_backticks = re.findall(r'```[a-zA-Z0-9_]*', content)
    return len(triple_backticks)

def check_indented_blocks(content):
    """检查缩进代码块"""
    lines = content.split('\n')
    indented_count = 0
    in_indented_block = False
    
    for line in lines:
        if line.startswith('    ') and line.strip():
            if not in_indented_block:
                in_indented_block = True
                indented_count += 1
        else:
            in_indented_block = False
    
    return indented_count

def check_directory(directory_path):
    """检查指定目录中的所有 Markdown 文档"""
    docs_dir = Path(directory_path)
    
    if not docs_dir.exists():
        print(f"❌ 目录不存在: {docs_dir}")
        return
    
    print(f"=== 检查目录: {docs_dir} ===")
    
    # 处理所有 .md 文件
    md_files = list(docs_dir.glob('*.md'))
    
    if not md_files:
        print(f"❌ 目录中没有找到 .md 文件: {docs_dir}")
        return
    
    total_files = 0
    total_triple_backticks = 0
    total_indented_blocks = 0
    
    for md_file in md_files:
        total_files += 1
        print(f"\n检查文件: {md_file.name}")
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        triple_backticks = check_code_blocks(content)
        indented_blocks = check_indented_blocks(content)
        
        total_triple_backticks += triple_backticks
        total_indented_blocks += indented_blocks
        
        if triple_backticks > 0:
            print(f"  ⚠️  发现 {triple_backticks} 个 ``` 标记")
        else:
            print(f"  ✅ 无 ``` 标记")
        
        print(f"  📝 发现 {indented_blocks} 个缩进代码块")
    
    print(f"\n=== 检查总结 ===")
    print(f"总文件数: {total_files}")
    print(f"总 ``` 标记数: {total_triple_backticks}")
    print(f"总缩进代码块数: {total_indented_blocks}")
    
    if total_triple_backticks == 0:
        print("✅ 所有文档的代码块格式处理完成！")
    else:
        print("⚠️  仍有文档包含 ``` 标记，需要进一步处理")

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1:
        # 使用命令行参数指定的目录
        directory = sys.argv[1]
    else:
        # 默认检查 docs/website 目录
        directory = 'docs/website'
    
    check_directory(directory)

if __name__ == '__main__':
    main()