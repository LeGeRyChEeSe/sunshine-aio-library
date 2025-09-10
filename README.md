# Sunshine-AIO-Library

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Validate Tools](https://github.com/sunshine-aio/library/actions/workflows/validate-tools.yml/badge.svg)](https://github.com/sunshine-aio/library/actions/workflows/validate-tools.yml)
[![Tools Count](https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/sunshine-aio/library/main/api/stats.json&query=$.overview.total_tools&label=tools&color=blue)](https://github.com/sunshine-aio/library/blob/main/api/catalog.json)

A curated, community-driven registry of high-quality tools for the Sunshine-AIO ecosystem.

## Related Project

This library is used by the main [Sunshine-AIO](https://github.com/LeGeRyChEeSe/Sunshine-AIO) project, which is a desktop application that allows users to easily install, manage, and configure local streaming tools.

## About

This repository serves as a schema-driven tool registry for the Sunshine-AIO application, enabling users to:

*   Easily discover and install tools for local streaming
*   Manage installations, configurations, and updates of these tools
*   Contribute to the community by proposing new tools

## Features

- **Schema-driven validation** ensures data consistency and quality
- **Automated tool verification** checks repository accessibility and activity
- **Quality scoring system** provides objective tool assessment (0-100 scale)
- **RESTful APIs** for programmatic access
- **Category-based organization** enables efficient tool discovery

## Getting Started

### Prerequisites
- Python 3.11 or higher
- Git for version control

### Installation
```bash
git clone https://github.com/LeGeRyChEeSe/sunshine-aio-library.git
cd sunshine-aio-library
pip install jsonschema requests pyyaml
```

### Quick Start
```bash
# Validate all tools
python scripts/validate.py --verbose

# Generate API catalogs
python scripts/generate-catalog.py --manifest

# Verify tool accessibility
python scripts/verify-tools.py
```

## How to Add a Tool

1. **Fork this repository**
2. **Create tool entry**: Add a JSON file in the appropriate category folder under `tools/`
3. **Validate**: Use `python scripts/validate.py --single your-tool.json`
4. **Submit PR**: Create a pull request with your tool entry
5. **Review**: Wait for community validation and approval

### Tool Entry Format
```json
{
  "name": "example-tool",
  "description": "A powerful example tool for automation",
  "category": "utilities/system-tools",
  "tags": ["automation", "system"],
  "repository": "https://github.com/owner/repo",
  "documentation": "https://owner.github.io/repo",
  "license": "MIT",
  "platforms": ["Windows", "Linux", "macOS"],
  "language": "Python"
}
```

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