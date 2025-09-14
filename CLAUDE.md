# Claude Code Configuration

## Prerequisites & Setup

### Virtual Environment Setup
Always use a virtual environment before running Python commands:

```bash
# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    python -m venv venv
fi

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install jsonschema requests pyyaml
```

### PowerShell Setup (Windows)
```powershell
# Check if virtual environment exists, create if not
if (-not (Test-Path "venv")) {
    python -m venv venv
}

# Activate virtual environment
venv\Scripts\Activate.ps1

# Install dependencies
pip install jsonschema requests pyyaml
```

## Project Commands

**Note**: All commands assume the virtual environment is activated. Use the setup commands above first.

### Development
- `python scripts/validate.py` - Validate all tool entries against JSON schema with regex pattern validation and autocompletion
- `python scripts/validate.py --no-autocomplete` - Validate without autocompletion for legacy manifests
- `python scripts/verify-tools.py` - Verify tool accessibility and functionality
- `python scripts/generate-catalog.py` - Generate API catalog from tool entries
- `python scripts/generate-catalog.py --manifest` - Generate manifest with API catalogs

### Testing
- `python scripts/validate.py --single tools/category/tool.json` - Validate single tool entry with pattern checks
- `python scripts/validate.py --verbose` - Validate with detailed output including pattern validation errors
- `python scripts/validate.py --dry-run` - Preview autocompletion changes without applying

### Schema Validation
- `python scripts/validate.py --dry-run` - Show what would be autocompleted without saving changes

### Environment Verification
Before running any script, you can check if dependencies are available:
```bash
python -c "import jsonschema, requests; print('Dependencies OK')"
```

## Project Structure

This repository follows a schema-driven approach for managing community tools:

- `/schemas/` - JSON Schema definitions for validation (tool-entry.json, category.json, validation-rules.json)
- `/tools/` - Tool entries organized by category
- `/scripts/` - Python automation scripts (validate.py, verify-tools.py, generate-catalog.py)
- `/api/` - Generated API files for programmatic access (catalog.json, categories.json, manifest.json, search.json, stats.json)
- `/.github/` - GitHub Actions workflows and templates
- `/docs/` - Documentation (API.md, CONTRIBUTING.md, SCHEMA.md)
- `/templates/` - Template files for tool entries

## Key Features

### Pattern Validation System
The schema enforces strict regex patterns for data consistency:
- **Name**: `^[a-zA-Z0-9\s\-_]+$` (2-50 characters)
- **Slug**: `^[a-z0-9-]+$` (2-50 characters, unique identifier)
- **Repository**: `^https://github\.com/[^/]+/[^/]+/?$` (GitHub URLs only)
- **Tags**: `^[a-z0-9-]+$` per tag (max 8 tags, 20 chars each)
- **Checksum**: `^(|sha256:[a-fA-F0-9]+|md5:[a-fA-F0-9]+|sha1:[a-fA-F0-9]+)$`

### Autocompletion System
The validation script includes intelligent autocompletion for legacy manifests:
- Automatically completes missing required fields for new schema format
- Fetches repository metrics to populate missing data
- Supports dry-run mode to preview changes before applying
- Can be disabled with `--no-autocomplete` flag
- Validates all patterns before and after autocompletion

### Schema Evolution
- **Legacy format**: Basic tool information (name, description, category, license)
- **New format**: Extended with installation, uninstallation, configuration support
- **Installation types**: executable, zip, script, msi, portable, package-manager
- **Platform compatibility**: Windows, Linux, macOS with streaming host support

## Quality Standards

- All tool entries must pass JSON schema validation with regex pattern checks
- Repository links must be accessible and functional
- Tools are automatically scored based on activity and quality metrics (0-100 scale)
- Community verification through GitHub Issues and PRs
- Automated verification with repository metrics collection