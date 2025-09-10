# Claude Code Configuration

## Project Commands

### Development
- `python scripts/validate.py` - Validate all tool entries against JSON schema
- `python scripts/verify-tools.py` - Verify tool accessibility and functionality
- `python scripts/generate-catalog.py` - Generate API catalog from tool entries
- `python scripts/update-readme.py` - Update README with latest tool statistics

### Testing
- `python -m pytest tests/` - Run all tests
- `python scripts/validate.py --single tools/category/tool.json` - Validate single tool entry

### Maintenance
- `python scripts/cleanup.py` - Clean up broken or deprecated tools
- `python scripts/stats.py` - Generate registry statistics

## Project Structure

This repository follows a schema-driven approach for managing community tools:

- `/schemas/` - JSON Schema definitions for validation
- `/tools/` - Tool entries organized by category
- `/scripts/` - Python automation scripts
- `/api/` - Generated API files for programmatic access
- `/.github/` - GitHub Actions workflows and templates

## Quality Standards

- All tool entries must pass JSON schema validation
- Repository links must be accessible
- Tools are automatically scored based on activity and quality metrics
- Community verification through GitHub Issues and PRs