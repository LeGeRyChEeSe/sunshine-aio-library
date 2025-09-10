<<<<<<< HEAD
# Sunshine-AIO-Library

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Welcome to the community tool library for Sunshine-AIO! This repository aims to centralize and facilitate access to a variety of complementary tools to enhance your local streaming experience with Sunshine and Apollo.

## Related Project

This library is used by the main [Sunshine-AIO](https://github.com/LeGeRyChEeSe/Sunshine-AIO) project, which is a desktop application that allows users to easily install, manage, and configure local streaming tools.

## Objective

This repository serves as a database for an application (Sunshine-AIO) that will allow users to:

*   Easily discover and install tools for local streaming.
*   Manage installations, configurations, and updates of these tools.
*   Contribute to the community by proposing new tools.

## How to add a tool?

We encourage the community to contribute by adding new tools to the library. To submit a tool, follow these simple steps:

1.  **Fork this repository**: Click the "Fork" button at the top right of this page to create your own copy of the repository.

2.  **Create a folder for your tool**: In the `tools/` folder, create a new folder with your tool's name in lowercase and with hyphens as separators (e.g., `tool-name`).

3.  **Add your tool's files**:
    *   A `manifest.json` file (required): This file contains all the information about your tool. Use the [`templates/TEMPLATE.md`](templates/TEMPLATE.md) file as a template and fill in all the required fields.
    *   An `icon.png` icon (required): An image representing your tool (PNG format, recommended size: 256x256 pixels).
    *   A `screenshots/` folder (optional): Add screenshots to illustrate your tool.
    *   A `README.md` file (optional, but recommended): Provide additional information about your tool, such as specific usage instructions.

4.  **Validate your `manifest.json` file**: Make sure your file is valid against the JSON schema available in `templates/manifest-schema.json`. You can use an online validator (e.g., [https://www.jsonschemavalidator.net/](https://www.jsonschemavalidator.net/)).

5.  **Create a pull request**: Once you have added your tool and validated the `manifest.json` file, create a pull request to the main branch of this repository.

6.  **Wait for validation**: Your submission will be reviewed by moderators. They will verify that your tool complies with the library's rules and that it works correctly. You may be asked to make changes to your submission.

7.  **Your tool is added!**: Once your pull request is accepted, your tool will be added to the library and will be accessible to all Sunshine-AIO users.

## Contribution Rules

*   Ensure that your tool is relevant to the Sunshine/Apollo ecosystem.
*   Provide complete and accurate information in the `manifest.json` file.
*   Do not include malicious code or inappropriate content.
*   Respect the copyrights and licenses of the software you use.
*   Be respectful towards other contributors and moderators.

## Repository Structure

```
sunshine-aio-library/
├── tools/              <- Folder containing all tools
│   ├── tool1/          <- Folder for a specific tool
│   │   ├── manifest.json   <- Metadata file (required)
│   │   ├── icon.png        <- Tool icon (required)
│   │   ├── screenshots/    <- Screenshots (optional)
│   │   │   ├── screenshot1.png
│   │   │   └── screenshot2.png
│   │   └── README.md       <- Tool-specific README (optional)
│   ├── tool2/
│   │   └── ...
│   └── ...
├── templates/          <- Folder containing templates
│   ├── manifest-schema.json <- JSON schema for manifest.json
│   └── TEMPLATE.md     <- Template for submitting a tool
└── README.md           <- This file
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
=======
# Sunshine-AIO Community Tools Registry

A curated, community-driven registry of high-quality tools for the Sunshine-AIO ecosystem.

[![Validate Tools](https://github.com/sunshine-aio/library/actions/workflows/validate-tools.yml/badge.svg)](https://github.com/sunshine-aio/library/actions/workflows/validate-tools.yml)
[![Tools Count](https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/sunshine-aio/library/main/api/stats.json&query=$.overview.total_tools&label=tools&color=blue)](https://github.com/sunshine-aio/library/blob/main/api/catalog.json)
[![Verified Tools](https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/sunshine-aio/library/main/api/stats.json&query=$.overview.verified_tools&label=verified&color=green)](https://github.com/sunshine-aio/library/blob/main/api/catalog.json)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [Development](#development)
- [License](#license)
- [Contact](#contact)

## About the Project

The Sunshine-AIO Community Tools Registry serves as a comprehensive, community-maintained catalog of tools specifically curated for the Sunshine-AIO project ecosystem. This registry implements a modern, schema-driven approach to tool discovery and validation, providing both human-readable documentation and machine-readable APIs.

### Problem Statement

Finding reliable, well-maintained tools for development workflows can be challenging. Developers often struggle with:
- Discovering tools that integrate well with their existing stack
- Verifying tool quality and maintenance status
- Understanding which tools are actively supported by the community

### Solution

This registry addresses these challenges by providing:
- **Structured Discovery**: Categorized tool listings with comprehensive metadata
- **Quality Assurance**: Automated validation and scoring system
- **API Integration**: RESTful APIs for programmatic access
- **Community Validation**: Peer review and collaborative maintenance

### Built With

- **Python 3.11+** - Core validation and catalog generation
- **JSON Schema** - Data validation and consistency
- **GitHub Actions** - Automated CI/CD pipelines
- **RESTful APIs** - Generated JSON catalogs

## Features

### Core Functionality
- **Schema-driven validation** ensures data consistency and quality
- **Automated tool verification** checks repository accessibility and activity
- **Quality scoring system** provides objective tool assessment (0-100 scale)
- **Multi-format APIs** support various integration patterns
- **Category-based organization** enables efficient tool discovery

### Quality Assurance
- Automated URL accessibility testing
- GitHub repository validation and metrics collection
- License compliance verification
- Documentation quality assessment
- Community review workflows

### Developer Experience
- Comprehensive JSON schemas for tool entries
- CLI tools for validation and testing
- GitHub templates for consistent contributions
- Detailed documentation and examples

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Git for version control
- Internet connection for tool verification

### Installation

1. Clone the repository
```bash
git clone https://github.com/sunshine-aio/library.git
cd library
```

2. Install Python dependencies
```bash
pip install jsonschema requests pyyaml
```

3. Verify installation
```bash
python3 scripts/validate.py --help
```

### Quick Start

Validate all tools in the registry:
```bash
python3 scripts/validate.py --verbose
```

Generate API catalogs:
```bash
python3 scripts/generate-catalog.py --manifest
```

Verify tool accessibility:
```bash
python3 scripts/verify-tools.py
```

## Usage

### For Tool Users

**Browse Tools by Category**
- [Automation Tools](tools/automation/) - Build tools, deployment, CI/CD
- [Testing Tools](tools/testing/) - Unit testing, integration testing, performance
- [Utilities](tools/utilities/) - File management, system tools, network utilities
- [Development Tools](tools/development/) - Debugging, profiling tools
- [Security Tools](tools/security/) - Security scanning and analysis tools

**Search Tools Programmatically**
```bash
# Get all tools
curl https://raw.githubusercontent.com/sunshine-aio/library/main/api/catalog.json

# Browse by category
curl https://raw.githubusercontent.com/sunshine-aio/library/main/api/categories.json

# Get registry statistics
curl https://raw.githubusercontent.com/sunshine-aio/library/main/api/stats.json
```

### For Contributors

**Submit a New Tool**
1. Search existing tools to avoid duplicates
2. Open a [tool request issue](.github/ISSUE_TEMPLATE/tool-request.yml)
3. Follow the guided template to provide tool information
4. Wait for community review and approval
5. Submit a pull request with the tool entry

**Tool Entry Format**
```json
{
  "name": "example-tool",
  "description": "A powerful example tool for automation",
  "category": "automation/build-tools",
  "tags": ["automation", "build", "docker"],
  "repository": "https://github.com/owner/repo",
  "documentation": "https://owner.github.io/repo",
  "license": "MIT",
  "platforms": ["Linux", "macOS", "Windows"],
  "language": "Python",
  "maintainer": {
    "name": "Tool Maintainer",
    "github": "maintainer-username"
  }
}
```

## API Reference

The registry provides several REST APIs for programmatic access:

### Available Endpoints

| Endpoint | Description | Update Frequency |
|----------|-------------|------------------|
| [`/api/catalog.json`](api/catalog.json) | Complete tool listing with metadata | On every push |
| [`/api/categories.json`](api/categories.json) | Category-based organization with statistics | On every push |
| [`/api/search.json`](api/search.json) | Search indexes and filters | On every push |
| [`/api/stats.json`](api/stats.json) | Comprehensive registry analytics | On every push |
| [`/api/manifest.json`](api/manifest.json) | API metadata and usage information | On every push |

### Example Usage

**JavaScript/Node.js**
```javascript
// Fetch all tools
const response = await fetch('https://raw.githubusercontent.com/sunshine-aio/library/main/api/catalog.json');
const catalog = await response.json();
console.log(`Found ${catalog.total_tools} tools`);
```

**Python**
```python
import requests

# Get verified tools
response = requests.get('https://raw.githubusercontent.com/sunshine-aio/library/main/api/catalog.json')
catalog = response.json()
verified_tools = [tool for tool in catalog['tools'] if tool['verification']['status'] == 'verified']
```

**Shell/Bash**
```bash
# Count tools by category
curl -s https://raw.githubusercontent.com/sunshine-aio/library/main/api/categories.json | \
  jq -r '.categories | to_entries[] | "\(.key): \(.value.stats.total)"'
```

For detailed API documentation, see the [API Reference Guide](docs/API.md).

## Contributing

We welcome community contributions to improve the registry. Please review our guidelines before contributing.

### How to Contribute

**Report New Tools**
1. Search existing tools to avoid duplicates
2. Open a [tool request issue](.github/ISSUE_TEMPLATE/tool-request.yml)
3. Provide complete tool information using the guided template
4. Wait for community review and maintainer approval

**Submit Pull Requests**
1. Fork the repository
2. Create a feature branch
3. Add your tool entry following our schema
4. Test your changes locally
5. Submit a pull request with detailed description

**Report Issues**
Use our [bug report template](.github/ISSUE_TEMPLATE/bug-report.yml) to report:
- Tool validation errors
- API or catalog issues
- Documentation problems
- Registry functionality bugs

### Quality Standards

All tools must meet these requirements:

- **Open Source License**: Compatible license (MIT, Apache-2.0, GPL-3.0, etc.)
- **Active Maintenance**: Recent commits within the last year
- **Documentation**: Clear README with installation and usage instructions
- **Accessibility**: Public GitHub repository that is functional
- **Categorization**: Appropriate category classification
- **Uniqueness**: No duplicate entries in the registry

### Tool Validation Process

1. **Schema Validation**: JSON structure and required fields
2. **URL Verification**: Repository and documentation accessibility
3. **Quality Scoring**: Automated assessment (0-100 scale)
4. **Community Review**: Peer evaluation and feedback
5. **Automated Testing**: Continuous integration checks

For detailed contribution guidelines, see the [Contributing Guide](docs/CONTRIBUTING.md).

## Development

### Local Development Environment

**System Requirements**
- Python 3.11 or higher
- Git version control
- Internet connection for tool verification

**Setup Instructions**
```bash
# Clone and enter the repository
git clone https://github.com/sunshine-aio/library.git
cd library

# Install required Python packages
pip install jsonschema requests pyyaml

# Verify installation
python3 scripts/validate.py --help
```

### Available CLI Commands

**Validation Commands**
```bash
# Validate all tools in registry
python3 scripts/validate.py --verbose

# Validate specific tool entry
python3 scripts/validate.py --single tools/category/tool.json

# Generate comprehensive validation report
python3 scripts/validate.py > validation-report.txt
```

**Tool Verification Commands**
```bash
# Verify tool accessibility and metrics
python3 scripts/verify-tools.py

# Verify with custom settings
python3 scripts/verify-tools.py --workers 10 --timeout 20

# Update tool files with verification results
python3 scripts/verify-tools.py --update
```

**Catalog Generation Commands**
```bash
# Generate all API catalogs
python3 scripts/generate-catalog.py --manifest

# Generate with custom directories
python3 scripts/generate-catalog.py --tools-dir ./tools --api-dir ./output
```

### Architecture Overview

The registry implements a modern, automated approach to tool curation:

**Core Components**
- **JSON Schema Validation**: Ensures consistent data structure and quality
- **Automated Verification**: Validates repository accessibility and tool metrics
- **Quality Scoring**: Objective assessment system (0-100 scale) based on multiple factors
- **API Generation**: Creates multiple JSON endpoints for different use cases
- **CI/CD Integration**: GitHub Actions automate validation and catalog updates

**Data Flow**
1. Tool entries are submitted via issues or pull requests
2. Automated validation checks schema compliance and URL accessibility
3. Quality scoring evaluates repository health and community metrics
4. Approved tools are merged and catalogs are regenerated
5. APIs are automatically updated and deployed

**Quality Assurance Pipeline**
- Schema validation against JSON Schema specifications
- URL accessibility testing with timeout handling
- GitHub API integration for repository metrics
- License compliance verification
- Community review and approval process

### Testing

**Unit Tests**
```bash
# Run all tests (when available)
python3 -m pytest tests/

# Test specific components
python3 -m pytest tests/test_validation.py
```

**Integration Testing**
```bash
# Test complete workflow
python3 scripts/validate.py --verbose
python3 scripts/verify-tools.py --workers 3
python3 scripts/generate-catalog.py --manifest
```

## Roadmap

**Current Status**: Production Ready ✅
- Full JSON Schema validation system
- Automated tool verification and scoring
- Comprehensive API generation
- Complete documentation suite
- GitHub Actions CI/CD pipeline

**Planned Enhancements**
- [ ] Advanced search capabilities with fuzzy matching
- [ ] Tool usage analytics and popularity metrics
- [ ] Integration with package managers (npm, PyPI, etc.)
- [ ] Automated dependency analysis
- [ ] Community rating and review system
- [ ] Web interface for registry browsing

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Individual Tool Licenses**: Each tool listed in this registry maintains its own license. Please refer to the respective tool repositories for specific licensing information.

## Contact

**Project Maintainers**
- Create an issue for bug reports or feature requests
- Submit pull requests for tool additions or improvements
- Join discussions for community feedback and suggestions

**Community Channels**
- [GitHub Issues](https://github.com/sunshine-aio/library/issues) - Bug reports and feature requests
- [GitHub Discussions](https://github.com/sunshine-aio/library/discussions) - Community conversations
- [Pull Requests](https://github.com/sunshine-aio/library/pulls) - Code contributions

**Repository Statistics**
- Maintained by the Sunshine-AIO community
- Automated updates via GitHub Actions
- Quality-focused curation process
- Open source and community-driven

---

<div align="center">

**Built with precision for the Sunshine-AIO ecosystem**

*This registry is automatically maintained and updated. For the latest statistics and tool information, visit the generated [API endpoints](api/).*

</div>
>>>>>>> clean-branch
