#!/usr/bin/env python3
"""
Tool Verification Script
Verifies tool functionality and updates verification status.
"""

import json
import sys
import os
import argparse
import requests
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import concurrent.futures
from urllib.parse import urlparse


class ToolVerifier:
    def __init__(self, max_workers: int = 5, timeout: int = 30):
        self.max_workers = max_workers
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Sunshine-AIO-Library-Verifier/1.0'
        })
    
    def verify_repository_health(self, repo_url: str) -> Dict[str, Any]:
        """Verify repository health and collect detailed metrics."""
        result = {
            "accessible": False,
            "metrics": {},
            "health_score": 0,
            "issues": [],
            "last_checked": datetime.now().isoformat()
        }
        
        try:
            # Extract repo info from URL
            if not repo_url.startswith("https://github.com/"):
                result["issues"].append("Not a GitHub repository")
                return result
            
            parts = repo_url.replace("https://github.com/", "").strip("/").split("/")
            if len(parts) != 2:
                result["issues"].append("Invalid GitHub URL format")
                return result
            
            owner, repo = parts
            api_base = f"https://api.github.com/repos/{owner}/{repo}"
            
            # Get basic repository information
            repo_response = self.session.get(api_base, timeout=self.timeout)
            if repo_response.status_code != 200:
                result["issues"].append(f"Repository API error: HTTP {repo_response.status_code}")
                return result
            
            repo_data = repo_response.json()
            
            # Check if repository is accessible
            result["accessible"] = True
            
            # Collect comprehensive metrics
            result["metrics"] = {
                "stars": repo_data.get("stargazers_count", 0),
                "forks": repo_data.get("forks_count", 0),
                "watchers": repo_data.get("watchers_count", 0),
                "open_issues": repo_data.get("open_issues_count", 0),
                "size": repo_data.get("size", 0),  # in KB
                "language": repo_data.get("language", ""),
                "license": repo_data.get("license", {}).get("spdx_id", "") if repo_data.get("license") else "",
                "created_at": repo_data.get("created_at", ""),
                "updated_at": repo_data.get("updated_at", ""),
                "pushed_at": repo_data.get("pushed_at", ""),
                "archived": repo_data.get("archived", False),
                "disabled": repo_data.get("disabled", False),
                "private": repo_data.get("private", False),
                "fork": repo_data.get("fork", False),
                "default_branch": repo_data.get("default_branch", "main"),
                "topics": repo_data.get("topics", [])
            }
            
            # Check for critical issues
            if repo_data.get("archived"):
                result["issues"].append("Repository is archived")
            if repo_data.get("disabled"):
                result["issues"].append("Repository is disabled")
            if repo_data.get("private"):
                result["issues"].append("Repository is private")
            
            # Get additional repository health indicators
            try:
                # Check for README
                readme_response = self.session.get(f"{api_base}/readme", timeout=10)
                result["metrics"]["has_readme"] = readme_response.status_code == 200
                
                # Check for recent releases
                releases_response = self.session.get(f"{api_base}/releases?per_page=1", timeout=10)
                if releases_response.status_code == 200:
                    releases = releases_response.json()
                    result["metrics"]["has_releases"] = len(releases) > 0
                    if releases:
                        result["metrics"]["latest_release"] = releases[0].get("published_at", "")
                else:
                    result["metrics"]["has_releases"] = False
                
                # Check for CI/CD (GitHub Actions)
                workflows_response = self.session.get(f"{api_base}/actions/workflows", timeout=10)
                if workflows_response.status_code == 200:
                    workflows = workflows_response.json()
                    result["metrics"]["has_ci"] = workflows.get("total_count", 0) > 0
                else:
                    result["metrics"]["has_ci"] = False
                
                # Get commit activity (last 52 weeks)
                activity_response = self.session.get(f"{api_base}/stats/commit_activity", timeout=15)
                if activity_response.status_code == 200:
                    activity = activity_response.json()
                    if activity:
                        recent_activity = sum(week["total"] for week in activity[-4:])  # Last 4 weeks
                        result["metrics"]["recent_commits"] = recent_activity
                    else:
                        result["metrics"]["recent_commits"] = 0
                else:
                    result["metrics"]["recent_commits"] = 0
                
                # Get contributors count
                contributors_response = self.session.get(f"{api_base}/contributors?per_page=1", timeout=10)
                if contributors_response.status_code == 200:
                    # GitHub returns the count in the Link header for pagination
                    link_header = contributors_response.headers.get('Link', '')
                    if 'last' in link_header:
                        # Extract last page number
                        import re
                        match = re.search(r'page=(\d+)>; rel="last"', link_header)
                        result["metrics"]["contributors"] = int(match.group(1)) if match else 1
                    else:
                        result["metrics"]["contributors"] = len(contributors_response.json())
                else:
                    result["metrics"]["contributors"] = 0
                
            except requests.exceptions.Timeout:
                result["issues"].append("Timeout getting additional metrics")
            except Exception as e:
                result["issues"].append(f"Error getting additional metrics: {str(e)}")
            
            # Calculate health score
            result["health_score"] = self._calculate_health_score(result["metrics"], result["issues"])
            
        except requests.exceptions.Timeout:
            result["issues"].append("Repository request timeout")
        except requests.exceptions.ConnectionError:
            result["issues"].append("Connection error")
        except Exception as e:
            result["issues"].append(f"Verification error: {str(e)}")
        
        return result
    
    def _calculate_health_score(self, metrics: Dict[str, Any], issues: List[str]) -> int:
        """Calculate repository health score (0-100)."""
        score = 100
        
        # Deduct for critical issues
        critical_issues = ["archived", "disabled", "private"]
        for issue in issues:
            if any(critical in issue.lower() for critical in critical_issues):
                score -= 50
        
        # Activity score (0-25 points)
        if metrics.get("pushed_at"):
            try:
                last_push = datetime.fromisoformat(metrics["pushed_at"].replace('Z', '+00:00'))
                days_ago = (datetime.now(last_push.tzinfo) - last_push).days
                
                if days_ago <= 30:
                    activity_score = 25
                elif days_ago <= 90:
                    activity_score = 20
                elif days_ago <= 180:
                    activity_score = 15
                elif days_ago <= 365:
                    activity_score = 10
                else:
                    activity_score = 5
                    
                score = score * 0.75 + activity_score  # 75% base + 25% activity
            except:
                score *= 0.9  # Small penalty for date parsing issues
        else:
            score *= 0.8  # Penalty for no push date
        
        # Documentation bonus
        if metrics.get("has_readme"):
            score += 5
        
        # CI/CD bonus
        if metrics.get("has_ci"):
            score += 5
        
        # Community engagement (stars, forks, contributors)
        stars = metrics.get("stars", 0)
        if stars >= 100:
            score += 10
        elif stars >= 50:
            score += 5
        elif stars >= 10:
            score += 2
        
        contributors = metrics.get("contributors", 0)
        if contributors >= 10:
            score += 5
        elif contributors >= 5:
            score += 3
        elif contributors >= 2:
            score += 1
        
        # Recent activity bonus
        recent_commits = metrics.get("recent_commits", 0)
        if recent_commits >= 10:
            score += 5
        elif recent_commits >= 5:
            score += 3
        elif recent_commits >= 1:
            score += 1
        
        return max(0, min(100, int(score)))
    
    def verify_documentation(self, doc_url: str) -> Dict[str, Any]:
        """Verify documentation accessibility and quality."""
        result = {
            "accessible": False,
            "status_code": None,
            "content_type": "",
            "response_time": 0,
            "issues": [],
            "last_checked": datetime.now().isoformat()
        }
        
        if not doc_url:
            result["issues"].append("No documentation URL provided")
            return result
        
        try:
            start_time = time.time()
            response = self.session.head(doc_url, timeout=self.timeout, allow_redirects=True)
            result["response_time"] = time.time() - start_time
            result["status_code"] = response.status_code
            result["content_type"] = response.headers.get("content-type", "")
            
            if response.status_code in [200, 301, 302]:
                result["accessible"] = True
            else:
                result["issues"].append(f"HTTP {response.status_code}")
            
            # Check if it's likely to be documentation
            if "text/html" not in result["content_type"] and result["accessible"]:
                result["issues"].append("May not be HTML documentation")
                
        except requests.exceptions.Timeout:
            result["issues"].append("Documentation timeout")
        except requests.exceptions.ConnectionError:
            result["issues"].append("Connection error")
        except Exception as e:
            result["issues"].append(f"Error: {str(e)}")
        
        return result
    
    def verify_single_tool(self, tool_path: Path) -> Dict[str, Any]:
        """Verify a single tool entry."""
        result = {
            "file": str(tool_path),
            "status": "unknown",
            "repository": {},
            "documentation": {},
            "overall_score": 0,
            "verification_date": datetime.now().isoformat(),
            "issues": []
        }
        
        try:
            # Load tool data
            with open(tool_path, 'r') as f:
                tool_data = json.load(f)
            
            # Verify repository
            repo_url = tool_data.get("repository", "")
            if repo_url:
                print(f"🔍 Verifying repository: {repo_url}")
                result["repository"] = self.verify_repository_health(repo_url)
            else:
                result["issues"].append("No repository URL provided")
            
            # Verify documentation
            doc_url = tool_data.get("documentation", "")
            if doc_url:
                print(f"📚 Verifying documentation: {doc_url}")
                result["documentation"] = self.verify_documentation(doc_url)
            
            # Calculate overall score
            repo_score = result["repository"].get("health_score", 0)
            doc_accessible = result["documentation"].get("accessible", False) if doc_url else True
            doc_bonus = 10 if doc_accessible else -5
            
            result["overall_score"] = min(100, max(0, repo_score + doc_bonus))
            
            # Determine status
            if result["repository"].get("accessible", False):
                if result["overall_score"] >= 80:
                    result["status"] = "verified"
                elif result["overall_score"] >= 60:
                    result["status"] = "conditional"
                else:
                    result["status"] = "needs_review"
            else:
                result["status"] = "failed"
            
        except FileNotFoundError:
            result["issues"].append("Tool file not found")
            result["status"] = "failed"
        except json.JSONDecodeError as e:
            result["issues"].append(f"Invalid JSON: {e}")
            result["status"] = "failed"
        except Exception as e:
            result["issues"].append(f"Verification error: {str(e)}")
            result["status"] = "failed"
        
        return result
    
    def verify_tools_batch(self, tool_paths: List[Path]) -> List[Dict[str, Any]]:
        """Verify multiple tools in parallel."""
        results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all verification tasks
            future_to_path = {
                executor.submit(self.verify_single_tool, path): path 
                for path in tool_paths
            }
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_path):
                try:
                    result = future.result()
                    results.append(result)
                    
                    # Print progress
                    status_emoji = {
                        "verified": "✅",
                        "conditional": "⚠️", 
                        "needs_review": "🔍",
                        "failed": "❌",
                        "unknown": "❓"
                    }
                    emoji = status_emoji.get(result["status"], "❓")
                    print(f"{emoji} {Path(result['file']).name} (Score: {result['overall_score']})")
                    
                except Exception as e:
                    path = future_to_path[future]
                    print(f"❌ Error verifying {path}: {e}")
                    results.append({
                        "file": str(path),
                        "status": "failed",
                        "issues": [str(e)],
                        "overall_score": 0
                    })
        
        return results
    
    def update_tool_verification(self, tool_path: Path, verification_result: Dict[str, Any]) -> bool:
        """Update tool file with verification results."""
        try:
            # Load current tool data
            with open(tool_path, 'r') as f:
                tool_data = json.load(f)
            
            # Update verification section
            tool_data["verification"] = {
                "status": verification_result["status"],
                "date": verification_result["verification_date"],
                "method": "automated",
                "score": verification_result["overall_score"]
            }
            
            # Update metrics if available
            if verification_result["repository"].get("metrics"):
                tool_data["metrics"] = {
                    "stars": verification_result["repository"]["metrics"].get("stars", 0),
                    "forks": verification_result["repository"]["metrics"].get("forks", 0),
                    "last_commit": verification_result["repository"]["metrics"].get("pushed_at", "").split("T")[0] if verification_result["repository"]["metrics"].get("pushed_at") else None
                }
            
            # Write updated data back
            with open(tool_path, 'w') as f:
                json.dump(tool_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to update {tool_path}: {e}")
            return False


def print_verification_summary(results: List[Dict[str, Any]]):
    """Print verification results summary."""
    total = len(results)
    status_counts = {}
    
    for result in results:
        status = result["status"]
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print(f"\n📊 Verification Summary ({total} tools)")
    print(f"✅ Verified: {status_counts.get('verified', 0)}")
    print(f"⚠️ Conditional: {status_counts.get('conditional', 0)}")
    print(f"🔍 Needs Review: {status_counts.get('needs_review', 0)}")
    print(f"❌ Failed: {status_counts.get('failed', 0)}")
    print(f"❓ Unknown: {status_counts.get('unknown', 0)}")
    
    # Show average scores by status
    if results:
        print(f"\n📈 Average Scores:")
        for status in status_counts:
            scores = [r["overall_score"] for r in results if r["status"] == status]
            if scores:
                avg_score = sum(scores) / len(scores)
                print(f"  {status}: {avg_score:.1f}")


def main():
    parser = argparse.ArgumentParser(description="Verify Sunshine-AIO tool entries")
    parser.add_argument("--single", "-s", type=str, help="Verify a single tool file")
    parser.add_argument("--tools-dir", "-d", type=str, help="Tools directory path")
    parser.add_argument("--update", "-u", action="store_true", help="Update tool files with verification results")
    parser.add_argument("--workers", "-w", type=int, default=5, help="Number of worker threads")
    parser.add_argument("--timeout", "-t", type=int, default=30, help="Request timeout in seconds")
    
    args = parser.parse_args()
    
    # Initialize verifier
    verifier = ToolVerifier(max_workers=args.workers, timeout=args.timeout)
    
    try:
        if args.single:
            # Verify single tool
            tool_path = Path(args.single)
            print(f"🔍 Verifying: {tool_path}")
            result = verifier.verify_single_tool(tool_path)
            
            # Print detailed results
            print(f"\nStatus: {result['status']} (Score: {result['overall_score']})")
            
            if result["repository"]:
                repo = result["repository"]
                print(f"\n🏪 Repository:")
                print(f"  Accessible: {'✅' if repo.get('accessible') else '❌'}")
                print(f"  Health Score: {repo.get('health_score', 0)}")
                if repo.get("metrics"):
                    print(f"  Stars: {repo['metrics'].get('stars', 0)}")
                    print(f"  Forks: {repo['metrics'].get('forks', 0)}")
                    print(f"  Contributors: {repo['metrics'].get('contributors', 0)}")
                
                if repo.get("issues"):
                    print(f"  Issues:")
                    for issue in repo["issues"]:
                        print(f"    - {issue}")
            
            if result["documentation"]:
                doc = result["documentation"]
                print(f"\n📚 Documentation:")
                print(f"  Accessible: {'✅' if doc.get('accessible') else '❌'}")
                print(f"  Status Code: {doc.get('status_code', 'N/A')}")
                print(f"  Response Time: {doc.get('response_time', 0):.2f}s")
            
            if result["issues"]:
                print(f"\n⚠️ Issues:")
                for issue in result["issues"]:
                    print(f"  - {issue}")
            
            # Update file if requested
            if args.update:
                if verifier.update_tool_verification(tool_path, result):
                    print(f"✅ Updated {tool_path}")
                else:
                    print(f"❌ Failed to update {tool_path}")
        
        else:
            # Verify all tools
            tools_dir = Path(args.tools_dir) if args.tools_dir else Path(__file__).parent.parent / "tools"
            
            # Find all tool files
            tool_paths = list(tools_dir.rglob("*.json"))
            if not tool_paths:
                print(f"No tool files found in {tools_dir}")
                return
            
            print(f"🔍 Verifying {len(tool_paths)} tools...")
            
            # Verify all tools
            results = verifier.verify_tools_batch(tool_paths)
            
            # Print summary
            print_verification_summary(results)
            
            # Update files if requested
            if args.update:
                print(f"\n📝 Updating tool files...")
                updated = 0
                for result in results:
                    tool_path = Path(result["file"])
                    if verifier.update_tool_verification(tool_path, result):
                        updated += 1
                
                print(f"✅ Updated {updated}/{len(results)} tool files")
    
    except KeyboardInterrupt:
        print("\n⏹️ Verification interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()