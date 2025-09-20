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
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
import re
from urllib.parse import urlparse


class ToolValidator:
    def __init__(self, schema_dir: Optional[Path] = None):
        self.schema_dir = schema_dir if schema_dir is not None else Path(__file__).parent.parent / "schemas"
        self.tool_schema = self._load_schema("tool-entry.json")
        self.validation_rules = self._load_schema("validation-rules.json")
        self.autocomplete_enabled = True
        
    def _load_schema(self, filename: str) -> Dict[str, Any]:
        """Load JSON schema from file."""
        schema_path = self.schema_dir / filename
        try:
            with open(schema_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[ERROR] Schema file not found: {schema_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"[ERROR] Invalid JSON in schema {filename}: {e}")
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
                return True, f"[OK] URL accessible (HTTP {response.status_code})"
            else:
                return False, f"[ERROR] URL returned HTTP {response.status_code}"
                
        except requests.exceptions.Timeout:
            return False, "[ERROR] URL timeout"
        except requests.exceptions.ConnectionError:
            return False, "[ERROR] Connection error"
        except Exception as e:
            return False, f"[ERROR] Error checking URL: {str(e)}"
    
    def validate_github_repository(self, repo_url: str) -> Tuple[bool, str, Dict[str, Any]]:
        """Validate GitHub repository and collect metrics."""
        if not repo_url.startswith("https://github.com/"):
            return False, "[ERROR] Not a GitHub URL", {}

        # Extract owner/repo from URL
        match = re.match(r'https://github\.com/([^/]+)/([^/]+)/?$', repo_url)
        if not match:
            return False, "[ERROR] Invalid GitHub URL format", {}

        owner, repo = match.groups()
        api_url = f"https://api.github.com/repos/{owner}/{repo}"

        try:
            response = requests.get(api_url, timeout=10)
            if response.status_code == 404:
                return False, "[ERROR] Repository not found", {}
            elif response.status_code != 200:
                return False, f"[ERROR] GitHub API error (HTTP {response.status_code})", {}

            repo_data = response.json()
            metrics = {
                "stars": repo_data.get("stargazers_count", 0),
                "forks": repo_data.get("forks_count", 0),
                "last_commit": repo_data.get("pushed_at", "").split("T")[0] if repo_data.get("pushed_at") else None,
                "language": repo_data.get("language", ""),
                "license": repo_data.get("license", {}).get("spdx_id", "") if repo_data.get("license") else "",
                "archived": repo_data.get("archived", False),
                "disabled": repo_data.get("disabled", False),
                "description": repo_data.get("description", ""),
                "homepage": repo_data.get("homepage", ""),
                "topics": repo_data.get("topics", []),
                "default_branch": repo_data.get("default_branch", "main"),
                "has_releases": repo_data.get("has_releases", False),
                "releases_url": repo_data.get("releases_url", "").replace("{/id}", "")
            }

            warnings = []
            if repo_data.get("archived"):
                warnings.append("[WARNING] Repository is archived")
            if repo_data.get("disabled"):
                warnings.append("[WARNING] Repository is disabled")
            if metrics["stars"] < self.validation_rules["properties"]["quality_thresholds"]["properties"]["minimum_stars"]["default"]:
                warnings.append(f"[WARNING] Low star count ({metrics['stars']})")

            status = "[OK] Repository accessible" + (f" ({', '.join(warnings)})" if warnings else "")
            return True, status, metrics

        except Exception as e:
            return False, f"[ERROR] Error accessing repository: {str(e)}", {}
    
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
                    warnings.append(f"[WARNING] Contains potentially unsafe word: '{word}'")
        
        return warnings

    def validate_installation_metadata(self, tool_data: Dict[str, Any], repo_metrics: Dict[str, Any]) -> List[str]:
        """Validate installation metadata and check GitHub releases compatibility."""
        errors = []
        installation = tool_data.get("installation", {})

        if not installation:
            errors.append("[ERROR] Missing installation metadata")
            return errors

        # Handle both old and new format
        if "platforms" in installation:
            # New multi-platform format
            platforms = installation["platforms"]
            if not platforms:
                errors.append("[ERROR] Empty platforms configuration")
                return errors

            # Check if repository has releases for download_strategy validation
            repo_url = tool_data.get("repository", "")
            releases_info = None
            if repo_url and "github.com" in repo_url:
                try:
                    match = re.match(r'https://github\.com/([^/]+)/([^/]+)/?$', repo_url)
                    if match:
                        owner, repo = match.groups()
                        releases_info = self._get_github_releases_info(owner, repo)
                except Exception:
                    pass

            # Validate each platform configuration
            for platform, config in platforms.items():
                platform_prefix = f"[{platform.upper()}]"

                # Required fields
                if not config.get("type"):
                    errors.append(f"{platform_prefix} Missing installation type")

                # Validate download strategy
                download_strategy = config.get("download_strategy", "github_releases")
                if download_strategy == "github_releases":
                    if not releases_info or not releases_info.get("has_releases"):
                        errors.append(f"{platform_prefix} GitHub releases strategy specified but no releases found")
                    else:
                        # Check if file pattern would match available assets
                        file_pattern = config.get("file_pattern")
                        if file_pattern and releases_info.get("platform_assets"):
                            platform_assets = releases_info["platform_assets"].get(platform.lower(), {})
                            if not platform_assets:
                                errors.append(f"{platform_prefix} No assets found for platform despite file pattern: {file_pattern}")

                # Validate installation flags for silent installation
                if config.get("silent", True):
                    install_flags = config.get("install_flags", [])
                    if not install_flags and config.get("type") in ["executable", "msi"]:
                        errors.append(f"{platform_prefix} Silent installation enabled but no install_flags specified")

                # Validate checksum configuration
                if config.get("checksum_verification", True):
                    checksum = config.get("checksum", "")
                    if not checksum:
                        errors.append(f"{platform_prefix} Checksum verification enabled but no checksum provided")

        else:
            # Old single-platform format - warn about deprecation
            errors.append("[WARNING] Using deprecated single-platform installation format. Consider upgrading to multi-platform format.")

            # Basic validation for old format
            if not installation.get("type"):
                errors.append("[ERROR] Missing installation type")

        return errors

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

    def _is_legacy_format(self, tool_data: Dict[str, Any]) -> bool:
        """Check if tool entry uses legacy format (missing modern fields)."""
        modern_fields = ["installation", "uninstallation", "compatibility", "slug"]
        return not any(field in tool_data for field in modern_fields)

    def _get_github_releases_info(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get latest release information from GitHub API."""
        try:
            api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
            response = requests.get(api_url, timeout=10)

            if response.status_code == 200:
                release_data = response.json()
                assets = release_data.get("assets", [])

                # Find primary asset (executable or installer)
                primary_asset = None
                for asset in assets:
                    name = asset.get("name", "").lower()
                    if any(ext in name for ext in [".exe", ".msi", ".zip", ".tar.gz", ".deb", ".rpm"]):
                        primary_asset = asset
                        break

                if not primary_asset and assets:
                    primary_asset = assets[0]  # Take first asset if no executable found

                # Detect multi-platform assets
                platform_assets = self._detect_platform_assets(assets)

                return {
                    "has_releases": True,
                    "latest_version": release_data.get("tag_name", ""),
                    "download_url": primary_asset.get("browser_download_url", "") if primary_asset else "",
                    "asset_name": primary_asset.get("name", "") if primary_asset else "",
                    "asset_size": primary_asset.get("size", 0) if primary_asset else 0,
                    "published_at": release_data.get("published_at", ""),
                    "prerelease": release_data.get("prerelease", False),
                    "is_multiplatform": len(platform_assets) > 1,
                    "platform_assets": platform_assets
                }
            else:
                return {"has_releases": False}

        except Exception:
            return {"has_releases": False}

    def _detect_platform_assets(self, assets: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Detect platform-specific assets from GitHub releases."""
        platform_assets = {}

        # Platform detection patterns with priorities (higher priority = better match)
        platform_patterns = {
            "windows": [
                (r'.*windows.*\.exe$', 100),  # Best: Windows installer exe
                (r'.*win(32|64)?.*\.exe$', 95),
                (r'.*windows.*\.msi$', 90),   # MSI installer
                (r'.*win(32|64)?.*\.msi$', 85),
                (r'^[^-]*\.exe$', 80),        # Simple exe (like "Tool.exe")
                (r'.*\.exe$', 70),            # Any exe
                (r'.*\.msi$', 60),            # Any MSI
                (r'.*windows.*\.zip$', 40),   # ZIP as fallback
                (r'.*win(32|64)?.*\.zip$', 35),
                (r'.*\.zip$', 20)             # Generic ZIP (low priority)
            ],
            "linux": [
                (r'.*linux.*\.deb$', 100),   # Best: Linux deb
                (r'.*ubuntu.*\.deb$', 95),
                (r'.*\.deb$', 90),            # Any deb
                (r'.*linux.*\.AppImage$', 85), # AppImage
                (r'.*\.AppImage$', 80),
                (r'.*linux.*\.rpm$', 75),    # RPM
                (r'.*\.rpm$', 70),
                (r'.*linux.*\.tar\.gz$', 50), # Tarball as fallback
                (r'.*\.tar\.gz$', 30)
            ],
            "macos": [
                (r'.*mac(os)?.*\.dmg$', 100), # Best: macOS DMG
                (r'.*darwin.*\.dmg$', 95),
                (r'.*\.dmg$', 90),            # Any DMG
                (r'.*mac(os)?.*\.pkg$', 80),  # PKG installer
                (r'.*darwin.*\.pkg$', 75),
                (r'.*\.pkg$', 70),
                (r'.*mac(os)?.*\.zip$', 50),  # ZIP as fallback
                (r'.*darwin.*\.zip$', 45)
            ]
        }

        # Exclude patterns for debug/development files
        exclude_patterns = [
            r'.*debug.*',
            r'.*pdb.*',
            r'.*symbols.*',
            r'.*dev.*',
            r'.*source.*',
            r'.*src.*'
        ]

        for asset in assets:
            asset_name = asset.get("name", "")
            asset_name_lower = asset_name.lower()

            # Skip debug/development files
            if any(re.search(exclude, asset_name_lower) for exclude in exclude_patterns):
                continue

            for platform, pattern_priorities in platform_patterns.items():
                best_match = None
                best_priority = -1

                for pattern, priority in pattern_priorities:
                    if re.match(pattern, asset_name_lower, re.IGNORECASE):
                        if priority > best_priority:
                            best_priority = priority
                            best_match = {
                                "asset": asset,
                                "name": asset_name,
                                "url": self._convert_to_latest_url(asset.get("browser_download_url", "")),
                                "type": self._detect_installation_type(asset_name, ""),
                                "executable": self._generate_generic_executable_name(asset_name, platform),
                                "priority": priority
                            }

                # Only update if we found a better match or no match exists
                if best_match and (platform not in platform_assets or
                                   best_priority > platform_assets[platform].get("priority", -1)):
                    platform_assets[platform] = best_match

        # Clean up priority field (not needed in final output)
        for platform_data in platform_assets.values():
            platform_data.pop("priority", None)

        return platform_assets

    def _convert_to_latest_url(self, original_url: str) -> str:
        """Convert a versioned GitHub release URL to generic latest format."""
        if not original_url or "github.com" not in original_url:
            return original_url

        # Pattern: https://github.com/owner/repo/releases/download/v1.2.3/filename
        # Convert to: https://github.com/owner/repo/releases/latest (generic, no specific file)
        pattern = r'https://github\.com/([^/]+)/([^/]+)/releases/download/([^/]+)/(.+)$'
        match = re.match(pattern, original_url)

        if match:
            owner, repo, version, filename = match.groups()
            latest_url = f"https://github.com/{owner}/{repo}/releases/latest"
            return latest_url

        return original_url

    def _generate_generic_executable_name(self, original_name: str, platform: str) -> str:
        """Generate a generic executable pattern that can match versioned files."""
        if not original_name:
            return original_name

        # Get file extension
        ext_match = re.search(r'\.([^.]+)$', original_name)
        if not ext_match:
            return original_name

        extension = ext_match.group(1)
        base_name = original_name.lower()

        # Step 1: Extract the core tool name using aggressive patterns
        # Remove extension first for easier processing
        name_without_ext = re.sub(r'\.[^.]+$', '', base_name)

        # Pattern 1: Tool name followed immediately by version numbers
        # "7z2501-arm" -> "7z", "discord0309" -> "discord"
        core_match = re.match(r'^([a-z]+)\d.*', name_without_ext)
        if core_match:
            core_name = core_match.group(1)
            return f"{core_name}.{extension}"

        # Pattern 2: Tool name with hyphens/underscores followed by version
        # "OBS-Studio-31.1.2-Windows" -> "OBS-Studio", "my-tool-v1.0" -> "my-tool"
        core_match = re.match(r'^([a-z-]+?)(?:[-_]v?\d+|[-_]\d{4}|[-_]windows|[-_]linux|[-_]mac).*', name_without_ext)
        if core_match:
            core_name = core_match.group(1).rstrip('-_')
            return f"{core_name}.{extension}"

        # Pattern 3: Simple tool name before first number/version indicator
        # "blender4.0" -> "blender", "firefox125" -> "firefox"
        core_match = re.match(r'^([a-z]+)', name_without_ext)
        if core_match:
            core_name = core_match.group(1)
            return f"{core_name}.{extension}"

        # Fallback: return original name if no pattern matches
        return original_name

    def _detect_installation_type(self, asset_name: str, repo_language: str) -> str:
        """Detect installation type based on asset name and repository language."""
        asset_lower = asset_name.lower()

        if ".msi" in asset_lower:
            return "msi"
        elif ".exe" in asset_lower:
            return "executable"
        elif any(ext in asset_lower for ext in [".zip", ".tar.gz", ".7z"]):
            return "zip"
        elif any(ext in asset_lower for ext in [".deb", ".rpm"]):
            return "package-manager"
        elif any(ext in asset_lower for ext in [".sh", ".ps1", ".bat"]):
            return "script"
        else:
            # Fallback based on language
            if repo_language in ["Python", "JavaScript", "TypeScript"]:
                return "script"
            else:
                return "portable"

    def _generate_installation_config(self, release_info: Dict[str, Any], repo_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate installation configuration based on release information."""
        if not release_info.get("has_releases"):
            return {
                "type": "executable",
                "args": [],
                "postInstall": "",
                "checksum": ""
            }

        # Always prioritize multi-platform format if we have platform-specific assets
        if release_info.get("platform_assets"):
            platform_assets = release_info["platform_assets"]
            platforms_config = {}

            for platform, asset_info in platform_assets.items():
                platform_config = {
                    "type": asset_info["type"],
                    "url": asset_info["url"],
                    "executable": asset_info["executable"],
                    "args": self._get_platform_default_args(platform, asset_info["type"]),
                    "postInstall": "",
                    "checksum": "",
                    "silent": platform != "macos"  # macOS often requires user interaction
                }
                platforms_config[platform] = platform_config

            return {"platforms": platforms_config}

        # Fallback: Single platform format only when no platform-specific assets found
        else:
            installation_config = {
                "type": "executable",
                "args": [],
                "postInstall": "",
                "checksum": ""
            }

            if release_info.get("asset_name"):
                asset_name = release_info["asset_name"]
                detected_type = self._detect_installation_type(asset_name, repo_metrics.get("language", ""))
                installation_config["type"] = detected_type
                installation_config["executable"] = self._generate_generic_executable_name(asset_name, "")

                # Always use generic latest URL for single platform
                if release_info.get("download_url"):
                    installation_config["url"] = self._convert_to_latest_url(release_info["download_url"])

            return installation_config

    def _get_platform_default_args(self, platform: str, install_type: str) -> List[str]:
        """Get default installation arguments for platform and type."""
        args_map = {
            "windows": {
                "msi": ["/quiet", "/norestart"],
                "executable": ["/S"],
                "zip": [],
                "portable": []
            },
            "linux": {
                "package-manager": ["--force-yes"],
                "executable": ["--silent"],
                "zip": [],
                "portable": []
            },
            "macos": {
                "portable": [],
                "executable": [],
                "zip": []
            }
        }

        return args_map.get(platform, {}).get(install_type, [])

    def _verify_executable_patterns(self, installation_config: Dict[str, Any], repo_url: str) -> List[str]:
        """Verify that executable patterns can match actual release assets."""
        verification_results = []

        if not repo_url or "github.com" not in repo_url:
            return ["[INFO] Cannot verify patterns for non-GitHub repository"]

        # Extract owner/repo from URL
        match = re.match(r'https://github\.com/([^/]+)/([^/]+)/?$', repo_url)
        if not match:
            return ["[WARNING] Invalid GitHub URL format for verification"]

        owner, repo = match.groups()

        try:
            # Get latest release data directly
            api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
            response = requests.get(api_url, timeout=10)

            if response.status_code != 200:
                return [f"[INFO] Cannot access latest release for verification (HTTP {response.status_code})"]

            release_data = response.json()
            assets = release_data.get("assets", [])

            if not assets:
                return ["[INFO] No release assets found for verification"]

            # Check if we have multi-platform installation
            if "platforms" in installation_config:
                platforms_config = installation_config["platforms"]

                for platform, platform_config in platforms_config.items():
                    pattern = platform_config.get("executable", "")
                    if not pattern:
                        verification_results.append(f"[WARNING] No executable pattern for {platform}")
                        continue

                    # Try to find matching asset
                    matches = self._find_matching_assets(pattern, assets, platform)

                    if matches:
                        best_match = matches[0]  # Take the best match
                        verification_results.append(f"[OK] {platform}: pattern '{pattern}' matches '{best_match['name']}'")
                    else:
                        verification_results.append(f"[WARNING] {platform}: pattern '{pattern}' found no matches in release assets")

            else:
                # Single platform installation
                pattern = installation_config.get("executable", "")
                if pattern:
                    matches = self._find_matching_assets(pattern, assets)
                    if matches:
                        best_match = matches[0]
                        verification_results.append(f"[OK] Pattern '{pattern}' matches '{best_match['name']}'")
                    else:
                        verification_results.append(f"[WARNING] Pattern '{pattern}' found no matches in release assets")
                else:
                    verification_results.append("[INFO] No executable pattern to verify")

        except Exception as e:
            verification_results.append(f"[ERROR] Pattern verification failed: {str(e)}")

        return verification_results

    def _find_matching_assets(self, pattern: str, assets: List[Dict[str, Any]], platform: Optional[str] = None) -> List[Dict[str, Any]]:
        """Find assets that match the given executable pattern."""
        if not pattern or not assets:
            return []

        matches = []

        # Extract base name and extension from pattern
        pattern_base = re.sub(r'\.[^.]*$', '', pattern.lower())  # Remove extension
        pattern_ext = re.search(r'\.([^.]*)$', pattern.lower())
        pattern_ext = pattern_ext.group(1) if pattern_ext else ""

        for asset in assets:
            asset_name = asset.get("name", "")
            asset_name_lower = asset_name.lower()

            # Skip debug/dev files
            if any(exclude in asset_name_lower for exclude in ["debug", "pdb", "symbols", "dev", "source", "src"]):
                continue

            # Check if asset matches pattern
            asset_base = re.sub(r'\.[^.]*$', '', asset_name_lower)
            asset_ext_match = re.search(r'\.([^.]*)$', asset_name_lower)
            asset_ext = asset_ext_match.group(1) if asset_ext_match else ""

            # Must have same extension
            if pattern_ext and asset_ext != pattern_ext:
                continue

            # Check if base names are compatible
            # Pattern "OBS-Studio" should match "OBS-Studio-31.1.2-Windows-x64"
            if pattern_base in asset_base or self._names_are_compatible(pattern_base, asset_base):
                # Platform-specific filtering
                if platform:
                    platform_keywords = {
                        "windows": ["windows", "win", "win32", "win64", "x64", "x86", "installer", "setup"],
                        "linux": ["linux", "ubuntu", "debian", "deb", "rpm", "appimage"],
                        "macos": ["mac", "macos", "darwin", "apple", "dmg", "pkg"]
                    }

                    if platform in platform_keywords:
                        keywords = platform_keywords[platform]
                        if any(keyword in asset_name_lower for keyword in keywords):
                            matches.append(asset)
                else:
                    matches.append(asset)

        # Sort by relevance (shorter names often better, specific platform indicators)
        matches.sort(key=lambda x: (
            len(x.get("name", "")),  # Prefer shorter names
            -sum(1 for keyword in ["installer", "setup"] if keyword in x.get("name", "").lower())  # Prefer installers
        ))

        return matches

    def _names_are_compatible(self, pattern_base: str, asset_base: str) -> bool:
        """Check if pattern and asset base names are compatible."""
        # Remove common separators and compare
        pattern_clean = re.sub(r'[-_\s]+', '', pattern_base)
        asset_clean = re.sub(r'[-_\s]+', '', asset_base)

        # Check if one is a substring of the other (case insensitive)
        return (pattern_clean in asset_clean or
                asset_clean in pattern_clean or
                pattern_clean.replace('-', '') in asset_clean.replace('-', ''))

    def _generate_slug(self, name: str) -> str:
        """Generate a URL-friendly slug from tool name."""
        slug = re.sub(r'[^a-zA-Z0-9\s\-_]', '', name)
        slug = re.sub(r'\s+', '-', slug)
        slug = slug.lower().strip('-')
        return slug

    def _map_github_language_to_schema(self, github_language: str) -> str:
        """Map GitHub language to schema-allowed language."""
        language_map = {
            "C": "C++",
            "C++": "C++",
            "C#": "C#",
            "JavaScript": "JavaScript",
            "TypeScript": "TypeScript",
            "Python": "Python",
            "Go": "Go",
            "Rust": "Rust",
            "Java": "Java",
            "PHP": "PHP",
            "Ruby": "Ruby",
            "Shell": "Shell",
            "PowerShell": "Shell",
            "Batchfile": "Shell"
        }
        return language_map.get(github_language, "Other")

    def _detect_platforms_from_releases(self, assets: List[Dict], repo_language: str) -> List[str]:
        """Detect supported platforms from release assets."""
        platforms = set()

        if not assets:
            # Fallback based on language
            if repo_language in ["Python", "JavaScript", "TypeScript", "Java"]:
                return ["Cross-platform"]
            else:
                return ["Windows", "Linux", "macOS"]

        for asset in assets:
            name = asset.get("name", "").lower()
            if any(term in name for term in ["win", "windows", ".exe", ".msi"]):
                platforms.add("Windows")
            if any(term in name for term in ["linux", ".deb", ".rpm", ".tar.gz"]):
                platforms.add("Linux")
            if any(term in name for term in ["mac", "macos", "darwin"]):
                platforms.add("macOS")

        if not platforms:
            platforms.add("Cross-platform")

        return sorted(list(platforms))

    def autocomplete_legacy_manifest(self, tool_data: Dict[str, Any], repo_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Auto-complete legacy manifest with modern fields."""
        if not self._is_legacy_format(tool_data):
            return tool_data  # Already complete

        print(f"[AUTOCOMPLETE] Completing legacy manifest for '{tool_data.get('name', 'Unknown')}'...")

        # Extract repository info
        repo_url = tool_data.get("repository", "")
        match = re.match(r'https://github\.com/([^/]+)/([^/]+)/?$', repo_url)
        if not match:
            return tool_data

        owner, repo = match.groups()

        # Get release information
        release_info = self._get_github_releases_info(owner, repo)

        # Generate missing fields
        completed_data = tool_data.copy()

        # Add slug if missing
        if "slug" not in completed_data:
            completed_data["slug"] = self._generate_slug(tool_data.get("name", ""))

        # Add short-description if missing (use description or repo description)
        if "short-description" not in completed_data and "short_description" not in completed_data:
            description = tool_data.get("description", repo_metrics.get("description", ""))
            if description:
                # Truncate to 100 chars max
                short_desc = description[:97] + "..." if len(description) > 100 else description
                completed_data["short-description"] = short_desc

        # Add platforms if missing
        if "platforms" not in completed_data:
            assets = []
            if release_info.get("has_releases"):
                # Would need to fetch assets separately, simplified for now
                assets = []
            completed_data["platforms"] = self._detect_platforms_from_releases(assets, repo_metrics.get("language", ""))

        # Add language if missing
        if "language" not in completed_data and repo_metrics.get("language"):
            completed_data["language"] = self._map_github_language_to_schema(repo_metrics["language"])

        # Add license if missing
        if "license" not in completed_data and repo_metrics.get("license"):
            completed_data["license"] = repo_metrics["license"]

        # Add compatibility section
        if "compatibility" not in completed_data:
            platforms = completed_data.get("platforms", ["Cross-platform"])
            platform_mapping = {
                "Windows": "windows",
                "Linux": "linux",
                "macOS": "macos",
                "Cross-platform": "windows"  # Default to windows for cross-platform
            }

            compat_platforms = []
            for platform in platforms:
                if platform in platform_mapping:
                    mapped = platform_mapping[platform]
                    if mapped not in compat_platforms:
                        compat_platforms.append(mapped)
                elif platform == "Cross-platform":
                    compat_platforms = ["windows", "linux", "macos"]
                    break

            completed_data["compatibility"] = {
                "sunshine": True,  # Default assumption
                "apollo": False,   # Conservative default
                "platforms": compat_platforms or ["windows"]
            }

        # Add installation section
        if "installation" not in completed_data:
            completed_data["installation"] = self._generate_installation_config(release_info, repo_metrics)

        # Add uninstallation section
        if "uninstallation" not in completed_data:
            completed_data["uninstallation"] = {
                "type": "manual",  # Safe default
                "path": "",
                "args": []
            }

        # Add configuration section
        if "configuration" not in completed_data:
            config = {"type": ""}
            # Check if homepage could be a config URL
            if repo_metrics.get("homepage") and repo_metrics["homepage"].startswith("http"):
                config["type"] = "url"
                config["url"] = repo_metrics["homepage"]
            completed_data["configuration"] = config

        # Add empty optional fields
        for field in ["screenshots", "icon"]:
            if field not in completed_data:
                completed_data[field] = [] if field == "screenshots" else ""

        # Add author if missing
        if "author" not in completed_data:
            completed_data["author"] = owner  # Use GitHub owner as author

        # Add website if missing and available
        if "website" not in completed_data and repo_metrics.get("homepage"):
            completed_data["website"] = repo_metrics["homepage"]

        # Add tags from GitHub topics if missing
        if "tags" not in completed_data and repo_metrics.get("topics"):
            # Convert topics to valid tags and limit to 8
            valid_tags = []
            for topic in repo_metrics["topics"][:8]:
                # Ensure tag matches pattern ^[a-z0-9-]+$
                tag = re.sub(r'[^a-z0-9-]', '-', topic.lower())
                if tag and len(tag) <= 20:
                    valid_tags.append(tag)
            if valid_tags:
                completed_data["tags"] = valid_tags

        print(f"[AUTOCOMPLETE] Completed {len([k for k in completed_data.keys() if k not in tool_data])} missing fields")
        return completed_data

    def validate_single_tool(self, tool_path: Path, dry_run: bool = False) -> Dict[str, Any]:
        """Validate a single tool entry and return results."""
        results = {
            "file": str(tool_path),
            "valid": False,
            "errors": [],
            "warnings": [],
            "metrics": {},
            "score": 0,
            "autocompleted": False,
            "would_autocomplete": False
        }

        try:
            # Load tool data
            original_tool_data = self._load_tool_entry(tool_path)

            # URL validation first to get repo metrics
            repo_url = original_tool_data["repository"]
            repo_valid, repo_status, repo_metrics = self.validate_github_repository(repo_url)
            results["metrics"] = repo_metrics

            if not repo_valid:
                results["errors"].append(repo_status)
                return results

            # Auto-complete legacy manifest if enabled or show what would be done
            tool_data = original_tool_data
            is_legacy = self._is_legacy_format(original_tool_data)

            if dry_run and is_legacy:
                # Dry run: show what would be completed but don't save
                completed_data = self.autocomplete_legacy_manifest(original_tool_data, repo_metrics)
                results["would_autocomplete"] = True
                results["warnings"].append("[DRY RUN] Would auto-complete legacy manifest (use without --dry-run to save)")

                # Show what would be added
                new_fields = [k for k in completed_data.keys() if k not in original_tool_data]
                if new_fields:
                    results["warnings"].append(f"[DRY RUN] Would add fields: {', '.join(new_fields)}")

                tool_data = completed_data  # Use completed data for validation

            elif self.autocomplete_enabled and is_legacy:
                tool_data = self.autocomplete_legacy_manifest(original_tool_data, repo_metrics)
                results["autocompleted"] = True

                # Save the completed manifest back to file
                try:
                    # Create backup of original
                    backup_path = tool_path.with_suffix('.json.backup')
                    if not backup_path.exists():
                        with open(backup_path, 'w', encoding='utf-8') as f:
                            json.dump(original_tool_data, f, indent=2, ensure_ascii=False)

                    # Write completed manifest
                    with open(tool_path, 'w', encoding='utf-8') as f:
                        json.dump(tool_data, f, indent=2, ensure_ascii=False)

                    results["warnings"].append("[AUTOCOMPLETE] Legacy manifest auto-completed and saved")

                except Exception as e:
                    results["warnings"].append(f"[WARNING] Could not save auto-completed manifest: {e}")

            # Schema validation on completed data
            schema_errors = self.validate_schema(tool_data)
            if schema_errors:
                results["errors"].extend(schema_errors)
                return results

            results["warnings"].append(repo_status)

            # Installation metadata validation
            installation_errors = self.validate_installation_metadata(tool_data, repo_metrics)
            if installation_errors:
                # Separate errors and warnings
                for error in installation_errors:
                    if error.startswith("[ERROR]"):
                        results["errors"].append(error)
                    else:
                        results["warnings"].append(error)

                # Return early if there are critical errors
                if any(error.startswith("[ERROR]") for error in installation_errors):
                    return results

            # Verify executable patterns work with actual releases
            if tool_data.get("installation"):
                pattern_verification = self._verify_executable_patterns(tool_data["installation"], repo_url)
                results["warnings"].extend(pattern_verification)

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
                results["warnings"].append(f"[WARNING] Score ({results['score']}) below review threshold ({review_threshold})")

            results["valid"] = len(results["errors"]) == 0

        except Exception as e:
            results["errors"].append(f"[ERROR] Validation error: {str(e)}")

        return results
    
    def validate_all_tools(self, tools_dir: Optional[Path] = None, dry_run: bool = False) -> Dict[str, Any]:
        """Validate all tool entries in the tools directory."""
        tools_dir = tools_dir if tools_dir is not None else Path(__file__).parent.parent / "tools"

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
            results = self.validate_single_tool(tool_file, dry_run)
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
        print(f"\n[STATS] Validation Summary")
        print(f"Total tools: {results['total']}")
        print(f"Valid: {results['valid']} [OK]")
        print(f"Invalid: {results['invalid']} [ERROR]")
        
        if results["categories"]:
            print(f"\n[INFO] By Category:")
            for category, stats in results["categories"].items():
                print(f"  {category}: {stats['valid']}[OK] {stats['invalid']}[ERROR]")
        
        autocompleted_count = sum(1 for tool in results["tools"] if tool.get("autocompleted", False))
        would_autocomplete_count = sum(1 for tool in results["tools"] if tool.get("would_autocomplete", False))

        if autocompleted_count > 0:
            print(f"\n[AUTOCOMPLETE] Auto-completed {autocompleted_count} legacy manifests")
        if would_autocomplete_count > 0:
            print(f"\n[DRY RUN] Would auto-complete {would_autocomplete_count} legacy manifests")

        if verbose or results["invalid"] > 0:
            print(f"\n[INFO] Detailed Results:")
            for tool in results["tools"]:
                status = "[OK]" if tool["valid"] else "[ERROR]"
                score = f" (Score: {tool['score']})" if tool.get("score") else ""
                autocompleted = " [AUTOCOMPLETED]" if tool.get("autocompleted") else ""
                would_autocomplete = " [WOULD AUTOCOMPLETE]" if tool.get("would_autocomplete") else ""
                print(f"{status} {tool['file']}{score}{autocompleted}{would_autocomplete}")

                if tool["errors"]:
                    for error in tool["errors"]:
                        print(f"    {error}")

                if verbose and tool["warnings"]:
                    for warning in tool["warnings"]:
                        print(f"    {warning}")
    else:
        # Single tool results
        status = "[VALID]" if results["valid"] else "[INVALID]"
        score = f" (Score: {results['score']})" if results.get("score") else ""
        autocompleted = " [AUTOCOMPLETED]" if results.get("autocompleted") else ""
        would_autocomplete = " [WOULD AUTOCOMPLETE]" if results.get("would_autocomplete") else ""
        print(f"\n{status}: {results['file']}{score}{autocompleted}{would_autocomplete}")

        if results["errors"]:
            print(f"\n[ERRORS]:")
            for error in results["errors"]:
                print(f"  {error}")

        if results["warnings"]:
            print(f"\n[WARNING] Warnings:")
            for warning in results["warnings"]:
                print(f"  {warning}")

        if results["metrics"]:
            print(f"\n[INFO] Metrics:")
            for key, value in results["metrics"].items():
                if value is not None and value != "":
                    print(f"  {key}: {value}")


def main():
    parser = argparse.ArgumentParser(description="Validate Sunshine-AIO tool entries")
    parser.add_argument("--single", "-s", type=str, help="Validate a single tool file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--tools-dir", "-d", type=str, help="Tools directory path")
    parser.add_argument("--schema-dir", type=str, help="Schema directory path")
    parser.add_argument("--no-autocomplete", action="store_true",
                        help="Disable auto-completion of legacy manifests")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be auto-completed without saving changes")

    args = parser.parse_args()

    # Initialize validator
    schema_dir: Optional[Path] = Path(args.schema_dir) if args.schema_dir else None
    validator = ToolValidator(schema_dir)

    # Configure auto-completion
    validator.autocomplete_enabled = not args.no_autocomplete
    if args.dry_run:
        validator.autocomplete_enabled = False  # Don't save in dry run mode
    
    try:
        if args.single:
            # Validate single tool
            tool_path = Path(args.single)
            results = validator.validate_single_tool(tool_path, dry_run=args.dry_run)
            print_results(results, args.verbose)

            # Exit with error code if invalid
            sys.exit(0 if results["valid"] else 1)
        else:
            # Validate all tools
            tools_dir: Optional[Path] = Path(args.tools_dir) if args.tools_dir else None
            results = validator.validate_all_tools(tools_dir, dry_run=args.dry_run)
            print_results(results, args.verbose)

            # Exit with error code if any invalid
            sys.exit(0 if results["invalid"] == 0 else 1)
            
    except KeyboardInterrupt:
        print("\n[STOP] Validation interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n[FATAL ERROR] Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()