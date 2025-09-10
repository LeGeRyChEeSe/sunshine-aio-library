#!/usr/bin/env python3
"""
Tool Entry Validation Script
Validates tool entries against JSON schema and performs additional checks.
"""

import json
import sys
import os
import argparse
import requests
import jsonschema
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime
import re


class ToolValidator:
    def __init__(self, schema_dir: Path = None):
        self.schema_dir = schema_dir or Path(__file__).parent.parent / "schemas"
        self.tool_schema = self._load_schema("tool-entry.json")
        self.validation_rules = self._load_schema("validation-rules.json")
        
    def _load_schema(self, filename: str) -> Dict[str, Any]:
        """Load JSON schema from file."""
        schema_path = self.schema_dir / filename
        try:
            with open(schema_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Schema file not found: {schema_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in schema {filename}: {e}")
            sys.exit(1)
    
    def _load_tool_entry(self, tool_path: Path) -> Dict[str, Any]:
        """Load tool entry from JSON file."""
        try:
            with open(tool_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise ValidationError(f"Tool file not found: {tool_path}")
        except json.JSONDecodeError as e:
            raise ValidationError(f"Invalid JSON in {tool_path}: {e}")
    
    def validate_schema(self, tool_data: Dict[str, Any]) -> List[str]:
        """Validate tool entry against JSON schema."""
        errors = []
        try:
            jsonschema.validate(tool_data, self.tool_schema)
        except jsonschema.ValidationError as e:
            errors.append(f"Schema validation failed: {e.message}")
            if e.absolute_path:
                errors.append(f"  Path: {' -> '.join(str(p) for p in e.absolute_path)}")
        except jsonschema.SchemaError as e:
            errors.append(f"Schema error: {e.message}")
        
        return errors
    
    def validate_url_accessibility(self, url: str, timeout: int = 10) -> Tuple[bool, str]:
        """Check if URL is accessible."""
        try:
            response = requests.head(url, timeout=timeout, allow_redirects=True)
            allowed_codes = self.validation_rules["properties"]["url_validation"]["properties"]["required_status_codes"]["default"]
            
            if response.status_code in allowed_codes:
                return True, f"✅ URL accessible (HTTP {response.status_code})"
            else:
                return False, f"❌ URL returned HTTP {response.status_code}"
                
        except requests.exceptions.Timeout:
            return False, "❌ URL timeout"
        except requests.exceptions.ConnectionError:
            return False, "❌ Connection error"
        except Exception as e:
            return False, f"❌ Error checking URL: {str(e)}"
    
    def validate_github_repository(self, repo_url: str) -> Tuple[bool, str, Dict[str, Any]]:
        """Validate GitHub repository and collect metrics."""
        if not repo_url.startswith("https://github.com/"):
            return False, "❌ Not a GitHub URL", {}
        
        # Extract owner/repo from URL
        match = re.match(r'https://github\.com/([^/]+)/([^/]+)/?$', repo_url)
        if not match:
            return False, "❌ Invalid GitHub URL format", {}
        
        owner, repo = match.groups()
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        
        try:
            response = requests.get(api_url, timeout=10)
            if response.status_code == 404:
                return False, "❌ Repository not found", {}
            elif response.status_code != 200:
                return False, f"❌ GitHub API error (HTTP {response.status_code})", {}
            
            repo_data = response.json()
            metrics = {
                "stars": repo_data.get("stargazers_count", 0),
                "forks": repo_data.get("forks_count", 0),
                "last_commit": repo_data.get("pushed_at", "").split("T")[0] if repo_data.get("pushed_at") else None,
                "language": repo_data.get("language", ""),
                "license": repo_data.get("license", {}).get("spdx_id", "") if repo_data.get("license") else "",
                "archived": repo_data.get("archived", False),
                "disabled": repo_data.get("disabled", False)
            }
            
            warnings = []
            if repo_data.get("archived"):
                warnings.append("⚠️ Repository is archived")
            if repo_data.get("disabled"):
                warnings.append("⚠️ Repository is disabled")
            if metrics["stars"] < self.validation_rules["properties"]["quality_thresholds"]["properties"]["minimum_stars"]["default"]:
                warnings.append(f"⚠️ Low star count ({metrics['stars']})")
            
            status = "✅ Repository accessible" + (f" ({', '.join(warnings)})" if warnings else "")
            return True, status, metrics
            
        except Exception as e:
            return False, f"❌ Error accessing repository: {str(e)}", {}
    
    def validate_content_safety(self, tool_data: Dict[str, Any]) -> List[str]:
        """Check for potentially unsafe content."""
        warnings = []
        forbidden_words = self.validation_rules["properties"]["content_validation"]["properties"]["forbidden_words"]["default"]
        
        text_fields = [
            tool_data.get("name", ""),
            tool_data.get("description", ""),
            " ".join(tool_data.get("tags", []))
        ]
        
        for field in text_fields:
            field_lower = field.lower()
            for word in forbidden_words:
                if word in field_lower:
                    warnings.append(f"⚠️ Contains potentially unsafe word: '{word}'")
        
        return warnings
    
    def calculate_quality_score(self, tool_data: Dict[str, Any], metrics: Dict[str, Any]) -> int:
        """Calculate quality score based on various metrics."""
        weights = self.validation_rules["properties"]["scoring_weights"]["properties"]
        score = 0
        
        # Stars score (0-30 points)
        stars = metrics.get("stars", 0)
        stars_score = min(30, stars * 0.5)  # 0.5 points per star, max 30
        score += stars_score * weights["stars"]["default"]
        
        # Forks score (0-20 points)
        forks = metrics.get("forks", 0)
        forks_score = min(20, forks * 2)  # 2 points per fork, max 20
        score += forks_score * weights["forks"]["default"]
        
        # Recent activity (0-20 points)
        if metrics.get("last_commit"):
            try:
                last_commit = datetime.strptime(metrics["last_commit"], "%Y-%m-%d")
                days_ago = (datetime.now() - last_commit).days
                if days_ago <= 30:
                    activity_score = 20
                elif days_ago <= 90:
                    activity_score = 15
                elif days_ago <= 365:
                    activity_score = 10
                else:
                    activity_score = 5
            except:
                activity_score = 5
        else:
            activity_score = 0
        score += activity_score * weights["recent_activity"]["default"]
        
        # Documentation (0-15 points)
        doc_score = 0
        if tool_data.get("documentation"):
            doc_score += 10
        if len(tool_data.get("description", "")) > 50:
            doc_score += 5
        score += doc_score * weights["documentation"]["default"]
        
        # License (0-10 points)
        if tool_data.get("license"):
            score += 10 * weights["license"]["default"]
        
        # Community (0-5 points based on complete profile)
        community_score = 0
        if tool_data.get("maintainer", {}).get("contact"):
            community_score += 2.5
        if tool_data.get("tags") and len(tool_data["tags"]) > 0:
            community_score += 2.5
        score += community_score * weights["community"]["default"]
        
        return min(100, int(score))
    
    def validate_single_tool(self, tool_path: Path) -> Dict[str, Any]:
        """Validate a single tool entry and return results."""
        results = {
            "file": str(tool_path),
            "valid": False,
            "errors": [],
            "warnings": [],
            "metrics": {},
            "score": 0
        }
        
        try:
            # Load tool data
            tool_data = self._load_tool_entry(tool_path)
            
            # Schema validation
            schema_errors = self.validate_schema(tool_data)
            if schema_errors:
                results["errors"].extend(schema_errors)
                return results
            
            # URL validation
            repo_url = tool_data["repository"]
            repo_valid, repo_status, repo_metrics = self.validate_github_repository(repo_url)
            results["metrics"] = repo_metrics
            
            if not repo_valid:
                results["errors"].append(repo_status)
                return results
            else:
                results["warnings"].append(repo_status)
            
            # Documentation URL validation (if provided)
            if tool_data.get("documentation"):
                doc_valid, doc_status = self.validate_url_accessibility(tool_data["documentation"])
                if not doc_valid:
                    results["warnings"].append(f"Documentation: {doc_status}")
                else:
                    results["warnings"].append(f"Documentation: {doc_status}")
            
            # Content safety check
            safety_warnings = self.validate_content_safety(tool_data)
            results["warnings"].extend(safety_warnings)
            
            # Calculate quality score
            results["score"] = self.calculate_quality_score(tool_data, repo_metrics)
            
            # Determine if manual review is needed
            review_threshold = self.validation_rules["properties"]["automation_rules"]["properties"]["review_required_score"]["default"]
            if results["score"] < review_threshold:
                results["warnings"].append(f"⚠️ Score ({results['score']}) below review threshold ({review_threshold})")
            
            results["valid"] = len(results["errors"]) == 0
            
        except Exception as e:
            results["errors"].append(f"❌ Validation error: {str(e)}")
        
        return results
    
    def validate_all_tools(self, tools_dir: Path = None) -> Dict[str, Any]:
        """Validate all tool entries in the tools directory."""
        tools_dir = tools_dir or Path(__file__).parent.parent / "tools"
        
        summary = {
            "total": 0,
            "valid": 0,
            "invalid": 0,
            "tools": [],
            "categories": {}
        }
        
        # Find all JSON files in tools directory
        for tool_file in tools_dir.rglob("*.json"):
            summary["total"] += 1
            
            # Determine category from path
            category_path = tool_file.relative_to(tools_dir)
            category = "/".join(category_path.parts[:-1]) if len(category_path.parts) > 1 else "uncategorized"
            
            if category not in summary["categories"]:
                summary["categories"][category] = {"valid": 0, "invalid": 0}
            
            # Validate tool
            results = self.validate_single_tool(tool_file)
            results["category"] = category
            summary["tools"].append(results)
            
            if results["valid"]:
                summary["valid"] += 1
                summary["categories"][category]["valid"] += 1
            else:
                summary["invalid"] += 1
                summary["categories"][category]["invalid"] += 1
        
        return summary


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def print_results(results: Dict[str, Any], verbose: bool = False):
    """Print validation results in a formatted way."""
    if "tools" in results:
        # Multiple tools summary
        print(f"\n📊 Validation Summary")
        print(f"Total tools: {results['total']}")
        print(f"Valid: {results['valid']} ✅")
        print(f"Invalid: {results['invalid']} ❌")
        
        if results["categories"]:
            print(f"\n📁 By Category:")
            for category, stats in results["categories"].items():
                print(f"  {category}: {stats['valid']}✅ {stats['invalid']}❌")
        
        if verbose or results["invalid"] > 0:
            print(f"\n📋 Detailed Results:")
            for tool in results["tools"]:
                status = "✅" if tool["valid"] else "❌"
                score = f" (Score: {tool['score']})" if tool.get("score") else ""
                print(f"{status} {tool['file']}{score}")
                
                if tool["errors"]:
                    for error in tool["errors"]:
                        print(f"    {error}")
                
                if verbose and tool["warnings"]:
                    for warning in tool["warnings"]:
                        print(f"    {warning}")
    else:
        # Single tool results
        status = "✅ VALID" if results["valid"] else "❌ INVALID"
        score = f" (Score: {results['score']})" if results.get("score") else ""
        print(f"\n{status}: {results['file']}{score}")
        
        if results["errors"]:
            print(f"\n❌ Errors:")
            for error in results["errors"]:
                print(f"  {error}")
        
        if results["warnings"]:
            print(f"\n⚠️ Warnings:")
            for warning in results["warnings"]:
                print(f"  {warning}")
        
        if results["metrics"]:
            print(f"\n📈 Metrics:")
            for key, value in results["metrics"].items():
                if value is not None and value != "":
                    print(f"  {key}: {value}")


def main():
    parser = argparse.ArgumentParser(description="Validate Sunshine-AIO tool entries")
    parser.add_argument("--single", "-s", type=str, help="Validate a single tool file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--tools-dir", "-d", type=str, help="Tools directory path")
    parser.add_argument("--schema-dir", type=str, help="Schema directory path")
    
    args = parser.parse_args()
    
    # Initialize validator
    schema_dir = Path(args.schema_dir) if args.schema_dir else None
    validator = ToolValidator(schema_dir)
    
    try:
        if args.single:
            # Validate single tool
            tool_path = Path(args.single)
            results = validator.validate_single_tool(tool_path)
            print_results(results, args.verbose)
            
            # Exit with error code if invalid
            sys.exit(0 if results["valid"] else 1)
        else:
            # Validate all tools
            tools_dir = Path(args.tools_dir) if args.tools_dir else None
            results = validator.validate_all_tools(tools_dir)
            print_results(results, args.verbose)
            
            # Exit with error code if any invalid
            sys.exit(0 if results["invalid"] == 0 else 1)
            
    except KeyboardInterrupt:
        print("\n⏹️ Validation interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()