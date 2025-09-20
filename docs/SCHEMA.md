# Schema Reference

This document provides detailed information about the JSON schemas used in the Sunshine-AIO Community Tools Registry.

## Tool Entry Schema

The main schema for tool entries is defined in [`schemas/tool-entry.json`](../schemas/tool-entry.json).

### Overview

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://github.com/sunshine-aio/library/schemas/tool-entry.json",
  "title": "Sunshine-AIO Tool Entry",
  "description": "Schema for a tool entry in the Sunshine-AIO community library"
}
```

### Required Fields

#### `name` (string)
- **Pattern**: `^[a-zA-Z0-9\\s\\-_]+$`
- **Length**: 2-50 characters
- **Description**: Tool name (alphanumeric, spaces, hyphens, underscores allowed)
- **Example**: `"Docker Compose Validator"`

#### `slug` (string)
- **Pattern**: `^[a-z0-9-]+$`
- **Length**: 2-50 characters
- **Description**: Unique identifier for the tool (lowercase, hyphens only)
- **Example**: `"docker-compose-validator"`

#### `repository` (string)
- **Format**: URI
- **Pattern**: `^https://github\\.com/[^/]+/[^/]+/?$`
- **Description**: GitHub repository URL
- **Example**: `"https://github.com/username/repository"`

#### `compatibility` (object)
**Required properties:**
- `sunshine` (boolean): Compatible with Sunshine streaming host
- `apollo` (boolean): Compatible with Apollo streaming host
- `platforms` (array): Supported operating systems (lowercase)
  - **Items**: `"windows"`, `"linux"`, `"macos"`, `"web"`
  - **Min Items**: 1
  - **Unique Items**: true

**Example**:
```json
{
  "sunshine": true,
  "apollo": false,
  "platforms": ["windows", "linux"]
}
```

#### `installation` (object)
The installation object supports both single-platform and multi-platform configurations:

**Single Platform Format (Legacy):**
- `type` (string, required): Installation method
  - **Enum**: `"executable"`, `"zip"`, `"script"`, `"msi"`, `"portable"`, `"package-manager"`
- `url` (string): Direct download URL (defaults to latest GitHub release)
- `executable` (string): Specific executable or package name
- `args` (array): Command line arguments for installation
- `postInstall` (string): Relative path to post-installation script
- `checksum` (string): File checksum for integrity verification (empty string allowed)
- `silent` (boolean): Whether installation should run silently (default: true)

**Multi-Platform Format (Recommended):**
- `platforms` (object, required): Platform-specific configurations
  - `windows` (object): Windows installation configuration
  - `linux` (object): Linux installation configuration
  - `macos` (object): macOS installation configuration

Each platform object supports the following properties:
- `type` (string, required): Installation method
  - **Windows**: `"executable"`, `"msi"`, `"zip"`, `"script"`, `"portable"`, `"package-manager"`
  - **Linux**: `"deb"`, `"rpm"`, `"appimage"`, `"zip"`, `"script"`, `"portable"`, `"package-manager"`
  - **macOS**: `"dmg"`, `"pkg"`, `"app"`, `"zip"`, `"script"`, `"portable"`, `"package-manager"`
- `download_strategy` (string): Strategy for downloading files
  - **Enum**: `"direct_url"`, `"github_releases"`, `"github_latest"`, `"package_manager"`
  - **Default**: `"github_releases"`
- `file_pattern` (string): Pattern to match release files (e.g., `"*.exe"`, `"*.AppImage"`)
- `url` (string): Direct download URL
- `executable` (string): Executable name
- `install_flags` (array): Silent installation flags (e.g., `["/S", "/SILENT"]`)
- `install_dir_flag` (string): Flag to specify installation directory (e.g., `"/DIR="`)
- `requires_admin` (boolean): Whether installation requires admin privileges
- `checksum_verification` (boolean): Whether to verify file integrity
- `checksum` (string): File checksum for verification
- `silent` (boolean): Whether installation should run silently

**Important**: For dynamic updates, use GitHub's latest release URLs without version numbers:
- `https://github.com/user/repo/releases/latest/download/Tool-Windows.exe`
- `https://github.com/user/repo/releases/latest/download/Tool-Linux.deb`
- `https://github.com/user/repo/releases/latest/download/Tool-macOS.dmg`

**Single Platform Example:**
```json
{
  "type": "executable",
  "executable": "MyTool.exe",
  "args": ["/S"],
  "silent": true
}
```

**Multi-Platform Example:**
```json
{
  "platforms": {
    "windows": {
      "type": "executable",
      "download_strategy": "github_releases",
      "file_pattern": "*.exe",
      "install_flags": ["/S", "/SILENT", "/VERYSILENT"],
      "install_dir_flag": "/DIR=",
      "requires_admin": true,
      "checksum_verification": true,
      "silent": true
    },
    "linux": {
      "type": "appimage",
      "download_strategy": "github_releases",
      "file_pattern": "*.AppImage",
      "install_flags": ["--silent"],
      "requires_admin": false,
      "checksum_verification": true,
      "silent": true
    },
    "macos": {
      "type": "dmg",
      "download_strategy": "github_releases",
      "file_pattern": "*.dmg",
      "install_flags": ["-allowUntrusted"],
      "requires_admin": false,
      "checksum_verification": true,
      "silent": true
    }
  }
}
```

#### `uninstallation` (object)
**Required properties:**
- `type` (string): Uninstallation method
  - **Enum**: `"executable"`, `"script"`, `"registry"`, `"manual"`

**Optional properties:**
- `path` (string): Path to uninstaller executable or script
- `args` (array): Command line arguments for uninstallation

**Example**:
```json
{
  "type": "registry",
  "args": ["/S"]
}
```

#### `configuration` (object)
**Required properties:**
- `type` (string): Configuration method (empty string allowed)
  - **Enum**: `""`, `"url"`, `"file"`, `"script"`, `"registry"`, `"none"`

**Optional properties:**
- `url` (string): Configuration interface URL
- `file` (string): Configuration file path
- `script` (string): Configuration script path

**Example**:
```json
{
  "type": "url",
  "url": "http://localhost:8080/config"
}
```

### Either/Or Required Fields

You must provide either the legacy format OR the new format:

**Legacy Format:**
- `description` (string): 10-150 characters
- `category` (string): Predefined category from enum
- `license` (string): Open source license from approved list

**New Format:**
- `short-description` (string): 10-100 characters

#### `category` (string) - Legacy Format
- **Enum**: Predefined category list
- **Description**: Primary category classification
- **Available Values**:
  ```json
  [
    "automation/build-tools",
    "automation/deployment",
    "automation/ci-cd",
    "testing/unit-testing",
    "testing/integration-testing",
    "testing/performance",
    "utilities/file-management",
    "utilities/system-tools",
    "utilities/network",
    "development/debugging",
    "development/profiling",
    "security/scanning"
  ]
  ```

#### `license` (string) - Legacy Format
- **Enum**: Compatible open source licenses
- **Available Values**:
  ```json
  [
    "MIT",
    "Apache-2.0",
    "GPL-3.0",
    "BSD-3-Clause",
    "ISC",
    "LGPL-3.0",
    "MPL-2.0",
    "Unlicense"
  ]
  ```

### Optional Fields

#### `verification` (object)
Advanced verification and quality information:
- `status` (string): Verification status
  - **Enum**: `"pending"`, `"verified"`, `"failed"`, `"deprecated"`
  - **Default**: `"pending"`
- `date` (string): Last verification date (ISO format)
- `method` (string): Verification method
  - **Enum**: `"automated"`, `"manual"`, `"community"`
- `score` (integer): Quality score (0-100)

#### `validation` (object)
Security and validation configuration:
- `checksum_required` (boolean): Whether checksum verification is required
- `signature_verification` (boolean): Whether digital signature verification is required
- `trust_level` (string): Trust level for this tool
  - **Enum**: `"unverified"`, `"community_verified"`, `"maintainer_verified"`, `"official"`
- `auto_update` (boolean): Whether this tool supports automatic updates

#### `subcategory` (string)
- **Max Length**: 30 characters
- **Description**: More specific classification within main category
- **Example**: `"docker-tools"`

#### `tags` (array)
- **Items**: Strings matching `^[a-z0-9-]+$`
- **Max Items**: 8
- **Max Item Length**: 20 characters
- **Unique Items**: true
- **Description**: Tags for better searchability
- **Example**: `["docker", "validation", "cli", "yaml"]`

#### `documentation` (string)
- **Format**: URI
- **Description**: Link to tool documentation
- **Example**: `"https://username.github.io/repository"`

#### `platforms` (array) - Legacy Format
- **Items**: Platform names
- **Available Values**: `["Windows", "Linux", "macOS", "Web", "Cross-platform"]`
- **Min Items**: 1
- **Unique Items**: true
- **Example**: `["Linux", "macOS", "Windows"]`

#### `language` (string)
- **Enum**: Primary programming language
- **Available Values**:
  ```json
  [
    "Python", "JavaScript", "TypeScript", "Go", "Rust",
    "Java", "C++", "C#", "PHP", "Ruby", "Shell", "Other"
  ]
  ```

#### `maintainer` (object)
Properties:
- `name` (string, required): Maintainer name (max 50 chars)
- `contact` (string, optional): Email address
- `github` (string, optional): GitHub username (pattern: `^[a-zA-Z0-9-]+$`)

**Example**:
```json
{
  "name": "John Doe",
  "contact": "john@example.com",
  "github": "johndoe"
}
```

#### New Format Optional Fields

#### `short_description` (string)
- **Length**: 10-100 characters
- **Description**: Alternative to description (underscore format)

#### `long-description` (string) or `long_description` (string)
- **Max Length**: 500 characters
- **Description**: Detailed description of the tool features and purpose

#### `author` (string)
- **Max Length**: 100 characters
- **Description**: Tool author or organization name

#### `website` (string)
- **Format**: URI
- **Description**: Official website URL

#### `screenshots` (array)
- **Items**: Relative path strings to screenshot images
- **Max Items**: 10
- **Description**: Screenshots of the tool interface

#### `icon` (string)
- **Description**: Relative path to tool icon image

### Auto-Generated Fields

These fields are automatically populated and should not be included in manual entries:

#### `metrics` (object)
Automatically collected GitHub metrics:
- `stars` (integer): GitHub stars count
- `forks` (integer): GitHub forks count
- `last_commit` (string, date): Date of last commit

#### `verification` (object)
Verification status and quality information:
- `status` (enum): `"pending"`, `"verified"`, `"failed"`, `"deprecated"`
- `date` (string, date-time): Last verification date
- `method` (enum): `"automated"`, `"manual"`, `"community"`
- `score` (integer, 0-100): Quality score

#### `added_date` (string, date)
Date when tool was added to registry

#### `contributed_by` (string)
GitHub username of contributor

### Complete Example (New Format)

```json
{
  "name": "Docker Compose Validator",
  "slug": "docker-compose-validator",
  "short-description": "A powerful CLI tool for validating Docker Compose files",
  "long_description": "Comprehensive validation tool that checks Docker Compose files for syntax errors, best practices, and security issues with detailed error reporting and suggestions.",
  "tags": ["docker", "validation", "cli", "yaml"],
  "repository": "https://github.com/username/docker-compose-validator",
  "documentation": "https://username.github.io/docker-compose-validator",
  "author": "John Doe",
  "website": "https://docker-validator.example.com",
  "compatibility": {
    "sunshine": true,
    "apollo": false,
    "platforms": ["windows", "linux", "macos"]
  },
  "installation": {
    "type": "executable",
    "url": "https://github.com/username/docker-compose-validator/releases/latest",
    "args": ["/S"],
    "silent": true,
    "checksum": "sha256:abc123..."
  },
  "uninstallation": {
    "type": "registry",
    "args": ["/S"]
  },
  "configuration": {
    "type": "url",
    "url": "http://localhost:8080/config"
  },
  "screenshots": ["screenshots/main.png", "screenshots/config.png"],
  "icon": "icons/validator.png"
}
```

### Legacy Format Example

```json
{
  "name": "Docker Compose Validator",
  "description": "A powerful CLI tool for validating Docker Compose files with comprehensive error reporting",
  "category": "utilities/file-management",
  "subcategory": "docker-tools",
  "tags": ["docker", "validation", "cli", "yaml"],
  "repository": "https://github.com/username/docker-compose-validator",
  "documentation": "https://username.github.io/docker-compose-validator",
  "license": "MIT",
  "platforms": ["Linux", "macOS", "Windows"],
  "language": "Python",
  "slug": "docker-compose-validator",
  "compatibility": {
    "sunshine": true,
    "apollo": false,
    "platforms": ["windows", "linux", "macos"]
  },
  "installation": {
    "type": "executable",
    "silent": true
  },
  "uninstallation": {
    "type": "registry"
  },
  "configuration": {
    "type": "url",
    "url": "http://localhost:8080/config"
  },
  "maintainer": {
    "name": "John Doe",
    "github": "johndoe",
    "contact": "john@example.com"
  },
  "added_date": "2024-01-15",
  "contributed_by": "contributor-username"
}
```

## 🏷️ Category Schema

The category definitions are stored in [`schemas/category.json`](../schemas/category.json).

### Structure

Categories follow a hierarchical structure:

```json
{
  "categories": {
    "automation": {
      "name": "Automation",
      "description": "Tools for automating development and deployment processes",
      "icon": "🚀",
      "subcategories": {
        "build-tools": {
          "name": "Build Tools",
          "description": "Tools for building and compiling applications"
        }
      }
    }
  }
}
```

### Available Categories

| Category | Subcategories | Description |
|----------|---------------|-------------|
| `automation` | `build-tools`, `deployment`, `ci-cd` | Process automation tools |
| `testing` | `unit-testing`, `integration-testing`, `performance` | Testing frameworks and tools |
| `utilities` | `file-management`, `system-tools`, `network` | General purpose utilities |
| `development` | `debugging`, `profiling` | Development and debugging tools |
| `security` | `scanning` | Security analysis tools |

## ⚙️ Validation Rules

The validation rules are defined in [`schemas/validation-rules.json`](../schemas/validation-rules.json).

### Quality Thresholds

```json
{
  "quality_thresholds": {
    "minimum_stars": 10,
    "minimum_score": 60,
    "max_days_since_commit": 365
  }
}
```

### URL Validation

```json
{
  "url_validation": {
    "allowed_domains": [
      "github.com",
      "docs.github.com",
      "readthedocs.io",
      "gitbook.io"
    ],
    "required_status_codes": [200, 301, 302]
  }
}
```

### Content Validation

```json
{
  "content_validation": {
    "forbidden_words": ["hack", "crack", "exploit", "malware"],
    "required_readme_sections": ["installation", "usage", "license"]
  }
}
```

### Scoring Weights

```json
{
  "scoring_weights": {
    "stars": 0.3,
    "forks": 0.2,
    "recent_activity": 0.2,
    "documentation": 0.15,
    "license": 0.1,
    "community": 0.05
  }
}
```

### Automation Rules

```json
{
  "automation_rules": {
    "auto_verify_threshold": 85,
    "auto_deprecate_days": 730,
    "review_required_score": 50
  }
}
```

## 🔧 Validation Process

### Schema Validation

1. **JSON Syntax**: Valid JSON format
2. **Required Fields**: All required fields present (name, repository, slug, compatibility, installation, uninstallation, configuration)
3. **Either/Or Fields**: Either legacy format (description, category, license) OR new format (short-description)
4. **Field Types**: Correct data types for each field
5. **Field Constraints**: Length, pattern, and enum validations
6. **Field Relationships**: Logical consistency between fields

### Autocompletion System

The validation script includes intelligent autocompletion for legacy manifests:

1. **Missing Field Detection**: Identifies missing required fields for new schema format
2. **Repository Metrics**: Automatically fetches GitHub repository data to populate missing metrics
3. **Smart Defaults**: Applies sensible defaults for installation, uninstallation, and configuration
4. **Dry-Run Mode**: Preview changes before applying with `--dry-run` flag
5. **Legacy Support**: Can be disabled with `--no-autocomplete` flag

### Extended Validation

1. **URL Accessibility**: Repository and documentation URLs are reachable
2. **GitHub Integration**: Repository exists and is publicly accessible
3. **License Compatibility**: License is open source and approved
4. **Content Safety**: No forbidden words or malicious indicators
5. **Duplicate Detection**: Tool slug and repository are unique
6. **Compatibility Validation**: Streaming host compatibility flags are properly set
7. **Installation Validation**: Installation types and configurations are valid

### Quality Scoring

Tools receive a quality score (0-100) based on:

- **Repository Activity (25%)**
  - Recent commits (last 30, 90, 365 days)
  - Maintenance regularity

- **Community Engagement (30%)**
  - GitHub stars
  - Fork count
  - Contributor count

- **Documentation Quality (15%)**
  - README comprehensiveness
  - External documentation availability

- **Technical Quality (20%)**
  - CI/CD presence
  - Test coverage indicators
  - Release management

- **Completeness (10%)**
  - Profile completion
  - Metadata richness
  - Streaming host compatibility
  - Installation/configuration completeness

## 🚨 Error Messages

### Common Validation Errors

**Schema Validation Errors:**
```
❌ Schema validation failed: 'name' is a required property
❌ Schema validation failed: 'example-name!' does not match pattern '^[a-zA-Z0-9\\s\\-_]+$'
❌ Schema validation failed: 'slug' does not match pattern '^[a-z0-9-]+$'
❌ Schema validation failed: 'description' should be at most 150 characters
❌ Schema validation failed: 'invalid-category' is not one of the allowed values
❌ Schema validation failed: 'repository' does not match pattern '^https://github\\.com/[^/]+/[^/]+/?$'
❌ Schema validation failed: 'tags[0]' does not match pattern '^[a-z0-9-]+$'
❌ Schema validation failed: 'checksum' does not match pattern '^(|sha256:[a-fA-F0-9]+|md5:[a-fA-F0-9]+|sha1:[a-fA-F0-9]+)$'
❌ Schema validation failed: 'compatibility' is a required property
❌ Schema validation failed: 'installation' is a required property
❌ Schema validation failed: 'uninstallation' is a required property
❌ Schema validation failed: 'configuration' is a required property
```

**URL Validation Errors:**
```
❌ Repository URL returned HTTP 404
❌ Documentation timeout
❌ Not a GitHub URL
❌ Invalid GitHub URL format
```

**Content Validation Warnings:**
```
⚠️ Contains potentially unsafe word: 'hack'
⚠️ Repository is archived
⚠️ Low star count (5)
⚠️ Score (45) below review threshold (50)
```

**Autocompletion Messages:**
```
✅ Auto-completed missing field: slug
✅ Auto-completed missing field: compatibility
✅ Auto-completed missing field: installation
ℹ️ Use --dry-run to preview autocompletion changes
ℹ️ Use --no-autocomplete to disable autocompletion
```

## 📊 API Schema

The generated API files follow these schemas:

### Catalog Schema (`api/catalog.json`)

```json
{
  "version": "1.0.0",
  "generated": "2024-01-15T10:30:00Z",
  "total_tools": 150,
  "tools": [
    {
      "id": "tool-name",
      "slug": "tool-name",
      "name": "Tool Name",
      "description": "...",
      "category": "automation/build-tools",
      "compatibility": {
        "sunshine": true,
        "apollo": false,
        "platforms": ["windows", "linux"]
      },
      "installation": {
        "type": "executable",
        "silent": true
      },
      "verification": {
        "status": "verified",
        "score": 85
      },
      "metrics": {
        "stars": 125,
        "forks": 23
      }
    }
  ]
}
```

### Search Index Schema (`api/search.json`)

```json
{
  "version": "1.0.0",
  "generated": "2024-01-15T10:30:00Z",
  "indexes": {
    "by_name": {
      "docker": ["tool1", "tool2"],
      "build": ["tool1", "tool3"]
    },
    "by_tag": {
      "automation": ["tool1", "tool2"]
    },
    "by_category": {
      "automation/build-tools": ["tool1", "tool2"]
    },
    "by_compatibility": {
      "sunshine": ["tool1", "tool2"],
      "apollo": ["tool3"]
    }
  },
  "filters": {
    "categories": ["automation/build-tools", "testing/unit-testing"],
    "languages": ["Python", "Go", "JavaScript"],
    "licenses": ["MIT", "Apache-2.0"],
    "platforms": ["Linux", "Windows", "macOS"],
    "installation_types": ["executable", "zip", "script"],
    "streaming_hosts": ["sunshine", "apollo"]
  }
}
```

## 🛠️ Schema Development

### Adding New Fields

1. Update the schema file (`schemas/tool-entry.json`)
2. Update validation logic (`scripts/validate.py`)
3. Update documentation (this file)
4. Update templates (issue/PR templates)
5. Test with example tools

### Schema Versioning

- Schema changes are versioned
- Backward compatibility is maintained when possible
- Breaking changes require migration scripts
- Version information is included in generated APIs

### Testing Schemas

```bash
# Validate schema files
python -c "
import json
from pathlib import Path
schema_files = ['schemas/tool-entry.json', 'schemas/category.json']
for file in schema_files:
    with open(file) as f:
        json.load(f)
    print(f'✅ {file}')
"

# Test against example data
python scripts/validate.py --single examples/example-tool.json

# Test with autocompletion
python scripts/validate.py --dry-run

# Test catalog generation
python scripts/generate-catalog.py
```

## 📚 References

- [JSON Schema Draft 7 Specification](https://json-schema.org/draft-07/schema)
- [JSON Schema Validation Keywords](https://json-schema.org/understanding-json-schema/reference/generic.html)
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [SPDX License List](https://spdx.org/licenses/)