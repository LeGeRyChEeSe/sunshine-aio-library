# Sunshine-AIO-Library

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Validate Tools](https://github.com/LeGeRyChEeSe/sunshine-aio-library/actions/workflows/validate-tools.yml/badge.svg)](https://github.com/LeGeRyChEeSe/sunshine-aio-library/actions/workflows/validate-tools.yml)
[![Tools Count](https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/LeGeRyChEeSe/sunshine-aio-library/main/api/stats.json&query=$.overview.total_tools&label=tools&color=blue)](https://github.com/LeGeRyChEeSe/sunshine-aio-library/blob/main/api/catalog.json)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![GitHub Issues](https://img.shields.io/github/issues/LeGeRyChEeSe/sunshine-aio-library)](https://github.com/LeGeRyChEeSe/sunshine-aio-library/issues)
[![GitHub Stars](https://img.shields.io/github/stars/LeGeRyChEeSe/sunshine-aio-library)](https://github.com/LeGeRyChEeSe/sunshine-aio-library/stargazers)

A curated, community-driven registry of high-quality tools for the Sunshine-AIO ecosystem.

## Related Project

This library is used by the main [Sunshine-AIO](https://github.com/LeGeRyChEeSe/Sunshine-AIO) project, which is a desktop application that allows users to easily install, manage, and configure local streaming tools.

## About

This repository serves as a schema-driven tool registry for the Sunshine-AIO application, enabling users to:

*   Easily discover and install tools for local streaming
*   Manage installations, configurations, and updates of these tools
*   Contribute to the community by proposing new tools

## Features

- **Schema-driven validation** with regex patterns ensures data consistency and quality
- **Automated tool verification** checks repository accessibility and activity
- **Quality scoring system** provides objective tool assessment (0-100 scale)
- **RESTful APIs** for programmatic access
- **Category-based organization** enables efficient tool discovery

## Getting Started

### Prerequisites
- Python 3.11 or higher
- Git for version control

### Installation

**Step 1: Clone the repository**
```bash
git clone https://github.com/LeGeRyChEeSe/sunshine-aio-library.git
cd sunshine-aio-library
```

**Step 2: Set up virtual environment**

*On Windows (PowerShell):*
```powershell
# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    python -m venv venv
}

# Activate virtual environment
venv\Scripts\Activate.ps1

# Install dependencies from requirements.txt
pip install -r requirements.txt
```

*On Linux/macOS:*
```bash
# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies from requirements.txt
pip install -r requirements.txt
```

**Step 3: Verify installation**
```bash
python -c "import jsonschema, requests; print('Dependencies installed successfully!')"
```

### Quick Start

**Important**: Make sure your virtual environment is activated before running these commands.

```bash
# Activate virtual environment first
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate

# Validate all tools with autocompletion
python scripts/validate.py --verbose

# Generate API catalogs
python scripts/generate-catalog.py --manifest

# Verify tool accessibility
python scripts/verify-tools.py

# View what would be autocompleted (dry run)
python scripts/validate.py --dry-run
```

## How to Add a Tool

1. **Fork this repository**
2. **Set up environment**: Follow the installation steps above with virtual environment
3. **Create tool entry**: Add a JSON file in the appropriate category folder under `tools/`
4. **Validate**: Use `python scripts/validate.py --single tools/category/your-tool.json` (includes pattern validation)
5. **Test autocompletion**: Use `python scripts/validate.py --dry-run --single tools/category/your-tool.json` to see suggested completions
6. **Submit PR**: Create a pull request with your tool entry
7. **Review**: Wait for community validation and approval

### Tool Entry Format

**Field Pattern Requirements:**
- `name`: Pattern `^[a-zA-Z0-9\s\-_]+$` (2-50 chars)
- `slug`: Pattern `^[a-z0-9-]+$` (2-50 chars, unique)
- `repository`: Pattern `^https://github\.com/[^/]+/[^/]+/?$`
- `tags`: Pattern `^[a-z0-9-]+$` per tag (max 8 tags, 20 chars each)
- `checksum`: Pattern `^(|sha256:[a-fA-F0-9]+|md5:[a-fA-F0-9]+|sha1:[a-fA-F0-9]+)$`

**Basic format (legacy compatibility):**
```json
{
  "name": "Example Tool",
  "slug": "example-tool",
  "description": "A powerful example tool for automation",
  "category": "utilities/system-tools",
  "tags": ["automation", "system"],
  "repository": "https://github.com/owner/repo",
  "documentation": "https://owner.github.io/repo",
  "license": "MIT",
  "platforms": ["Windows", "Linux", "macOS"],
  "language": "Python",
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
    "type": "none"
  }
}
```

**Complete format with installation support:**
```json
{
  "name": "Advanced Tool",
  "slug": "advanced-tool",
  "short-description": "A powerful tool with automated installation",
  "long-description": "This tool provides comprehensive automation capabilities with seamless installation and configuration management.",
  "author": "Developer Name",
  "website": "https://tool.example.com",
  "repository": "https://github.com/owner/repo",
  "tags": ["automation", "system"],
  "compatibility": {
    "sunshine": true,
    "apollo": false,
    "platforms": ["windows", "linux", "macos"]
  },
  "installation": {
    "type": "executable",
    "args": ["--silent", "--install"],
    "postInstall": "setup.ps1",
    "checksum": "sha256:abc123...",
    "silent": true
  },
  "uninstallation": {
    "type": "executable",
    "path": "%PROGRAMFILES%\\Tool\\uninstall.exe",
    "args": ["--silent"]
  },
  "configuration": {
    "type": "url",
    "url": "http://localhost:8080/config"
  },
  "screenshots": ["screenshots/main.png"],
  "icon": "icon.png"
}
```

### Installation Types Supported

- **`executable`**: Windows .exe, Linux/macOS binaries
- **`zip`**: Compressed archives to extract
- **`script`**: PowerShell (.ps1) or Bash (.sh) scripts
- **`msi`**: Windows Installer packages
- **`portable`**: Portable applications (no installation)
- **`package-manager`**: System package managers (apt, yum, brew, etc.)

## API Reference

The registry provides REST APIs for programmatic access:

| Endpoint | Description |
|----------|-------------|
| [`/api/catalog.json`](api/catalog.json) | Complete tool listing with metadata |
| [`/api/categories.json`](api/categories.json) | Category-based organization |
| [`/api/stats.json`](api/stats.json) | Registry statistics |

## Repository Structure

```
sunshine-aio-library/
├── tools/              <- Tool entries organized by category
├── schemas/            <- JSON Schema definitions
├── scripts/            <- Python automation scripts
├── api/                <- Generated API files
├── .github/            <- GitHub Actions workflows
└── docs/               <- Documentation
```

## Quality Standards

All tools must meet:
- **Open Source License**: Compatible license (MIT, Apache-2.0, GPL-3.0, etc.)
- **Active Maintenance**: Recent commits within the last year
- **Documentation**: Clear README with installation instructions
- **Accessibility**: Public GitHub repository that is functional

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.