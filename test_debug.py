#!/usr/bin/env python3
"""
Debug Testing Script for ETL Sidecar
Tests all endpoints and functionality in debug mode
"""

import requests
import json
import time
import sys
from typing import Dict, Any

class ETLSidecarDebugTester:
    def __init__(self, base_url: str = "http://localhost:3009"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
    
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   📝 {details}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": time.time()
        })
    
    def test_health_check(self):
        """Test health check endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/healthz", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "Health Check",
                    True,
                    f"Status: {data.get('status')}, Model: {data.get('model')}"
                )
                return data
            else:
                self.log_test("Health Check", False, f"Status code: {response.status_code}")
                return None
                
        except Exception as e:
            self.log_test("Health Check", False, f"Error: {str(e)}")
            return None
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "Root Endpoint",
                    True,
                    f"Service: {data.get('service')}, Version: {data.get('version')}"
                )
                return data
            else:
                self.log_test("Root Endpoint", False, f"Status code: {response.status_code}")
                return None
                
        except Exception as e:
            self.log_test("Root Endpoint", False, f"Error: {str(e)}")
            return None
    
    def test_similarity_calculation(self):
        """Test similarity calculation endpoint"""
        try:
            test_data = {
                "headers": ["customer_name", "email_address", "phone_number", "created_date"],
                "canonicalFields": ["name", "email", "phone", "created_at", "address"]
            }
            
            start_time = time.time()
            response = self.session.post(
                f"{self.base_url}/similarity/headers",
                json=test_data,
                timeout=30
            )
            processing_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                similarities = data.get('similarities', [])
                
                self.log_test(
                    "Similarity Calculation",
                    True,
                    f"Matrix: {len(similarities)}x{len(similarities[0]) if similarities else 0}, "
                    f"Time: {processing_time:.3f}s"
                )
                
                # Log similarity matrix
                print("   📊 Similarity Matrix:")
                for i, header in enumerate(test_data["headers"]):
                    for j, canonical in enumerate(test_data["canonicalFields"]):
                        score = similarities[i][j]
                        print(f"     {header} → {canonical}: {score:.3f}")
                
                return data
            else:
                self.log_test("Similarity Calculation", False, f"Status code: {response.status_code}")
                return None
                
        except Exception as e:
            self.log_test("Similarity Calculation", False, f"Error: {str(e)}")
            return None
    
    def test_debug_stats(self):
        """Test debug stats endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/debug/stats", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                stats = data.get('stats', {})
                
                self.log_test(
                    "Debug Stats",
                    True,
                    f"Requests: {stats.get('request_count')}, "
                    f"Memory: {stats.get('memory', {}).get('percent', 0):.1f}%"
                )
                return data
            else:
                self.log_test("Debug Stats", False, f"Status code: {response.status_code}")
                return None
                
        except Exception as e:
            self.log_test("Debug Stats", False, f"Error: {str(e)}")
            return None
    
    def test_debug_test(self):
        """Test debug test endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/debug/test", timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                self.log_test(
                    "Debug Test",
                    True,
                    f"Status: {data.get('status')}"
                )
                return data
            else:
                self.log_test("Debug Test", False, f"Status code: {response.status_code}")
                return None
                
        except Exception as e:
            self.log_test("Debug Test", False, f"Error: {str(e)}")
            return None
    
    def test_performance(self, num_requests: int = 5):
        """Test performance with multiple requests"""
        print(f"\n🚀 Performance Test ({num_requests} requests)")
        
        test_data = {
            "headers": ["customer_name", "email_address"],
            "canonicalFields": ["name", "email", "phone"]
        }
        
        times = []
        successes = 0
        
        for i in range(num_requests):
            try:
                start_time = time.time()
                response = self.session.post(
                    f"{self.base_url}/similarity/headers",
                    json=test_data,
                    timeout=30
                )
                processing_time = time.time() - start_time
                
                if response.status_code == 200:
                    times.append(processing_time)
                    successes += 1
                    print(f"   Request {i+1}: {processing_time:.3f}s")
                else:
                    print(f"   Request {i+1}: FAILED (Status: {response.status_code})")
                    
            except Exception as e:
                print(f"   Request {i+1}: ERROR ({str(e)})")
        
        if times:
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            
            self.log_test(
                "Performance Test",
                successes == num_requests,
                f"Success: {successes}/{num_requests}, "
                f"Avg: {avg_time:.3f}s, Min: {min_time:.3f}s, Max: {max_time:.3f}s"
            )
        else:
            self.log_test("Performance Test", False, "No successful requests")
    
    def test_error_handling(self):
        """Test error handling with invalid requests"""
        print("\n🔍 Error Handling Test")
        
        # Test with invalid JSON
        try:
            response = self.session.post(
                f"{self.base_url}/similarity/headers",
                data="invalid json",
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            self.log_test("Invalid JSON", response.status_code == 422, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Invalid JSON", False, f"Error: {str(e)}")
        
        # Test with missing fields
        try:
            response = self.session.post(
                f"{self.base_url}/similarity/headers",
                json={"headers": ["test"]},  # Missing canonicalFields
                timeout=10
            )
            self.log_test("Missing Fields", response.status_code == 422, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Missing Fields", False, f"Error: {str(e)}")
        
        # Test with empty arrays
        try:
            response = self.session.post(
                f"{self.base_url}/similarity/headers",
                json={"headers": [], "canonicalFields": []},
                timeout=10
            )
            self.log_test("Empty Arrays", response.status_code == 200, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Empty Arrays", False, f"Error: {str(e)}")
    
    def run_all_tests(self):
        """Run all debug tests"""
        print("🧪 ETL Sidecar Debug Test Suite")
        print("=" * 50)
        
        # Basic endpoint tests
        print("\n📋 Basic Endpoint Tests")
        self.test_health_check()
        self.test_root_endpoint()
        
        # Core functionality tests
        print("\n🔧 Core Functionality Tests")
        self.test_similarity_calculation()
        
        # Debug-specific tests
        print("\n🐛 Debug-Specific Tests")
        self.test_debug_stats()
        self.test_debug_test()
        
        # Performance tests
        self.test_performance(3)
        
        # Error handling tests
        self.test_error_handling()
        
        # Summary
        print("\n📊 Test Summary")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ Failed Tests:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['details']}")
        
        return passed_tests == total_tests

def main():
    """Main test runner"""
    import argparse
    
    parser = argparse.ArgumentParser(description="ETL Sidecar Debug Tester")
    parser.add_argument("--url", default="http://localhost:3009", help="Base URL for the service")
    parser.add_argument("--wait", type=int, default=5, help="Wait time before starting tests (seconds)")
    
    args = parser.parse_args()
    
    print(f"🔗 Testing ETL Sidecar at: {args.url}")
    print(f"⏳ Waiting {args.wait} seconds for service to be ready...")
    time.sleep(args.wait)
    
    tester = ETLSidecarDebugTester(args.url)
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed! ETL Sidecar is working correctly.")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed. Check the output above for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()

