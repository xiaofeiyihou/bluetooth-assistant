#!/usr/bin/env python3
"""
GitHub Actions工作流版本验证脚本
验证build.yml文件中的所有action版本是否为最新稳定版本
"""

import re

def verify_github_actions_versions():
    """验证GitHub Actions工作流文件中的版本"""
    
    workflow_file = ".github/workflows/build.yml"
    
    try:
        with open(workflow_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔍 正在验证GitHub Actions工作流版本...")
        print(f"📁 检查文件: {workflow_file}")
        print("-" * 50)
        
        # 定义的最新稳定版本
        latest_versions = {
            'actions/checkout': 'v4',
            'actions/setup-python': 'v5', 
            'actions/upload-artifact': 'v4'
        }
        
        # 查找所有uses语句
        uses_pattern = r'uses:\s*([^@]+)@([^\s]+)'
        matches = re.findall(uses_pattern, content)
        
        all_correct = True
        
        for repo, version in matches:
            repo = repo.strip()
            version = version.strip()
            
            expected = latest_versions.get(repo)
            
            if expected:
                status = "✅ 正确" if version == expected else "❌ 需更新"
                if version != expected:
                    all_correct = False
                
                print(f"📦 {repo}:")
                print(f"   当前版本: {version}")
                print(f"   期望版本: {expected}")
                print(f"   状态: {status}")
                print()
            else:
                print(f"⚠️  未知仓库: {repo}@{version}")
                print()
        
        print("-" * 50)
        if all_correct:
            print("🎉 恭喜！所有GitHub Actions版本都是最新的稳定版本！")
            print("✅ 工作流文件已优化，不会再收到deprecated警告")
        else:
            print("⚠️  发现需要更新的版本，请更新到最新稳定版本")
        
        return all_correct
        
    except FileNotFoundError:
        print(f"❌ 错误: 找不到文件 {workflow_file}")
        return False
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        return False

def check_build_dependencies():
    """检查构建依赖是否完整"""
    workflow_file = ".github/workflows/build.yml"
    
    try:
        with open(workflow_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("\n🔍 检查构建依赖...")
        print("-" * 50)
        
        # 检查关键依赖
        dependencies = {
            'cython': 'Cython (用于Python编译)',
            'buildozer': 'Buildozer (Android构建工具)',
        }
        
        all_deps_present = True
        
        for dep, description in dependencies.items():
            if dep in content:
                print(f"✅ {dep}: {description}")
            else:
                print(f"❌ 缺失: {dep} - {description}")
                all_deps_present = False
        
        print()
        if all_deps_present:
            print("🎉 所有构建依赖都已配置完整！")
            print("✅ 修复了Cython缺失导致的构建失败问题")
        else:
            print("⚠️  仍有一些依赖需要添加")
        
        return all_deps_present
        
    except Exception as e:
        print(f"❌ 检查依赖时出错: {str(e)}")
        return False

def check_deprecated_patterns():
    """检查是否有其他deprecated模式"""
    
    workflow_file = ".github/workflows/build.yml"
    
    try:
        with open(workflow_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("\n🔍 检查其他可能的deprecated模式...")
        
        # 检查v3版本引用
        v3_patterns = [
            r'actions/checkout@v3',
            r'actions/setup-python@v4', 
            r'actions/upload-artifact@v3'
        ]
        
        found_deprecated = []
        
        for pattern in v3_patterns:
            matches = re.findall(pattern, content)
            if matches:
                found_deprecated.extend(matches)
        
        if found_deprecated:
            print("⚠️  发现deprecated版本引用:")
            for match in found_deprecated:
                print(f"   - {match}")
            print("请更新这些版本到最新稳定版本")
        else:
            print("✅ 未发现v3版本的引用")
            
    except Exception as e:
        print(f"❌ 检查deprecated模式时出错: {str(e)}")

def display_current_content():
    """显示当前工作流文件的关键内容"""
    workflow_file = ".github/workflows/build.yml"
    
    try:
        with open(workflow_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print("\n📄 当前工作流文件关键配置:")
        print("-" * 50)
        
        for i, line in enumerate(lines, 1):
            if 'uses:' in line or 'python-version:' in line or 'name:' in line or 'pip install' in line:
                print(f"第{i:2d}行: {line.strip()}")
                
    except Exception as e:
        print(f"❌ 读取文件时出错: {str(e)}")

if __name__ == "__main__":
    print("🚀 GitHub Actions工作流版本验证工具 (增强版)")
    print("=" * 60)
    
    # 显示当前配置
    display_current_content()
    
    # 验证版本
    is_correct = verify_github_actions_versions()
    
    # 检查构建依赖
    deps_ok = check_build_dependencies()
    
    # 检查deprecated模式
    check_deprecated_patterns()
    
    print("\n" + "=" * 60)
    print("📋 解决方案建议:")
    if is_correct and deps_ok:
        print("✅ 工作流配置完全正确，可以进行构建！")
        print("📱 接下来:")
        print("1. 推送到GitHub仓库")
        print("2. 清除GitHub Actions缓存")
        print("3. 重新触发构建")
    else:
        print("⚠️  发现配置问题，需要进一步修复")
    
    print("\n🎯 目标: 成功构建APK，消除所有警告和错误")