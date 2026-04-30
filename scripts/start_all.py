#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音电商数据分析平台 - 一键启动脚本
同时启动三个看板服务
"""

import subprocess
import sys
import os
import time
import webbrowser
from threading import Thread

def start_service(command, name, port, color_code):
    """启动服务"""
    color_prefix = f"\033[{color_code}m"
    color_suffix = "\033[0m"
    
    print(f"{color_prefix}🚀 启动 {name} (端口: {port})...{color_suffix}")
    
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 等待服务启动
        time.sleep(3)
        
        if process.poll() is None:
            print(f"{color_prefix}✅ {name} 启动成功！访问: http://localhost:{port}{color_suffix}")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"{color_prefix}❌ {name} 启动失败{color_suffix}")
            if stderr:
                print(f"错误: {stderr}")
            return None
            
    except Exception as e:
        print(f"{color_prefix}❌ {name} 启动失败: {e}{color_suffix}")
        return None

def open_browser(urls, delay=5):
    """延迟打开浏览器"""
    time.sleep(delay)
    for name, url in urls.items():
        print(f"🌐 正在打开 {name}: {url}")
        webbrowser.open(url)

def main():
    """主函数"""
    print("=" * 70)
    print("🚀 抖音电商数据分析平台 - 一键启动")
    print("=" * 70)
    
    # 获取项目根目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    print(f"📁 项目目录: {project_root}\n")
    
    # 定义服务
    services = {
        '销售智能分析': {
            'command': f'cd "{project_root}/sales-intelligence-dashboard" && python app.py',
            'port': 8050,
            'color': '94'  # 蓝色
        },
        '抖音短视频看板': {
            'command': f'cd "{project_root}/douyin-video-dashboard" && npm start',
            'port': 3000,
            'color': '95'  # 紫色
        },
        '客户分析看板': {
            'command': f'cd "{project_root}" && streamlit run customer-analytics-dashboard/app.py',
            'port': 8501,
            'color': '92'  # 绿色
        }
    }
    
    # 启动所有服务
    processes = {}
    for name, config in services.items():
        process = start_service(
            config['command'],
            name,
            config['port'],
            config['color']
        )
        if process:
            processes[name] = process
        time.sleep(2)  # 间隔启动
    
    if not processes:
        print("\n❌ 所有服务启动失败")
        return False
    
    print("\n" + "=" * 70)
    print("✅ 服务启动完成！")
    print("=" * 70)
    
    # 显示访问地址
    print("\n🌐 访问地址:")
    urls = {}
    for name, config in services.items():
        url = f"http://localhost:{config['port']}"
        urls[name] = url
        print(f"  • {name}: {url}")
    
    print("\n📋 操作说明:")
    print("  • 按 Ctrl+C 停止所有服务")
    print("  • 每个服务在独立的进程中运行")
    
    # 询问是否打开浏览器
    try:
        response = input("\n🌐 是否自动打开浏览器? (y/n): ").strip().lower()
        if response in ['y', 'yes', '是']:
            browser_thread = Thread(target=open_browser, args=(urls, 3))
            browser_thread.daemon = True
            browser_thread.start()
    except KeyboardInterrupt:
        pass
    
    print("\n" + "=" * 70)
    print("🔄 服务运行中...")
    print("=" * 70)
    
    # 等待用户中断
    try:
        while True:
            time.sleep(1)
            # 检查服务状态
            for name, process in list(processes.items()):
                if process.poll() is not None:
                    print(f"⚠️ {name} 已停止")
                    del processes[name]
            
            if not processes:
                print("\n❌ 所有服务已停止")
                break
                
    except KeyboardInterrupt:
        print("\n\n🛑 正在停止所有服务...")
        for name, process in processes.items():
            print(f"  停止 {name}...")
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                process.kill()
        
        print("✅ 所有服务已停止")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        sys.exit(1)
