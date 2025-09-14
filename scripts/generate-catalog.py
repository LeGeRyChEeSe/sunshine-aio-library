#!/usr/bin/env python3
"""
Catalog Generation Script
Generates API catalogs and search indexes from tool entries.
"""

import json
import sys
import os
import argparse
from pathlib import Path
from typing import Dict, List, Any, Set, Optional
from datetime import datetime
import hashlib


class CatalogGenerator:
    def __init__(self, tools_dir: Optional[Path] = None, api_dir: Optional[Path] = None):
        self.tools_dir = tools_dir or Path(__file__).parent.parent / "tools"
        self.api_dir = api_dir or Path(__file__).parent.parent / "api"
        self.api_dir.mkdir(exist_ok=True)
        
    def load_all_tools(self) -> List[Dict[str, Any]]:
        """Load all tool entries from the tools directory."""
        tools = []
        
        for tool_file in self.tools_dir.rglob("*.json"):
            try:
                with open(tool_file, 'r') as f:
                    tool_data = json.load(f)
                
                # Add metadata
                relative_path = tool_file.relative_to(self.tools_dir)
                tool_data["_metadata"] = {
                    "file_path": str(relative_path),
                    "category_path": "/".join(relative_path.parts[:-1]) if len(relative_path.parts) > 1 else "uncategorized",
                    "file_name": tool_file.name,
                    "last_modified": datetime.fromtimestamp(tool_file.stat().st_mtime).isoformat()
                }
                
                tools.append(tool_data)
                
            except Exception as e:
                print(f"⚠️ Error loading {tool_file}: {e}")
                continue
        
        return tools
    
    def generate_main_catalog(self, tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate the main catalog with all tools."""
        catalog = {
            "version": "1.0.0",
            "generated": datetime.now().isoformat(),
            "total_tools": len(tools),
            "tools": []
        }
        
        for tool in tools:
            # Create catalog entry with essential information
            catalog_entry = {
                "id": tool.get("name", "unknown"),
                "name": tool.get("name", "Unknown"),
                "description": tool.get("description", ""),
                "category": tool.get("category", "uncategorized"),
                "subcategory": tool.get("subcategory"),
                "tags": tool.get("tags", []),
                "repository": tool.get("repository", ""),
                "documentation": tool.get("documentation"),
                "license": tool.get("license", ""),
                "platforms": tool.get("platforms", []),
                "language": tool.get("language"),
                "verification": {
                    "status": tool.get("verification", {}).get("status", "pending"),
                    "score": tool.get("verification", {}).get("score", 0),
                    "date": tool.get("verification", {}).get("date")
                },
                "metrics": {
                    "stars": tool.get("metrics", {}).get("stars", 0),
                    "forks": tool.get("metrics", {}).get("forks", 0),
                    "last_commit": tool.get("metrics", {}).get("last_commit")
                },
                "maintainer": {
                    "name": tool.get("maintainer", {}).get("name"),
                    "github": tool.get("maintainer", {}).get("github")
                },
                "added_date": tool.get("added_date"),
                "contributed_by": tool.get("contributed_by"),
                "_metadata": tool.get("_metadata", {})
            }
            
            # Remove None values to keep JSON clean
            catalog_entry = self._clean_dict(catalog_entry)
            catalog["tools"].append(catalog_entry)
        
        # Sort tools by verification score (descending) then by stars
        catalog["tools"].sort(key=lambda x: (
            x.get("verification", {}).get("score", 0),
            x.get("metrics", {}).get("stars", 0)
        ), reverse=True)
        
        return catalog
    
    def generate_categories_index(self, tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate categories index with statistics."""
        categories = {}
        
        for tool in tools:
            category = tool.get("category", "uncategorized")
            subcategory = tool.get("subcategory")
            
            # Initialize category if not exists
            if category not in categories:
                parts = category.split("/")
                main_cat = parts[0] if parts else "uncategorized"
                sub_cat = parts[1] if len(parts) > 1 else None
                
                categories[category] = {
                    "name": main_cat.replace("-", " ").title(),
                    "subcategory": sub_cat.replace("-", " ").title() if sub_cat else None,
                    "full_path": category,
                    "tools": [],
                    "stats": {
                        "total": 0,
                        "verified": 0,
                        "average_score": 0,
                        "total_stars": 0,
                        "languages": set(),
                        "licenses": set()
                    }
                }
            
            # Add tool to category
            categories[category]["tools"].append({
                "id": tool.get("name", "unknown"),
                "name": tool.get("name", "Unknown"),
                "description": tool.get("description", ""),
                "verification_status": tool.get("verification", {}).get("status", "pending"),
                "score": tool.get("verification", {}).get("score", 0),
                "stars": tool.get("metrics", {}).get("stars", 0)
            })
            
            # Update statistics
            stats = categories[category]["stats"]
            stats["total"] += 1
            
            if tool.get("verification", {}).get("status") == "verified":
                stats["verified"] += 1
            
            stats["total_stars"] += tool.get("metrics", {}).get("stars", 0)
            
            if tool.get("language"):
                stats["languages"].add(tool["language"])
            
            if tool.get("license"):
                stats["licenses"].add(tool["license"])
        
        # Calculate averages and convert sets to lists
        for category_data in categories.values():
            stats = category_data["stats"]
            if stats["total"] > 0:
                total_score = sum(tool["score"] for tool in category_data["tools"])
                stats["average_score"] = round(total_score / stats["total"], 1)
            
            stats["languages"] = sorted(list(stats["languages"]))
            stats["licenses"] = sorted(list(stats["licenses"]))
            
            # Sort tools in category by score
            category_data["tools"].sort(key=lambda x: x["score"], reverse=True)
        
        # Create final structure
        index = {
            "version": "1.0.0",
            "generated": datetime.now().isoformat(),
            "total_categories": len(categories),
            "categories": categories
        }
        
        return index
    
    def generate_search_index(self, tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate search index for fast lookups."""
        index = {
            "version": "1.0.0",
            "generated": datetime.now().isoformat(),
            "indexes": {
                "by_name": {},
                "by_tag": {},
                "by_category": {},
                "by_language": {},
                "by_license": {},
                "by_platform": {}
            },
            "filters": {
                "categories": set(),
                "languages": set(),
                "licenses": set(),
                "platforms": set(),
                "tags": set(),
                "verification_statuses": set()
            }
        }
        
        for tool in tools:
            tool_id = tool.get("name", "unknown")
            
            # Index by name (searchable)
            name = tool.get("name", "").lower()
            description = tool.get("description", "").lower()
            search_text = f"{name} {description}".strip()
            
            for word in search_text.split():
                if len(word) >= 2:  # Index words with 2+ characters
                    if word not in index["indexes"]["by_name"]:
                        index["indexes"]["by_name"][word] = []
                    index["indexes"]["by_name"][word].append(tool_id)
            
            # Index by tags
            for tag in tool.get("tags", []):
                if tag not in index["indexes"]["by_tag"]:
                    index["indexes"]["by_tag"][tag] = []
                index["indexes"]["by_tag"][tag].append(tool_id)
                index["filters"]["tags"].add(tag)
            
            # Index by category
            category = tool.get("category", "uncategorized")
            if category not in index["indexes"]["by_category"]:
                index["indexes"]["by_category"][category] = []
            index["indexes"]["by_category"][category].append(tool_id)
            index["filters"]["categories"].add(category)
            
            # Index by language
            language = tool.get("language")
            if language:
                if language not in index["indexes"]["by_language"]:
                    index["indexes"]["by_language"][language] = []
                index["indexes"]["by_language"][language].append(tool_id)
                index["filters"]["languages"].add(language)
            
            # Index by license
            license_name = tool.get("license")
            if license_name:
                if license_name not in index["indexes"]["by_license"]:
                    index["indexes"]["by_license"][license_name] = []
                index["indexes"]["by_license"][license_name].append(tool_id)
                index["filters"]["licenses"].add(license_name)
            
            # Index by platform
            for platform in tool.get("platforms", []):
                if platform not in index["indexes"]["by_platform"]:
                    index["indexes"]["by_platform"][platform] = []
                index["indexes"]["by_platform"][platform].append(tool_id)
                index["filters"]["platforms"].add(platform)
            
            # Add verification status to filters
            verification_status = tool.get("verification", {}).get("status", "pending")
            index["filters"]["verification_statuses"].add(verification_status)
        
        # Convert sets to sorted lists
        for filter_name in index["filters"]:
            index["filters"][filter_name] = sorted(list(index["filters"][filter_name]))
        
        return index
    
    def generate_stats(self, tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive statistics."""
        stats = {
            "version": "1.0.0",
            "generated": datetime.now().isoformat(),
            "overview": {
                "total_tools": len(tools),
                "verified_tools": 0,
                "pending_tools": 0,
                "failed_tools": 0,
                "total_stars": 0,
                "total_forks": 0,
                "average_score": 0
            },
            "categories": {},
            "languages": {},
            "licenses": {},
            "platforms": {},
            "verification_statuses": {},
            "quality_distribution": {
                "excellent": 0,  # 90-100
                "good": 0,       # 70-89
                "fair": 0,       # 50-69
                "poor": 0        # 0-49
            },
            "activity_analysis": {
                "active": 0,     # Activity in last 30 days
                "moderate": 0,   # Activity in last 6 months
                "inactive": 0    # No activity in 6+ months
            },
            "top_tools": {
                "by_stars": [],
                "by_score": [],
                "by_recent_activity": []
            }
        }
        
        # Collect data
        scores = []
        starred_tools = []
        scored_tools = []
        recent_tools = []
        
        for tool in tools:
            # Basic stats
            verification = tool.get("verification", {})
            metrics = tool.get("metrics", {})
            
            status = verification.get("status", "pending")
            score = verification.get("score", 0)
            stars = metrics.get("stars", 0)
            forks = metrics.get("forks", 0)
            
            stats["overview"]["total_stars"] += stars
            stats["overview"]["total_forks"] += forks
            scores.append(score)
            
            # Verification status counts
            if status == "verified":
                stats["overview"]["verified_tools"] += 1
            elif status == "pending":
                stats["overview"]["pending_tools"] += 1
            elif status == "failed":
                stats["overview"]["failed_tools"] += 1
            
            stats["verification_statuses"][status] = stats["verification_statuses"].get(status, 0) + 1
            
            # Quality distribution
            if score >= 90:
                stats["quality_distribution"]["excellent"] += 1
            elif score >= 70:
                stats["quality_distribution"]["good"] += 1
            elif score >= 50:
                stats["quality_distribution"]["fair"] += 1
            else:
                stats["quality_distribution"]["poor"] += 1
            
            # Category stats
            category = tool.get("category", "uncategorized")
            if category not in stats["categories"]:
                stats["categories"][category] = {"count": 0, "average_score": 0, "total_stars": 0}
            stats["categories"][category]["count"] += 1
            stats["categories"][category]["total_stars"] += stars
            
            # Language stats
            language = tool.get("language")
            if language:
                if language not in stats["languages"]:
                    stats["languages"][language] = {"count": 0, "average_score": 0}
                stats["languages"][language]["count"] += 1
            
            # License stats
            license_name = tool.get("license")
            if license_name:
                stats["licenses"][license_name] = stats["licenses"].get(license_name, 0) + 1
            
            # Platform stats
            for platform in tool.get("platforms", []):
                stats["platforms"][platform] = stats["platforms"].get(platform, 0) + 1
            
            # Activity analysis
            last_commit = metrics.get("last_commit")
            if last_commit:
                try:
                    commit_date = datetime.fromisoformat(last_commit)
                    days_ago = (datetime.now() - commit_date).days
                    
                    if days_ago <= 30:
                        stats["activity_analysis"]["active"] += 1
                    elif days_ago <= 180:
                        stats["activity_analysis"]["moderate"] += 1
                    else:
                        stats["activity_analysis"]["inactive"] += 1
                except:
                    stats["activity_analysis"]["inactive"] += 1
            else:
                stats["activity_analysis"]["inactive"] += 1
            
            # Collect tools for top lists
            tool_summary = {
                "id": tool.get("name", "unknown"),
                "name": tool.get("name", "Unknown"),
                "category": category,
                "stars": stars,
                "score": score,
                "last_commit": last_commit
            }
            
            starred_tools.append(tool_summary)
            scored_tools.append(tool_summary)
            if last_commit:
                recent_tools.append(tool_summary)
        
        # Calculate averages
        if tools:
            stats["overview"]["average_score"] = round(sum(scores) / len(scores), 1)
            
            for category_data in stats["categories"].values():
                if category_data["count"] > 0:
                    # We'll need to recalculate this properly
                    pass
        
        # Generate top lists
        stats["top_tools"]["by_stars"] = sorted(starred_tools, key=lambda x: x["stars"], reverse=True)[:10]
        stats["top_tools"]["by_score"] = sorted(scored_tools, key=lambda x: x["score"], reverse=True)[:10]
        
        # Sort recent tools by commit date
        recent_tools_sorted = []
        for tool in recent_tools:
            if tool["last_commit"]:
                try:
                    tool["last_commit_date"] = datetime.fromisoformat(tool["last_commit"])
                    recent_tools_sorted.append(tool)
                except:
                    pass
        
        stats["top_tools"]["by_recent_activity"] = sorted(
            recent_tools_sorted, 
            key=lambda x: x["last_commit_date"], 
            reverse=True
        )[:10]
        
        # Clean up temporary fields
        for tool in stats["top_tools"]["by_recent_activity"]:
            if "last_commit_date" in tool:
                del tool["last_commit_date"]
        
        return stats
    
    def _clean_dict(self, d: Any) -> Any:
        """Recursively remove None values from dictionary."""
        if isinstance(d, dict):
            return {k: self._clean_dict(v) for k, v in d.items() if v is not None}
        elif isinstance(d, list):
            return [self._clean_dict(item) for item in d if item is not None]
        else:
            return d
    
    def generate_all_catalogs(self) -> Dict[str, str]:
        """Generate all catalog files."""
        print("📊 Loading tools...")
        tools = self.load_all_tools()
        
        if not tools:
            print("⚠️ No tools found!")
            return {}
        
        print(f"📈 Generating catalogs for {len(tools)} tools...")
        
        # Generate all catalogs
        catalogs = {
            "catalog.json": self.generate_main_catalog(tools),
            "categories.json": self.generate_categories_index(tools),
            "search.json": self.generate_search_index(tools),
            "stats.json": self.generate_stats(tools)
        }
        
        # Write catalog files
        files_written = {}
        for filename, data in catalogs.items():
            output_path = self.api_dir / filename
            try:
                with open(output_path, 'w') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False, default=str)
                
                # Calculate file size
                size_kb = output_path.stat().st_size / 1024
                files_written[filename] = f"{output_path} ({size_kb:.1f} KB)"
                print(f"✅ Generated {filename} ({size_kb:.1f} KB)")
                
            except Exception as e:
                print(f"❌ Failed to write {filename}: {e}")
        
        return files_written
    
    def generate_manifest(self) -> Dict[str, Any]:
        """Generate a manifest file with catalog metadata."""
        manifest = {
            "version": "1.0.0",
            "generated": datetime.now().isoformat(),
            "catalogs": {},
            "api_endpoints": {
                "main_catalog": "/api/catalog.json",
                "categories": "/api/categories.json",
                "search_index": "/api/search.json",
                "statistics": "/api/stats.json"
            },
            "usage": {
                "search_tools": "GET /api/search.json -> filter by indexes.by_name[query]",
                "list_categories": "GET /api/categories.json -> categories",
                "get_stats": "GET /api/stats.json",
                "browse_all": "GET /api/catalog.json -> tools[]"
            }
        }
        
        # Add file metadata for each catalog
        for api_file in self.api_dir.glob("*.json"):
            if api_file.name != "manifest.json":
                try:
                    stat = api_file.stat()
                    manifest["catalogs"][api_file.name] = {
                        "path": str(api_file.relative_to(self.api_dir.parent)),
                        "size_bytes": stat.st_size,
                        "size_kb": round(stat.st_size / 1024, 1),
                        "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                    }
                except Exception as e:
                    print(f"⚠️ Error getting metadata for {api_file}: {e}")
        
        # Write manifest
        manifest_path = self.api_dir / "manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        return manifest


def main():
    parser = argparse.ArgumentParser(description="Generate Sunshine-AIO tool catalogs")
    parser.add_argument("--tools-dir", "-d", type=str, help="Tools directory path")
    parser.add_argument("--api-dir", "-o", type=str, help="API output directory path") 
    parser.add_argument("--manifest", "-m", action="store_true", help="Generate manifest file")
    
    args = parser.parse_args()
    
    # Initialize generator
    tools_dir = Path(args.tools_dir) if args.tools_dir else None
    api_dir = Path(args.api_dir) if args.api_dir else None
    generator = CatalogGenerator(tools_dir, api_dir)
    
    try:
        # Generate all catalogs
        files_written = generator.generate_all_catalogs()
        
        if not files_written:
            print("❌ No catalog files generated")
            sys.exit(1)
        
        # Generate manifest if requested
        if args.manifest:
            manifest = generator.generate_manifest()
            print(f"✅ Generated manifest.json")
        
        print(f"\n🎉 Generated {len(files_written)} catalog files:")
        for filename, path_info in files_written.items():
            print(f"  📄 {path_info}")
        
        print(f"\n📁 API directory: {generator.api_dir}")
        
    except KeyboardInterrupt:
        print("\n⏹️ Catalog generation interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()