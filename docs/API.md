# 📊 API Documentation

The Sunshine-AIO Community Tools Registry provides several JSON APIs for programmatic access to the tool catalog. All APIs are available via GitHub's raw content CDN.

## 🌐 Base URL

```
https://raw.githubusercontent.com/sunshine-aio/library/main/api/
```

## 📋 Available Endpoints

### Main Catalog
**Endpoint**: `/catalog.json`  
**Description**: Complete tool listing with full metadata  
**Update Frequency**: On every main branch push

### Categories Index  
**Endpoint**: `/categories.json`  
**Description**: Category-based organization with statistics  
**Update Frequency**: On every main branch push

### Search Index
**Endpoint**: `/search.json`  
**Description**: Optimized search indexes and filters  
**Update Frequency**: On every main branch push

### Statistics
**Endpoint**: `/stats.json`  
**Description**: Comprehensive registry analytics  
**Update Frequency**: On every main branch push

### API Manifest
**Endpoint**: `/manifest.json`  
**Description**: API metadata and usage information  
**Update Frequency**: On every main branch push

## 🔍 Detailed API Reference

### 1. Main Catalog (`/catalog.json`)

The primary API containing all tools with comprehensive metadata.

#### Structure
```json
{
  "version": "1.0.0",
  "generated": "2024-01-15T10:30:00Z",
  "total_tools": 150,
  "tools": [
    {
      "id": "tool-name",
      "name": "Tool Display Name",
      "description": "Brief description of the tool",
      "category": "automation/build-tools",
      "subcategory": "docker-tools",
      "tags": ["docker", "build", "automation"],
      "repository": "https://github.com/owner/repo",
      "documentation": "https://owner.github.io/repo",
      "license": "MIT",
      "platforms": ["Linux", "macOS", "Windows"],
      "language": "Python",
      "verification": {
        "status": "verified",
        "score": 85,
        "date": "2024-01-15T09:00:00Z"
      },
      "metrics": {
        "stars": 125,
        "forks": 23,
        "last_commit": "2024-01-10"
      },
      "maintainer": {
        "name": "John Doe",
        "github": "johndoe"
      },
      "added_date": "2024-01-01",
      "contributed_by": "contributor",
      "_metadata": {
        "file_path": "automation/build-tools/tool-name.json",
        "category_path": "automation/build-tools"
      }
    }
  ]
}
```

#### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique tool identifier (same as name) |
| `name` | string | Tool name |
| `description` | string | Brief tool description |
| `category` | string | Primary category classification |
| `subcategory` | string | Optional subcategory |
| `tags` | array | Search tags |
| `repository` | string | GitHub repository URL |
| `documentation` | string | Documentation URL (optional) |
| `license` | string | Open source license |
| `platforms` | array | Supported platforms |
| `language` | string | Primary programming language |
| `verification.status` | string | Verification status: "verified", "pending", "failed" |
| `verification.score` | integer | Quality score (0-100) |
| `verification.date` | string | Last verification timestamp |
| `metrics.stars` | integer | GitHub stars count |
| `metrics.forks` | integer | GitHub forks count |
| `metrics.last_commit` | string | Last commit date |
| `maintainer` | object | Tool maintainer information |
| `added_date` | string | Date added to registry |
| `contributed_by` | string | GitHub username of contributor |

#### Usage Examples

**Fetch all tools:**
```bash
curl https://raw.githubusercontent.com/sunshine-aio/library/main/api/catalog.json
```

**Filter verified tools (using jq):**
```bash
curl -s https://raw.githubusercontent.com/sunshine-aio/library/main/api/catalog.json | \
  jq '.tools[] | select(.verification.status == "verified")'
```

**Find tools by category:**
```bash
curl -s https://raw.githubusercontent.com/sunshine-aio/library/main/api/catalog.json | \
  jq '.tools[] | select(.category == "automation/build-tools")'
```

**Get top-rated tools:**
```bash
curl -s https://raw.githubusercontent.com/sunshine-aio/library/main/api/catalog.json | \
  jq '.tools | sort_by(-.verification.score) | .[0:10]'
```

### 2. Categories Index (`/categories.json`)

Organized view of tools grouped by categories with statistics.

#### Structure
```json
{
  "version": "1.0.0", 
  "generated": "2024-01-15T10:30:00Z",
  "total_categories": 12,
  "categories": {
    "automation/build-tools": {
      "name": "Build Tools",
      "subcategory": "Build Tools", 
      "full_path": "automation/build-tools",
      "tools": [
        {
          "id": "docker-buildx",
          "name": "Docker Buildx",
          "description": "Extended build capabilities for Docker",
          "verification_status": "verified",
          "score": 92,
          "stars": 156
        }
      ],
      "stats": {
        "total": 15,
        "verified": 12,
        "average_score": 78.5,
        "total_stars": 2340,
        "languages": ["Go", "Python", "Shell"],
        "licenses": ["Apache-2.0", "MIT"]
      }
    }
  }
}
```

#### Usage Examples

**Browse by category:**
```bash
curl -s https://raw.githubusercontent.com/sunshine-aio/library/main/api/categories.json | \
  jq '.categories["automation/build-tools"].tools'
```

**Category statistics:**
```bash
curl -s https://raw.githubusercontent.com/sunshine-aio/library/main/api/categories.json | \
  jq '.categories | to_entries | map({category: .key, stats: .value.stats})'
```

### 3. Search Index (`/search.json`)

Optimized indexes for fast searching and filtering.

#### Structure
```json
{
  "version": "1.0.0",
  "generated": "2024-01-15T10:30:00Z", 
  "indexes": {
    "by_name": {
      "docker": ["docker-buildx", "docker-compose-validator"],
      "build": ["docker-buildx", "webpack-optimizer"],
      "test": ["jest-runner", "pytest-fixtures"]
    },
    "by_tag": {
      "automation": ["docker-buildx", "ansible-runner"],
      "testing": ["jest-runner", "pytest-fixtures"]
    },
    "by_category": {
      "automation/build-tools": ["docker-buildx", "webpack-optimizer"],
      "testing/unit-testing": ["jest-runner", "pytest-fixtures"]
    },
    "by_language": {
      "Python": ["pytest-fixtures", "flask-validator"],
      "JavaScript": ["jest-runner", "webpack-optimizer"]
    },
    "by_license": {
      "MIT": ["jest-runner", "flask-validator"],
      "Apache-2.0": ["docker-buildx", "ansible-runner"]
    },
    "by_platform": {
      "Linux": ["docker-buildx", "pytest-fixtures"],
      "Windows": ["powershell-tools", "dotnet-helpers"]
    }
  },
  "filters": {
    "categories": ["automation/build-tools", "testing/unit-testing"],
    "languages": ["Python", "Go", "JavaScript"],
    "licenses": ["MIT", "Apache-2.0", "GPL-3.0"],
    "platforms": ["Linux", "Windows", "macOS"],
    "tags": ["docker", "testing", "automation"],
    "verification_statuses": ["verified", "pending", "failed"]
  }
}
```

#### Usage Examples

**Search by keyword:**
```bash
# Find tools containing "docker" in name or description
curl -s https://raw.githubusercontent.com/sunshine-aio/library/main/api/search.json | \
  jq '.indexes.by_name.docker'
```

**Filter by tag:**
```bash
# Find all automation tools
curl -s https://raw.githubusercontent.com/sunshine-aio/library/main/api/search.json | \
  jq '.indexes.by_tag.automation'
```

**Get available filters:**
```bash
# List all available programming languages
curl -s https://raw.githubusercontent.com/sunshine-aio/library/main/api/search.json | \
  jq '.filters.languages'
```

### 4. Statistics (`/stats.json`)

Comprehensive analytics about the registry.

#### Structure
```json
{
  "version": "1.0.0",
  "generated": "2024-01-15T10:30:00Z",
  "overview": {
    "total_tools": 150,
    "verified_tools": 120,
    "pending_tools": 25,
    "failed_tools": 5,
    "total_stars": 15420,
    "total_forks": 2340,
    "average_score": 76.8
  },
  "categories": {
    "automation/build-tools": {
      "count": 25,
      "average_score": 82.1,
      "total_stars": 3450
    }
  },
  "languages": {
    "Python": {
      "count": 45,
      "average_score": 78.9
    },
    "Go": {
      "count": 32,
      "average_score": 81.2
    }
  },
  "licenses": {
    "MIT": 65,
    "Apache-2.0": 42,
    "GPL-3.0": 18
  },
  "platforms": {
    "Linux": 142,
    "macOS": 128,
    "Windows": 95
  },
  "quality_distribution": {
    "excellent": 45,  // 90-100
    "good": 52,       // 70-89  
    "fair": 38,       // 50-69
    "poor": 15        // 0-49
  },
  "activity_analysis": {
    "active": 89,     // Activity in last 30 days
    "moderate": 45,   // Activity in last 6 months
    "inactive": 16    // No activity in 6+ months
  },
  "top_tools": {
    "by_stars": [
      {
        "id": "kubernetes-cli",
        "name": "Kubernetes CLI",
        "category": "automation/deployment",
        "stars": 2340,
        "score": 98
      }
    ],
    "by_score": [
      {
        "id": "perfect-tool",
        "name": "Perfect Tool",
        "category": "utilities/system-tools", 
        "score": 100,
        "stars": 156
      }
    ],
    "by_recent_activity": [
      {
        "id": "active-tool",
        "name": "Very Active Tool",
        "category": "development/debugging",
        "last_commit": "2024-01-14"
      }
    ]
  }
}
```

#### Usage Examples

**Registry overview:**
```bash
curl -s https://raw.githubusercontent.com/sunshine-aio/library/main/api/stats.json | \
  jq '.overview'
```

**Language distribution:**
```bash
curl -s https://raw.githubusercontent.com/sunshine-aio/library/main/api/stats.json | \
  jq '.languages | to_entries | sort_by(-.value.count)'
```

**Quality metrics:**
```bash
curl -s https://raw.githubusercontent.com/sunshine-aio/library/main/api/stats.json | \
  jq '.quality_distribution'
```

### 5. API Manifest (`/manifest.json`)

Metadata about the API itself.

#### Structure
```json
{
  "version": "1.0.0",
  "generated": "2024-01-15T10:30:00Z",
  "catalogs": {
    "catalog.json": {
      "path": "api/catalog.json",
      "size_bytes": 245760,
      "size_kb": 240.0,
      "last_modified": "2024-01-15T10:30:00Z"
    }
  },
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
```

## 🚀 Integration Examples

### JavaScript/Node.js

```javascript
// Fetch all tools
async function getAllTools() {
  const response = await fetch('https://raw.githubusercontent.com/sunshine-aio/library/main/api/catalog.json');
  const catalog = await response.json();
  return catalog.tools;
}

// Search tools by category
async function getToolsByCategory(category) {
  const catalog = await getAllTools();
  return catalog.filter(tool => tool.category === category);
}

// Find tools by tag
async function searchByTag(tag) {
  const response = await fetch('https://raw.githubusercontent.com/sunshine-aio/library/main/api/search.json');
  const searchIndex = await response.json();
  const toolIds = searchIndex.indexes.by_tag[tag] || [];
  
  const catalog = await getAllTools();
  return catalog.filter(tool => toolIds.includes(tool.id));
}
```

### Python

```python
import requests
import json

BASE_URL = "https://raw.githubusercontent.com/sunshine-aio/library/main/api"

def get_all_tools():
    """Fetch all tools from the catalog."""
    response = requests.get(f"{BASE_URL}/catalog.json")
    response.raise_for_status()
    return response.json()["tools"]

def search_tools(query):
    """Search tools by name or description."""
    response = requests.get(f"{BASE_URL}/search.json")
    response.raise_for_status()
    search_index = response.json()
    
    # Find tools matching query in name index
    matching_ids = set()
    for word, tool_ids in search_index["indexes"]["by_name"].items():
        if query.lower() in word.lower():
            matching_ids.update(tool_ids)
    
    # Get full tool details
    tools = get_all_tools()
    return [tool for tool in tools if tool["id"] in matching_ids]

def get_verified_tools():
    """Get only verified tools."""
    tools = get_all_tools()
    return [tool for tool in tools if tool["verification"]["status"] == "verified"]

def get_category_stats():
    """Get statistics by category."""
    response = requests.get(f"{BASE_URL}/categories.json")
    response.raise_for_status()
    categories = response.json()["categories"]
    
    return {
        category: data["stats"]
        for category, data in categories.items()
    }
```

### Go

```go
package main

import (
    "encoding/json"
    "fmt"
    "net/http"
)

const baseURL = "https://raw.githubusercontent.com/sunshine-aio/library/main/api"

type Tool struct {
    ID           string `json:"id"`
    Name         string `json:"name"`
    Description  string `json:"description"`
    Category     string `json:"category"`
    Repository   string `json:"repository"`
    License      string `json:"license"`
    Verification struct {
        Status string `json:"status"`
        Score  int    `json:"score"`
    } `json:"verification"`
}

type Catalog struct {
    Version    string `json:"version"`
    Generated  string `json:"generated"`
    TotalTools int    `json:"total_tools"`
    Tools      []Tool `json:"tools"`
}

func getAllTools() (*Catalog, error) {
    resp, err := http.Get(baseURL + "/catalog.json")
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    var catalog Catalog
    if err := json.NewDecoder(resp.Body).Decode(&catalog); err != nil {
        return nil, err
    }
    
    return &catalog, nil
}

func getVerifiedTools() ([]Tool, error) {
    catalog, err := getAllTools()
    if err != nil {
        return nil, err
    }
    
    var verified []Tool
    for _, tool := range catalog.Tools {
        if tool.Verification.Status == "verified" {
            verified = append(verified, tool)
        }
    }
    
    return verified, nil
}
```

### Shell/Bash

```bash
#!/bin/bash

BASE_URL="https://raw.githubusercontent.com/sunshine-aio/library/main/api"

# Get all tools
get_all_tools() {
    curl -s "${BASE_URL}/catalog.json"
}

# Get tools by category
get_tools_by_category() {
    local category="$1"
    get_all_tools | jq --arg cat "$category" '.tools[] | select(.category == $cat)'
}

# Get verified tools
get_verified_tools() {
    get_all_tools | jq '.tools[] | select(.verification.status == "verified")'
}

# Search tools by tag
search_by_tag() {
    local tag="$1"
    local search_index=$(curl -s "${BASE_URL}/search.json")
    local tool_ids=$(echo "$search_index" | jq -r --arg tag "$tag" '.indexes.by_tag[$tag][]?')
    
    if [[ -n "$tool_ids" ]]; then
        local catalog=$(get_all_tools)
        echo "$tool_ids" | while read -r tool_id; do
            echo "$catalog" | jq --arg id "$tool_id" '.tools[] | select(.id == $id)'
        done
    fi
}

# Get registry statistics
get_stats() {
    curl -s "${BASE_URL}/stats.json" | jq '.overview'
}

# Usage examples
echo "=== Registry Statistics ==="
get_stats

echo -e "\n=== Verified Tools Count ==="
get_verified_tools | jq -s 'length'

echo -e "\n=== Build Tools ==="
get_tools_by_category "automation/build-tools" | jq -r '.name'
```

## ⚡ Performance Tips

### Caching
- APIs are served via CDN and can be cached
- Use ETags or Last-Modified headers for cache validation
- Consider local caching for frequently accessed data

### Filtering
- Use the search index for efficient lookups
- Filter on the client side after fetching
- Consider pagination for large result sets

### Rate Limits
- No explicit rate limits, but be respectful
- Use appropriate caching to minimize requests
- Consider implementing exponential backoff

## 🔄 Update Frequency

- **Main Branch Pushes**: APIs are updated automatically
- **Verification Status**: Updated during scheduled verification runs
- **Statistics**: Recalculated with each catalog update
- **Real-time**: APIs reflect the latest state of the main branch

## 📚 API Versioning

- **Current Version**: 1.0.0 (semantic versioning)
- **Breaking Changes**: Will increment major version
- **Backward Compatibility**: Maintained when possible
- **Deprecation**: Old versions supported for transition period

## ❓ Troubleshooting

### Common Issues

**404 Not Found**
- Verify the correct URL and branch
- Check if the API file exists in the repository

**JSON Parse Error**  
- API may be updating during request
- Retry after a short delay
- Validate JSON structure

**Empty Results**
- Check if filters are too restrictive
- Verify search terms are correct
- Confirm tools exist in the category

**Stale Data**
- APIs update on main branch changes
- Check the `generated` timestamp
- Clear local cache if needed

### Support

For API-related issues:
1. Check the [manifest.json](https://raw.githubusercontent.com/sunshine-aio/library/main/api/manifest.json) for current status
2. Review the repository's latest commits
3. Open an issue with API-specific details