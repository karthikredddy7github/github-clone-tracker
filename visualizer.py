#!/usr/bin/env python3
"""
GitHub Clone Statistics Visualizer
Generates graphs and charts from collected clone data.
"""

import json
import os
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for GitHub Actions
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import defaultdict


class CloneVisualizer:
    def __init__(self, data_file='clone_data.json'):
        self.data_file = data_file
        self.output_dir = 'graphs'
        self.data = self.load_data()
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def load_data(self):
        """Load clone data from JSON file"""
        if not os.path.exists(self.data_file):
            print(f"❌ Error: {self.data_file} not found. Run github_clone_tracker.py first.")
            return None
        
        with open(self.data_file, 'r') as f:
            return json.load(f)
    
    def plot_cumulative_clones(self):
        """Generate cumulative total clones graph"""
        if not self.data or not self.data['cumulative']:
            print("⚠️  No cumulative data available")
            return
        
        dates = sorted(self.data['cumulative'].keys())
        totals = [self.data['cumulative'][d]['total_clones'] for d in dates]
        
        # Convert dates to datetime objects
        date_objects = [datetime.strptime(d, '%Y-%m-%d') for d in dates]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(date_objects, totals, marker='o', linewidth=2, markersize=4, color='#2E86AB')
        ax.fill_between(date_objects, totals, alpha=0.3, color='#2E86AB')
        
        ax.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax.set_ylabel('Total Clones', fontsize=12, fontweight='bold')
        ax.set_title('📈 Cumulative Repository Clones Over Time', fontsize=14, fontweight='bold', pad=20)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.xticks(rotation=45, ha='right')
        
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        output_path = os.path.join(self.output_dir, 'cumulative_clones.png')
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Saved: {output_path}")
    
    def plot_daily_activity(self):
        """Generate daily clone activity chart"""
        if not self.data or not self.data['cumulative']:
            print("⚠️  No cumulative data available")
            return
        
        dates = sorted(self.data['cumulative'].keys())
        daily_clones = [self.data['cumulative'][d]['daily_clones'] for d in dates]
        
        # Convert dates to datetime objects
        date_objects = [datetime.strptime(d, '%Y-%m-%d') for d in dates]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(date_objects, daily_clones, color='#A23B72', alpha=0.7, edgecolor='black')
        
        ax.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax.set_ylabel('Daily Clones', fontsize=12, fontweight='bold')
        ax.set_title('📊 Daily Clone Activity', fontsize=14, fontweight='bold', pad=20)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.xticks(rotation=45, ha='right')
        
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        output_path = os.path.join(self.output_dir, 'daily_activity.png')
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Saved: {output_path}")
    
    def plot_repository_breakdown(self):
        """Generate per-repository breakdown chart"""
        if not self.data or not self.data['repositories']:
            print("⚠️  No repository data available")
            return
        
        # Calculate total clones per repository
        repo_totals = {}
        for repo_name, repo_data in self.data['repositories'].items():
            total = sum(day['count'] for day in repo_data['daily_clones'].values())
            if total > 0:  # Only include repos with clones
                repo_totals[repo_name] = total
        
        if not repo_totals:
            print("⚠️  No repository clone data available")
            return
        
        # Sort by total clones (descending) and take top 15
        sorted_repos = sorted(repo_totals.items(), key=lambda x: x[1], reverse=True)[:15]
        repos, totals = zip(*sorted_repos)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        bars = ax.barh(repos, totals, color='#F18F01', edgecolor='black', alpha=0.8)
        
        # Add value labels on bars
        for bar in bars:
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2, 
                   f'{int(width)}', ha='left', va='center', fontweight='bold', fontsize=9)
        
        ax.set_xlabel('Total Clones', fontsize=12, fontweight='bold')
        ax.set_ylabel('Repository', fontsize=12, fontweight='bold')
        ax.set_title('🏆 Top Repositories by Clone Count', fontsize=14, fontweight='bold', pad=20)
        
        ax.grid(True, alpha=0.3, axis='x')
        plt.tight_layout()
        
        output_path = os.path.join(self.output_dir, 'repository_breakdown.png')
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Saved: {output_path}")
    
    def plot_repository_trend(self):
        """Generate trend chart showing top repositories over time"""
        if not self.data or not self.data['repositories']:
            print("⚠️  No repository data available")
            return
        
        # Calculate total clones per repository
        repo_totals = {}
        for repo_name, repo_data in self.data['repositories'].items():
            total = sum(day['count'] for day in repo_data['daily_clones'].values())
            if total > 0:
                repo_totals[repo_name] = total
        
        # Get top 5 repositories
        top_repos = sorted(repo_totals.items(), key=lambda x: x[1], reverse=True)[:5]
        
        if not top_repos:
            print("⚠️  No repository clone data available for trend chart")
            return
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E']
        
        for idx, (repo_name, _) in enumerate(top_repos):
            repo_data = self.data['repositories'][repo_name]['daily_clones']
            
            # Build cumulative data for this repo
            dates = sorted(repo_data.keys())
            cumulative = []
            total = 0
            
            for date in dates:
                total += repo_data[date]['count']
                cumulative.append(total)
            
            date_objects = [datetime.strptime(d, '%Y-%m-%d') for d in dates]
            
            ax.plot(date_objects, cumulative, marker='o', linewidth=2, 
                   markersize=3, label=repo_name, color=colors[idx % len(colors)])
        
        ax.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax.set_ylabel('Cumulative Clones', fontsize=12, fontweight='bold')
        ax.set_title('📈 Top 5 Repositories - Clone Trends', fontsize=14, fontweight='bold', pad=20)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.xticks(rotation=45, ha='right')
        
        ax.legend(loc='upper left', framealpha=0.9)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        output_path = os.path.join(self.output_dir, 'repository_trends.png')
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Saved: {output_path}")
    
    def generate_stats_summary(self):
        """Generate a text summary of statistics"""
        if not self.data:
            return
        
        summary_lines = []
        summary_lines.append("# 📊 Clone Statistics Summary\n")
        summary_lines.append(f"**Last Updated:** {self.data.get('last_updated', 'Unknown')}\n\n")
        
        # Overall stats
        if self.data['cumulative']:
            latest_date = max(self.data['cumulative'].keys())
            total_clones = self.data['cumulative'][latest_date]['total_clones']
            days_tracked = len(self.data['cumulative'])
            
            summary_lines.append("## Overall Statistics\n")
            summary_lines.append(f"- **Total Clones (All Time):** {total_clones:,}\n")
            summary_lines.append(f"- **Days Tracked:** {days_tracked}\n")
            summary_lines.append(f"- **Average Daily Clones:** {total_clones / days_tracked:.1f}\n\n")
        
        # Repository stats
        repos_with_data = [r for r in self.data['repositories'].values() if r['daily_clones']]
        summary_lines.append(f"## Repository Statistics\n")
        summary_lines.append(f"- **Repositories Tracked:** {len(repos_with_data)}\n\n")
        
        # Top repositories
        if self.data['repositories']:
            repo_totals = {}
            for repo_name, repo_data in self.data['repositories'].items():
                total = sum(day['count'] for day in repo_data['daily_clones'].values())
                if total > 0:
                    repo_totals[repo_name] = total
            
            if repo_totals:
                summary_lines.append("## Top 10 Repositories by Clones\n")
                sorted_repos = sorted(repo_totals.items(), key=lambda x: x[1], reverse=True)[:10]
                
                for idx, (repo, count) in enumerate(sorted_repos, 1):
                    summary_lines.append(f"{idx}. **{repo}**: {count:,} clones\n")
        
        output_path = os.path.join(self.output_dir, 'STATS_SUMMARY.md')
        with open(output_path, 'w') as f:
            f.writelines(summary_lines)
        
        print(f"✅ Saved: {output_path}")
    
    def run(self):
        """Generate all visualizations"""
        if not self.data:
            return
        
        print("🎨 Generating visualizations...\n")
        
        self.plot_cumulative_clones()
        self.plot_daily_activity()
        self.plot_repository_breakdown()
        self.plot_repository_trend()
        self.generate_stats_summary()
        
        print(f"\n✨ All visualizations saved to '{self.output_dir}/' directory")


if __name__ == '__main__':
    visualizer = CloneVisualizer()
    visualizer.run()
