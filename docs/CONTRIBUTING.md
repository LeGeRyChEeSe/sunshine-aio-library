# 🤝 Contributing to Sunshine-AIO Community Tools Registry

Thank you for your interest in contributing to the Sunshine-AIO Community Tools Registry! This document provides comprehensive guidelines for adding tools, reporting issues, and improving the registry.

## 🎯 How to Contribute

### 🔧 Adding a New Tool

The most common contribution is adding a new tool to the registry. Here's the complete process:

#### Step 1: Check for Duplicates
Before submitting a new tool, search the existing registry to ensure it's not already included:
- Browse [categories](../tools/) manually
- Search the [API catalog](../api/catalog.json)
- Use GitHub's search functionality

#### Step 2: Verify Tool Requirements
Ensure your tool meets our quality standards:

**Required Criteria:**
- ✅ Open source with compatible license
- ✅ GitHub repository that's publicly accessible
- ✅ Active maintenance (commits within last year)
- ✅ Clear documentation (README with installation/usage)
- ✅ Fits within our category structure

**Quality Indicators:**
- ⭐ At least 10 GitHub stars (or exceptional utility for niche tools)
- 🧪 Evidence of testing (CI/CD, test files)
- 👥 Active community or responsive maintainer
- 📚 Comprehensive documentation

#### Step 3: Choose Contribution Method

**Option A: Issue Request (Recommended)**
1. Open a [tool request issue](../.github/ISSUE_TEMPLATE/tool-request.yml)
2. Fill out the complete template
3. Wait for maintainer approval
4. Create a pull request (or maintainer will create one)

**Option B: Direct Pull Request**
1. Fork the repository
2. Create a new tool entry JSON file
3. Submit a pull request
4. Respond to review feedback

### 📝 Tool Entry Format

Tools are defined using JSON files following our [schema](../schemas/tool-entry.json).

#### File Location
Place your tool file in the appropriate category directory:
```
tools/
├── automation/
│   ├── build-tools/
│   │   └── your-tool.json
│   └── deployment/
├── testing/
│   └── unit-testing/
└── utilities/
    └── file-management/
```

#### Tool Entry Template
```json
{
  "name": "your-tool-name",
  "description": "Brief description of what the tool does (10-150 chars)",
  "category": "automation/build-tools",
  "subcategory": "docker-tools",
  "tags": ["automation", "docker", "build"],
  "repository": "https://github.com/username/repository",
  "documentation": "https://username.github.io/repository",
  "license": "MIT",
  "platforms": ["Linux", "macOS", "Windows"],
  "language": "Python",
  "maintainer": {
    "name": "Your Name",
    "github": "yourusername",
    "contact": "you@example.com"
  },
  "added_date": "2024-01-15",
  "contributed_by": "yourgithubusername"
}
```

#### Field Guidelines

**Required Fields:**
- `name`: Tool name (alphanumeric, hyphens, underscores only)
- `description`: Clear, concise description (10-150 characters)
- `category`: One of the predefined categories (see [categories](../schemas/category.json))
- `repository`: GitHub repository URL
- `license`: Open source license from approved list

**Optional but Recommended:**
- `subcategory`: More specific classification
- `tags`: Search tags (lowercase, hyphens only, max 8 tags)
- `documentation`: Link to documentation
- `platforms`: Supported operating systems
- `language`: Primary programming language
- `maintainer`: Tool maintainer information

**Auto-Generated (Do Not Include):**
- `metrics`: GitHub stats (stars, forks, etc.)
- `verification`: Quality verification status

### 🏷️ Categories and Tags

#### Available Categories
```
automation/build-tools      - Build and compilation tools
automation/deployment       - Deployment and infrastructure tools  
automation/ci-cd           - CI/CD and pipeline tools
testing/unit-testing       - Unit testing frameworks and tools
testing/integration-testing - Integration testing tools
testing/performance        - Performance and load testing
utilities/file-management  - File and directory utilities
utilities/system-tools     - System administration tools
utilities/network          - Network analysis and tools
development/debugging      - Debugging and troubleshooting tools
development/profiling      - Performance profiling tools
security/scanning          - Security analysis and scanning
```

#### Tag Best Practices
- Use lowercase with hyphens
- Be specific but not redundant with category
- Include technology stack (e.g., "docker", "kubernetes")
- Include use cases (e.g., "monitoring", "backup")
- Maximum 8 tags per tool

### 📋 Pull Request Process

#### Creating a Pull Request

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/library.git
   cd library
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b add-tool-name
   ```

3. **Add Tool Entry**
   ```bash
   # Create the JSON file in appropriate category
   mkdir -p tools/category/subcategory
   # Edit your tool file
   nano tools/category/subcategory/your-tool.json
   ```

4. **Validate Locally**
   ```bash
   # Install dependencies
   pip install jsonschema requests pyyaml
   
   # Validate your tool
   python scripts/validate.py --single tools/category/subcategory/your-tool.json
   
   # Verify accessibility
   python scripts/verify-tools.py --single tools/category/subcategory/your-tool.json
   ```

5. **Commit and Push**
   ```bash
   git add tools/category/subcategory/your-tool.json
   git commit -m "Add [tool-name] to [category]
   
   - Brief description of what the tool does
   - Key features and use cases
   - License: [LICENSE-NAME]
   
   🤖 Generated with Claude Code
   
   Co-Authored-By: Claude <noreply@anthropic.com>"
   
   git push origin add-tool-name
   ```

6. **Submit Pull Request**
   Use our [pull request template](../.github/pull_request_template.md) and fill out all sections.

#### Review Process

1. **Automated Checks**
   - Schema validation
   - URL accessibility testing
   - Duplicate detection
   - Quality scoring

2. **Maintainer Review**
   - Tool relevance to ecosystem
   - Quality and maintenance status
   - Documentation completeness
   - Category appropriateness

3. **Community Feedback**
   - Other contributors may provide feedback
   - Address any requested changes
   - Discussion may occur in PR comments

4. **Approval and Merge**
   - Once approved, maintainer will merge
   - API catalogs will be automatically updated
   - Tool becomes available in registry

### 🐛 Reporting Issues

#### Bug Reports
Use our [bug report template](../.github/ISSUE_TEMPLATE/bug-report.yml) for:
- Tool validation errors
- API catalog issues  
- Documentation problems
- Search functionality issues

#### Other Contributions

**Documentation Improvements**
- Fix typos or unclear instructions
- Add examples or use cases
- Improve schema documentation
- Update API documentation

**Infrastructure Improvements**
- Enhance validation scripts
- Improve GitHub Actions workflows
- Add new quality checks
- Optimize catalog generation

**Schema Updates**
- Propose new categories or fields
- Suggest validation improvements
- Request new license options

## 🔍 Quality Standards

### Tool Requirements

**Minimum Standards:**
- GitHub repository with clear README
- Open source license
- Recent activity (commits within 365 days)
- Functional installation/usage instructions
- No malware or security risks

**Quality Indicators:**
- GitHub stars (typically 10+ for automatic verification)
- Active issues/PR handling
- Comprehensive documentation
- Test coverage
- CI/CD integration
- Community engagement

### Scoring System

Tools are automatically scored (0-100) based on:
- **Activity (25%)**: Recent commits and maintenance
- **Popularity (30%)**: Stars and community engagement  
- **Documentation (15%)**: README quality and external docs
- **License (10%)**: Compatible open source license
- **Community (20%)**: Contributors and issue handling

### Verification Levels

- **✅ Verified**: Score 80+ with comprehensive validation
- **⚠️ Conditional**: Score 60-79 with minor issues
- **🔍 Needs Review**: Score below 60 requiring manual review
- **❌ Failed**: Inaccessible or non-functional

## 🛠️ Development Setup

### Local Environment

```bash
# Clone repository
git clone https://github.com/sunshine-aio/library.git
cd library

# Install dependencies
pip install -r requirements.txt
# OR manually:
pip install jsonschema requests pyyaml pytest

# Set up pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

### Useful Scripts

```bash
# Validate all tools
python scripts/validate.py --verbose

# Validate specific tool
python scripts/validate.py --single tools/path/to/tool.json

# Verify tool accessibility
python scripts/verify-tools.py

# Generate API catalogs
python scripts/generate-catalog.py --manifest

# Update tool verification status
python scripts/verify-tools.py --update
```

### Testing Changes

```bash
# Run validation tests
python -m pytest tests/

# Test specific tool entry
python scripts/validate.py --single your-tool.json

# Check catalog generation
python scripts/generate-catalog.py
ls -la api/
```

## 📋 Review Checklist

Before submitting, ensure:

**Tool Quality:**
- [ ] Repository is publicly accessible
- [ ] README exists with clear installation/usage
- [ ] License is open source and compatible
- [ ] Recent activity (commits within year)
- [ ] No duplicate in existing registry

**Entry Format:**
- [ ] JSON syntax is valid
- [ ] All required fields present
- [ ] Category matches predefined options
- [ ] Repository URL format is correct
- [ ] Description is clear and appropriate length

**Testing:**
- [ ] Local validation passes
- [ ] Tool accessibility verified
- [ ] No validation errors or warnings
- [ ] Generated catalogs look correct

## 🤔 FAQ

**Q: How long does review take?**
A: Typically 2-7 days depending on complexity and maintainer availability.

**Q: Can I add proprietary tools?**
A: No, we only accept open source tools with compatible licenses.

**Q: What if my tool has few stars?**
A: We consider utility and quality over popularity. Provide compelling justification for tools with low star counts.

**Q: How do I update tool information?**
A: Submit a PR with changes to the existing tool file. Include justification for updates.

**Q: Can I add tools I don't maintain?**
A: Yes, as long as they meet quality standards and you provide accurate information.

**Q: How are API catalogs updated?**
A: Automatically via GitHub Actions when changes are merged to main branch.

## 📞 Getting Help

- **General Questions**: Open a [discussion](https://github.com/sunshine-aio/library/discussions)
- **Bug Reports**: Use our [issue template](../.github/ISSUE_TEMPLATE/bug-report.yml)  
- **Tool Requests**: Use our [tool request template](../.github/ISSUE_TEMPLATE/tool-request.yml)
- **Direct Contact**: Mention maintainers in issues or PRs

## 🙏 Recognition

Contributors are recognized through:
- GitHub contributor statistics
- Attribution in tool entries (`contributed_by` field)
- Acknowledgment in release notes
- Community discussions and feedback

Thank you for helping build the best tool registry for the Sunshine-AIO ecosystem! 🚀