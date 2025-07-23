"""
API Usage Monitor - Track your Gemini API usage and costs
Run this alongside your API to monitor usage and prevent surprises
"""

import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

class UsageMonitor:
    def __init__(self, usage_file="api_usage.json"):
        self.usage_file = usage_file
        self.load_usage()
        
    def load_usage(self):
        """Load usage data from file"""
        if os.path.exists(self.usage_file):
            with open(self.usage_file, 'r') as f:
                self.usage = json.load(f)
        else:
            self.usage = {
                "daily": defaultdict(int),
                "monthly": defaultdict(int),
                "total_requests": 0,
                "total_cost": 0.0
            }
    
    def save_usage(self):
        """Save usage data to file"""
        # Convert defaultdict to regular dict for JSON
        usage_data = {
            "daily": dict(self.usage["daily"]),
            "monthly": dict(self.usage["monthly"]),
            "total_requests": self.usage["total_requests"],
            "total_cost": self.usage["total_cost"]
        }
        with open(self.usage_file, 'w') as f:
            json.dump(usage_data, f, indent=2)
    
    def track_request(self, tokens_in=2000, tokens_out=1000):
        """Track a single API request"""
        today = datetime.now().strftime("%Y-%m-%d")
        month = datetime.now().strftime("%Y-%m")
        
        # Update counters
        self.usage["daily"][today] = self.usage["daily"].get(today, 0) + 1
        self.usage["monthly"][month] = self.usage["monthly"].get(month, 0) + 1
        self.usage["total_requests"] += 1
        
        # Calculate cost (Gemini 1.5 Flash pricing)
        # Free tier: 1,500 requests/day
        daily_count = self.usage["daily"][today]
        if daily_count > 1500:
            # Paid tier pricing
            cost_in = (tokens_in / 1_000_000) * 0.075
            cost_out = (tokens_out / 1_000_000) * 0.30
            request_cost = cost_in + cost_out
            self.usage["total_cost"] += request_cost
        else:
            request_cost = 0
        
        self.save_usage()
        return daily_count, request_cost
    
    def get_daily_stats(self):
        """Get today's usage statistics"""
        today = datetime.now().strftime("%Y-%m-%d")
        daily_count = self.usage["daily"].get(today, 0)
        free_remaining = max(0, 1500 - daily_count)
        
        return {
            "date": today,
            "requests": daily_count,
            "free_remaining": free_remaining,
            "is_paid_tier": daily_count > 1500
        }
    
    def get_monthly_stats(self):
        """Get this month's usage statistics"""
        month = datetime.now().strftime("%Y-%m")
        monthly_count = self.usage["monthly"].get(month, 0)
        
        # Estimate monthly cost
        avg_daily = monthly_count / datetime.now().day
        projected_monthly = avg_daily * 30
        
        # Calculate costs (assuming average distribution)
        free_requests = min(projected_monthly, 1500 * 30)
        paid_requests = max(0, projected_monthly - free_requests)
        estimated_cost = paid_requests * 0.00045  # Average cost per resume
        
        return {
            "month": month,
            "requests": monthly_count,
            "projected_total": int(projected_monthly),
            "estimated_cost": estimated_cost
        }
    
    def print_summary(self):
        """Print usage summary"""
        daily = self.get_daily_stats()
        monthly = self.get_monthly_stats()
        
        print("\n📊 API USAGE SUMMARY")
        print("=" * 50)
        
        print(f"\n📅 Today ({daily['date']}):")
        print(f"   Requests: {daily['requests']:,}")
        print(f"   Free remaining: {daily['free_remaining']:,}")
        if daily['is_paid_tier']:
            print("   ⚠️  NOW USING PAID TIER")
        
        print(f"\n📆 This Month ({monthly['month']}):")
        print(f"   Requests: {monthly['requests']:,}")
        print(f"   Projected total: {monthly['projected_total']:,}")
        print(f"   Estimated cost: ${monthly['estimated_cost']:.2f}")
        
        print(f"\n💰 All-time:")
        print(f"   Total requests: {self.usage['total_requests']:,}")
        print(f"   Total cost: ${self.usage['total_cost']:.2f}")
        
        print("\n💡 Tips:")
        if daily['free_remaining'] < 100:
            print("   ⚠️  Low on free tier requests today!")
        if monthly['estimated_cost'] > 50:
            print("   📈 Consider raising prices - high volume!")
        print("   ✅ Remember: Even with costs, you have 99%+ margins!")

# Example usage in your app.py:
# monitor = UsageMonitor()
# daily_count, cost = monitor.track_request()
# if daily_count % 100 == 0:
#     monitor.print_summary()

if __name__ == "__main__":
    # Test the monitor
    monitor = UsageMonitor()
    monitor.print_summary()
