# 📋 Schema Reference

This document provides detailed information about the JSON schemas used in the Sunshine-AIO Community Tools Registry.

## 📄 Tool Entry Schema

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
- **Pattern**: `^[a-zA-Z0-9-_]+$`
- **Length**: 2-50 characters
- **Description**: Tool name using only alphanumeric characters, hyphens, and underscores
- **Example**: `"docker-compose-validator"`

#### `description` (string)
- **Length**: 10-150 characters
- **Description**: Brief, clear description of what the tool does
- **Example**: `"A powerful CLI tool for validating Docker Compose files with comprehensive error reporting"`

#### `category` (string)
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

#### `repository` (string)
- **Format**: URI
- **Pattern**: `^https://github\\.com/[^/]+/[^/]+/?$`
- **Description**: GitHub repository URL
- **Example**: `"https://github.com/username/repository"`

#### `license` (string)
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

#### `platforms` (array)
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

### Complete Example

```json
{
  "name": "docker-compose-validator",
  "description": "A powerful CLI tool for validating Docker Compose files with comprehensive error reporting",
  "category": "utilities/file-management",
  "subcategory": "docker-tools",
  "tags": ["docker", "validation", "cli", "yaml"],
  "repository": "https://github.com/username/docker-compose-validator",
  "documentation": "https://username.github.io/docker-compose-validator", 
  "license": "MIT",
  "platforms": ["Linux", "macOS", "Windows"],
  "language": "Python",
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
2. **Required Fields**: All required fields present
3. **Field Types**: Correct data types for each field
4. **Field Constraints**: Length, pattern, and enum validations
5. **Field Relationships**: Logical consistency between fields

### Extended Validation

1. **URL Accessibility**: Repository and documentation URLs are reachable
2. **GitHub Integration**: Repository exists and is publicly accessible
3. **License Compatibility**: License is open source and approved
4. **Content Safety**: No forbidden words or malicious indicators
5. **Duplicate Detection**: Tool name and repository are unique

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
  - License compliance

## 🚨 Error Messages

### Common Validation Errors

**Schema Validation Errors:**
```
❌ Schema validation failed: 'name' is a required property
❌ Schema validation failed: 'example-name!' does not match '^[a-zA-Z0-9-_]+$'
❌ Schema validation failed: 'description' should be at most 150 characters
❌ Schema validation failed: 'invalid-category' is not one of the allowed values
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
      "name": "Tool Name", 
      "description": "...",
      "category": "automation/build-tools",
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
    }
  },
  "filters": {
    "categories": ["automation/build-tools", "testing/unit-testing"],
    "languages": ["Python", "Go", "JavaScript"],
    "licenses": ["MIT", "Apache-2.0"],
    "platforms": ["Linux", "Windows", "macOS"]
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

# Test catalog generation
python scripts/generate-catalog.py
```

## 📚 References

- [JSON Schema Draft 7 Specification](https://json-schema.org/draft-07/schema)
- [JSON Schema Validation Keywords](https://json-schema.org/understanding-json-schema/reference/generic.html)
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [SPDX License List](https://spdx.org/licenses/)