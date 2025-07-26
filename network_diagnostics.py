#!/usr/bin/env python3
"""
Network Diagnostics for SONALI Music Bot
Run this to diagnose connection issues
"""

import asyncio
import socket
import subprocess
import sys
import time
import json
from pathlib import Path

def test_dns_resolution():
    """Test DNS resolution for Telegram endpoints"""
    endpoints = [
        "api.telegram.org",
        "149.154.167.50",  # Telegram DC2
        "149.154.175.50",  # Telegram DC4
        "91.108.56.130"    # Telegram DC5
    ]
    
    print("🔍 Testing DNS Resolution...")
    results = []
    
    for endpoint in endpoints:
        try:
            start_time = time.time()
            ip = socket.gethostbyname(endpoint)
            response_time = (time.time() - start_time) * 1000
            print(f"✅ {endpoint} -> {ip} ({response_time:.1f}ms)")
            results.append({"endpoint": endpoint, "ip": ip, "time": response_time, "status": "OK"})
        except socket.gaierror as e:
            print(f"❌ {endpoint} -> DNS Error: {e}")
            results.append({"endpoint": endpoint, "error": str(e), "status": "FAILED"})
    
    return results

def test_tcp_connectivity():
    """Test TCP connectivity to Telegram"""
    endpoints = [
        ("api.telegram.org", 443),
        ("api.telegram.org", 80),
        ("149.154.167.50", 443),
        ("149.154.175.50", 443)
    ]
    
    print("\n🔌 Testing TCP Connectivity...")
    results = []
    
    for host, port in endpoints:
        try:
            start_time = time.time()
            sock = socket.create_connection((host, port), timeout=10)
            sock.close()
            response_time = (time.time() - start_time) * 1000
            print(f"✅ {host}:{port} ({response_time:.1f}ms)")
            results.append({"host": host, "port": port, "time": response_time, "status": "OK"})
        except (socket.timeout, socket.error) as e:
            print(f"❌ {host}:{port} -> {e}")
            results.append({"host": host, "port": port, "error": str(e), "status": "FAILED"})
    
    return results

def test_http_connectivity():
    """Test HTTP/HTTPS connectivity"""
    try:
        import requests
        
        print("\n🌐 Testing HTTP/HTTPS Connectivity...")
        results = []
        
        urls = [
            "https://api.telegram.org",
            "https://www.google.com",
            "https://httpbin.org/ip"
        ]
        
        for url in urls:
            try:
                start_time = time.time()
                response = requests.get(url, timeout=10)
                response_time = (time.time() - start_time) * 1000
                print(f"✅ {url} -> {response.status_code} ({response_time:.1f}ms)")
                results.append({"url": url, "status_code": response.status_code, "time": response_time, "status": "OK"})
            except requests.RequestException as e:
                print(f"❌ {url} -> {e}")
                results.append({"url": url, "error": str(e), "status": "FAILED"})
        
        return results
    except ImportError:
        print("⚠️ requests module not available, skipping HTTP tests")
        return []

def check_firewall_ports():
    """Check if common ports are accessible"""
    print("\n🔥 Checking Firewall/Port Access...")
    
    ports_to_check = [80, 443, 8080, 8443]
    results = []
    
    for port in ports_to_check:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex(("www.google.com", port))
            sock.close()
            
            if result == 0:
                print(f"✅ Port {port} is accessible")
                results.append({"port": port, "status": "OPEN"})
            else:
                print(f"❌ Port {port} is blocked")
                results.append({"port": port, "status": "BLOCKED"})
        except Exception as e:
            print(f"⚠️ Port {port} test failed: {e}")
            results.append({"port": port, "error": str(e), "status": "ERROR"})
    
    return results

def check_proxy_settings():
    """Check for proxy settings"""
    print("\n🔄 Checking Proxy Settings...")
    
    proxy_vars = ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"]
    proxy_found = False
    
    for var in proxy_vars:
        import os
        value = os.environ.get(var)
        if value:
            print(f"🔍 Found proxy setting: {var}={value}")
            proxy_found = True
    
    if not proxy_found:
        print("ℹ️ No proxy settings detected")
    
    return proxy_found

def ping_test():
    """Perform ping test to various endpoints"""
    print("\n🏓 Performing Ping Test...")
    
    endpoints = [
        "8.8.8.8",           # Google DNS
        "1.1.1.1",           # Cloudflare DNS
        "api.telegram.org",   # Telegram API
        "149.154.167.50"     # Telegram DC
    ]
    
    results = []
    
    for endpoint in endpoints:
        try:
            if sys.platform.startswith('win'):
                cmd = ['ping', '-n', '4', endpoint]
            else:
                cmd = ['ping', '-c', '4', endpoint]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"✅ Ping to {endpoint}: SUCCESS")
                results.append({"endpoint": endpoint, "status": "SUCCESS"})
            else:
                print(f"❌ Ping to {endpoint}: FAILED")
                results.append({"endpoint": endpoint, "status": "FAILED"})
                
        except subprocess.TimeoutExpired:
            print(f"⏱️ Ping to {endpoint}: TIMEOUT")
            results.append({"endpoint": endpoint, "status": "TIMEOUT"})
        except Exception as e:
            print(f"⚠️ Ping to {endpoint}: ERROR - {e}")
            results.append({"endpoint": endpoint, "error": str(e), "status": "ERROR"})
    
    return results

def generate_report(all_results):
    """Generate a comprehensive report"""
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "test_results": all_results
    }
    
    # Count successes and failures
    total_tests = 0
    passed_tests = 0
    
    for category, results in all_results.items():
        if isinstance(results, list):
            total_tests += len(results)
            passed_tests += sum(1 for r in results if r.get("status") in ["OK", "SUCCESS", "OPEN"])
    
    report["summary"] = {
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0
    }
    
    # Save report
    with open("network_diagnostics_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📊 Network Diagnostics Summary")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Success Rate: {report['summary']['success_rate']:.1f}%")
    print(f"Report saved to: network_diagnostics_report.json")
    
    return report

def main():
    """Main diagnostics function"""
    print("🔍 SONALI Music Bot - Network Diagnostics")
    print("=" * 50)
    
    all_results = {}
    
    # Run all tests
    all_results["dns_resolution"] = test_dns_resolution()
    all_results["tcp_connectivity"] = test_tcp_connectivity()
    all_results["http_connectivity"] = test_http_connectivity()
    all_results["firewall_ports"] = check_firewall_ports()
    all_results["proxy_settings"] = check_proxy_settings()
    all_results["ping_test"] = ping_test()
    
    # Generate report
    report = generate_report(all_results)
    
    # Recommendations
    print("\n💡 Recommendations:")
    
    if report["summary"]["success_rate"] < 50:
        print("❌ Severe network issues detected!")
        print("   - Check your internet connection")
        print("   - Verify firewall settings")
        print("   - Contact your ISP if issues persist")
    elif report["summary"]["success_rate"] < 80:
        print("⚠️ Some network issues detected")
        print("   - Some Telegram endpoints may be blocked")
        print("   - Consider using a VPN or proxy")
        print("   - Check firewall/antivirus settings")
    else:
        print("✅ Network connectivity looks good!")
        print("   - Your connection should work well with Telegram")
    
    print("\n🔧 If you're still experiencing issues:")
    print("   1. Try using a VPN")
    print("   2. Check if Telegram is blocked in your region")
    print("   3. Verify your session strings are valid")
    print("   4. Ensure API_ID and API_HASH are correct")

if __name__ == "__main__":
    main()
