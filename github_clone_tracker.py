#!/usr/bin/env python3
"""
GitHub Clone Tracker - Automated Data Collection
Fetches clone traffic data for all repositories and stores it incrementally.
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, Any
import sys


class CloneTracker:
    def __init__(self):
        self.token = os.environ.get('GITHUB_TOKEN')
        self.username = os.environ.get('GITHUB_USERNAME')
        self.data_file = 'clone_data.json'
        
        if not self.token:
            print("❌ Error: GITHUB_TOKEN environment variable not set")
            sys.exit(1)
        
        if not self.username:
            print("❌ Error: GITHUB_USERNAME environment variable not set")
            sys.exit(1)
        
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Load existing data
        self.data = self.load_data()
    
    def load_data(self) -> Dict[str, Any]:
        """Load existing clone data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("⚠️  Warning: Could not parse existing data file, starting fresh")
        
        # Default structure
        return {
            'repositories': {},
            'cumulative': {},
            'last_updated': None
        }
    
    def save_data(self):
        """Save clone data to JSON file"""
        self.data['last_updated'] = datetime.now().isoformat()
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
        print(f"✅ Data saved to {self.data_file}")
    
    def get_all_repositories(self):
        """Fetch all repositories for the authenticated user"""
        repos = []
        page = 1
        
        while True:
            url = f'https://api.github.com/user/repos?per_page=100&page={page}&type=owner'
            response = requests.get(url, headers=self.headers)
            
            if response.status_code != 200:
                print(f"❌ Error fetching repositories: {response.status_code}")
                print(response.json())
                break
            
            page_repos = response.json()
            if not page_repos:
                break
            
            repos.extend(page_repos)
            page += 1
        
        print(f"📦 Found {len(repos)} repositories")
        return repos
    
    def get_clone_stats(self, repo_name: str):
        """Fetch clone statistics for a specific repository"""
        url = f'https://api.github.com/repos/{self.username}/{repo_name}/traffic/clones'
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            print(f"⚠️  No access to clone stats for {repo_name} (might be private without proper permissions)")
            return None
        else:
            print(f"⚠️  Error fetching clone stats for {repo_name}: {response.status_code}")
            return None
    
    def process_repository(self, repo_name: str):
        """Process clone statistics for a single repository"""
        stats = self.get_clone_stats(repo_name)
        
        if not stats or 'clones' not in stats:
            return
        
        # Initialize repository data if it doesn't exist
        if repo_name not in self.data['repositories']:
            self.data['repositories'][repo_name] = {'daily_clones': {}}
        
        repo_data = self.data['repositories'][repo_name]
        
        # Store daily clone data
        for clone_day in stats['clones']:
            date = clone_day['timestamp'][:10]  # Extract YYYY-MM-DD
            count = clone_day['count']
            uniques = clone_day['uniques']
            
            # Only update if we don't have this date or if the data is newer
            if date not in repo_data['daily_clones'] or clone_day['count'] > repo_data['daily_clones'][date]['count']:
                repo_data['daily_clones'][date] = {
                    'count': count,
                    'uniques': uniques
                }
        
        print(f"  ✓ {repo_name}: {len(stats['clones'])} days of data")
    
    def calculate_cumulative_stats(self):
        """Calculate cumulative statistics across all repositories"""
        cumulative = {}
        
        for repo_name, repo_data in self.data['repositories'].items():
            for date, day_data in repo_data['daily_clones'].items():
                if date not in cumulative:
                    cumulative[date] = {'total_clones': 0, 'unique_users': set()}
                
                cumulative[date]['total_clones'] += day_data['count']
                # Note: We can't accurately track unique users across repos
                # so we'll track unique cloners per repo
        
        # Convert to sorted list and calculate running totals
        sorted_dates = sorted(cumulative.keys())
        running_total_clones = 0
        
        self.data['cumulative'] = {}
        for date in sorted_dates:
            running_total_clones += cumulative[date]['total_clones']
            self.data['cumulative'][date] = {
                'total_clones': running_total_clones,
                'daily_clones': cumulative[date]['total_clones']
            }
    
    def run(self):
        """Main execution function"""
        print("🚀 Starting GitHub Clone Tracker")
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"👤 User: {self.username}\n")
        
        # Fetch all repositories
        repos = self.get_all_repositories()
        
        # Process each repository
        print("\n📊 Fetching clone statistics...\n")
        for repo in repos:
            self.process_repository(repo['name'])
        
        # Calculate cumulative statistics
        print("\n🧮 Calculating cumulative statistics...")
        self.calculate_cumulative_stats()
        
        # Save data
        self.save_data()
        
        # Print summary
        total_repos_with_data = len([r for r in self.data['repositories'].values() if r['daily_clones']])
        total_days_tracked = len(self.data['cumulative'])
        
        if total_days_tracked > 0:
            latest_date = max(self.data['cumulative'].keys())
            total_clones = self.data['cumulative'][latest_date]['total_clones']
        else:
            total_clones = 0
        
        print(f"\n" + "="*50)
        print(f"📈 Summary:")
        print(f"  • Repositories with clone data: {total_repos_with_data}/{len(repos)}")
        print(f"  • Days tracked: {total_days_tracked}")
        print(f"  • Total clones (cumulative): {total_clones}")
        print("="*50 + "\n")


if __name__ == '__main__':
    tracker = CloneTracker()
    tracker.run()
