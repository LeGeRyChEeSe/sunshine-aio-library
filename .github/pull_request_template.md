# 🔧 Tool Addition/Update Request

## 📋 Summary
<!-- Brief description of the changes in this PR -->

## 📊 Changes Made
<!-- Check all that apply -->
- [ ] 🆕 New tool addition
- [ ] 📝 Tool information update  
- [ ] 🔧 Tool metadata correction
- [ ] 🗂️ Category or classification change
- [ ] 📚 Documentation update
- [ ] 🐛 Bug fix
- [ ] 🔨 Infrastructure/script update

## 🛠️ Tool Details
<!-- Fill out for new tools or significant updates -->

**Tool Name:** `tool-name`
**Slug:** `tool-slug` (lowercase, hyphens only, 2-50 chars)
**Format:** [ ] Legacy (description, category, license) [ ] New (short-description, compatibility, installation)
**Category/Subcategory:** `streaming/hosts` or `category/subcategory`
**Repository:** https://github.com/owner/repo
**License:** `LICENSE-NAME` (for legacy format)

**Key Features:**
<!-- List 3-5 main features or use cases -->
- Feature 1
- Feature 2
- Feature 3

## ✅ Validation Checklist
<!-- These will be automatically checked by CI, but please verify manually -->

### Required Checks
- [ ] 🔍 JSON schema validation passes with regex pattern validation
- [ ] 🆔 Unique slug assigned and follows pattern: `^[a-z0-9-]+$` (2-50 chars)
- [ ] 📛 Name follows pattern: `^[a-zA-Z0-9\s\-_]+$` (2-50 chars)
- [ ] 🌐 Repository URL follows GitHub pattern: `^https://github\.com/[^/]+/[^/]+/?$`
- [ ] 📚 Documentation exists and is accessible
- [ ] 🏷️ Appropriate category from streaming-focused enum (for legacy format)
- [ ] 📜 Compatible open source license from enum (for legacy format)
- [ ] 🎯 No duplicate entries (slug and repository)
- [ ] 🖥️ Streaming host compatibility (sunshine/apollo) properly set as boolean
- [ ] 📦 Installation/uninstallation/configuration methods defined with proper types
- [ ] 🏷️ Tags follow pattern `^[a-z0-9-]+$` (max 8 tags, 20 chars each)
- [ ] 🔐 Checksum follows pattern (empty string or hash format allowed)

### Quality Checks
- [ ] ⭐ Repository has at least 10 stars (or exceptional utility)
- [ ] 📅 Recent activity (commits within last year)
- [ ] 📖 Clear README with installation/usage instructions
- [ ] 🧪 Evidence of testing or CI/CD
- [ ] 👥 Active community or maintainer engagement

### Metadata Completeness
- [ ] 📝 Description format correct:
  - Legacy: `description` field (10-150 chars)
  - New: `short-description` field (10-100 chars) with hyphens allowed
- [ ] 📖 Long description added if needed (max 500 chars)
- [ ] 🏷️ Relevant tags added for searchability (lowercase, hyphens, max 8)
- [ ] 💻 Platform compatibility specified:
  - Legacy: `platforms` array (Windows, Linux, macOS, Web, Cross-platform)
  - New: `compatibility.platforms` array (windows, linux, macos, web - lowercase)
- [ ] 🔧 Primary language from enum (optional)
- [ ] 👤 Author information:
  - Legacy: `maintainer` object (name, github, contact)
  - New: `author` string (max 100 chars)
- [ ] 🎮 Streaming host compatibility boolean values (sunshine/apollo)
- [ ] 🛠️ Installation types from enum: executable, zip, script, msi, portable, package-manager
- [ ] 🗑️ Uninstallation type from enum: executable, script, registry, manual
- [ ] ⚙️ Configuration type from enum: "", url, file, script, registry, none

## 🧪 Testing
<!-- How did you test these changes? -->

- [ ] Ran `python scripts/validate.py --single tools/path/to/tool.json` (with regex pattern validation and autocompletion)
- [ ] Checked autocompletion preview with `python scripts/validate.py --single tools/path/to/tool.json --dry-run`
- [ ] Used `python scripts/validate.py --verbose` for detailed pattern validation errors
- [ ] Ran `python scripts/verify-tools.py --single tools/path/to/tool.json`
- [ ] Tested tool installation/usage locally
- [ ] Verified all URLs are accessible
- [ ] Confirmed virtual environment setup (see CLAUDE.md prerequisites)

## 📸 Screenshots/Evidence
<!-- If applicable, add screenshots or evidence of tool functionality -->

## 🔗 Related Issues
<!-- Link any related issues -->
Closes #issue-number
Related to #issue-number

## 📋 Review Notes
<!-- Any specific areas you'd like reviewers to focus on -->

## ⚠️ Breaking Changes
<!-- List any breaking changes if applicable -->
- [ ] No breaking changes
- [ ] Breaking changes (describe below):

## 📚 Additional Context
<!-- Any other context about the PR that reviewers should know -->

---

### 🤖 Automated Checks
<!-- This section will be updated by GitHub Actions -->
The following checks will run automatically:
- ✅ Schema validation with regex pattern enforcement
- ✅ Autocompletion for missing fields (legacy format migration)
- ✅ URL accessibility testing
- ✅ Duplicate detection (slug and repository)
- ✅ Quality scoring (0-100 scale)
- ✅ Repository metrics collection (stars, forks, last commit)
- ✅ Catalog generation (API files update)

**Note:** Please ensure all automated checks pass before requesting review. If checks fail, review the error logs and update your submission accordingly.

---

**By submitting this PR, I confirm that:**
- [ ] I have read and followed the contributing guidelines
- [ ] The tool is open source and compatible with our registry (for legacy format)
- [ ] I have the right to submit this tool for inclusion
- [ ] All information provided is accurate to the best of my knowledge
- [ ] I have provided complete streaming host compatibility information (boolean values)
- [ ] Installation, uninstallation, and configuration methods follow schema enums and are appropriate
- [ ] All regex patterns are followed (name, slug, repository, tags, checksum)
- [ ] Tool entry format (legacy vs new) is consistent throughout the submission