#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音电商数据分析平台 - 环境安装脚本
"""

import subprocess
import sys
import os

def run_command(command, description):
    """运行命令并显示结果"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ {description}完成")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description}失败")
        print(f"错误: {e.stderr}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 抖音电商数据分析平台 - 环境安装")
    print("=" * 60)
    
    # 获取项目根目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    print(f"📁 项目目录: {project_root}")
    
    # 安装Python依赖
    if not run_command(
        f"cd {project_root} && pip install -r requirements.txt",
        "安装Python依赖"
    ):
        print("❌ Python依赖安装失败")
        return False
    
    # 检查Node.js
    print("\n🔄 检查Node.js环境...")
    try:
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ Node.js版本: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ 未检测到Node.js，请先安装Node.js 16+")
        print("下载地址: https://nodejs.org/")
        return False
    
    # 安装抖音看板依赖
    douyin_dashboard_dir = os.path.join(project_root, "douyin-video-dashboard")
    if os.path.exists(douyin_dashboard_dir):
        if not run_command(
            f"cd {douyin_dashboard_dir} && npm install",
            "安装抖音看板Node依赖"
        ):
            print("⚠️ 抖音看板依赖安装失败，请手动安装")
    
    print("\n" + "=" * 60)
    print("✅ 环境安装完成！")
    print("=" * 60)
    print("\n📖 使用说明:")
    print("1. 启动销售分析: python sales-intelligence-dashboard/app.py")
    print("2. 启动抖音看板: cd douyin-video-dashboard && npm start")
    print("3. 启动客户分析: streamlit run customer-analytics-dashboard/app.py")
    print("4. 一键启动所有: python scripts/start_all.py")
    print("\n🌐 访问地址:")
    print("- 销售分析: http://localhost:8050")
    print("- 抖音看板: http://localhost:3000")
    print("- 客户分析: http://localhost:8501")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
