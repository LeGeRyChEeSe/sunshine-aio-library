# Tool Submission Template for Sunshine-AIO-Library

This document serves as a template for submitting new tools to the Sunshine-AIO community library. By following this template, you ensure that your tool is compatible with the Sunshine-AIO API and can be easily integrated into the application.

## Structure of the `manifest.json` file

Your submission must include a `manifest.json` file in the root directory of your tool. This file contains all the necessary metadata to describe and manage your tool. Here is the complete structure, with detailed explanations for each field:

```json
{
  "name": "Tool Name",
  "slug": "tool-name",
  "short-description": "Brief description of the tool",
  "long-description": "Detailed description of the tool, its features, and its purpose",
  "author": "Author Name / Organization",
  "website": "https://tool-website.com",
  "repository": "https://github.com/author/tool",
  "tags": ["tag1", "tag2", "tag3"],
  "compatibility": {
    "sunshine": true,
    "apollo": false,
    "platforms": ["windows", "linux", "macos"]
  },
  "installation": {
    "type": "executable",
    "executable": "MyTool.exe",
    "args": ["--silent", "--install"],
    "postInstall": "post-installation-script.ps1",
    "checksum": "sha256:..."
  },
  "uninstallation": {
    "type": "executable",
    "path": "%PROGRAMFILES%\\Tool\\uninstall.exe",
    "args": ["--silent"]
  },
  "configuration": {
    "type": "url",
    "url": "http://localhost:8080/config",
    "file": "config.json"
  },
  "screenshots": [
    "screenshots/screenshot1.png",
    "screenshots/screenshot2.png"
  ],
  "icon": "icon.png"
}
```

## Detailed field explanations

### General Information

* **`name`** (required): Full name of the tool.
* **`slug`** (required): Unique identifier for the tool, lowercase with hyphens as separators.
* **`short-description`** (required): Brief description of the tool.
* **`long-description`** (optional): Detailed description of the tool, its features and purpose.
* **`author`** (required): Name of the tool author or maintaining organization.
* **`website`** (optional): URL of the tool's official website.
* **`repository`** (required): URL of the tool's source code repository.
* **`tags`** (required): List of keywords describing the tool.

### Compatibility

* **`compatibility`** (required):
    * **`sunshine`** (required): `true` if the tool is compatible with Sunshine.
    * **`apollo`** (required): `true` if the tool is compatible with Apollo.
    * **`platforms`** (required): List of supported operating systems.

### Installation

* **`installation`** (required): Supports both single-platform and multi-platform configurations:

**Single Platform Format:**
* **`type`** (required): Installation method type (`"executable"`, `"zip"`, `"script"`, `"msi"`, `"portable"`, `"package-manager"`).
* **`url`** (optional): Direct download URL. Use GitHub latest release format: `https://github.com/user/repo/releases/latest/download/filename.ext`
* **`executable`** (optional): Specific executable or package name (e.g., `Tool.exe`, `Tool.deb`, `Tool.dmg`).
* **`args`** (optional): Command line arguments for installation.
* **`postInstall`** (optional): Relative path to post-installation script.
* **`checksum`** (optional): File checksum for integrity verification.
* **`silent`** (optional): Silent installation (default: `true`).

**Multi-Platform Format:**
```json
"installation": {
  "platforms": {
    "windows": {
      "type": "msi",
      "url": "https://github.com/user/repo/releases/latest/download/Tool-Windows.msi",
      "executable": "Tool.msi",
      "args": ["/quiet"],
      "silent": true
    },
    "linux": {
      "type": "package-manager",
      "url": "https://github.com/user/repo/releases/latest/download/Tool-Linux.deb",
      "executable": "Tool.deb",
      "args": ["--force-yes"],
      "silent": true
    },
    "macos": {
      "type": "portable",
      "url": "https://github.com/user/repo/releases/latest/download/Tool-macOS.dmg",
      "executable": "Tool.dmg",
      "silent": false
    }
  }
}
```

### Uninstallation

* **`uninstallation`** (required):
    * **`type`** (required): Uninstallation method type (`"executable"`, `"script"`, `"registry"`, `"manual"`).
    * **`path`** (optional): Full path to the uninstaller executable or script.
    * **`args`** (optional): Command line arguments for uninstallation.

### Configuration

* **`configuration`** (required):
    * **`type`** (optional): Configuration method type (`""`, `"url"`, `"file"`, `"script"`, `"registry"`, `"none"`).
    * **`url`** (optional): URL of the configuration interface.
    * **`file`** (optional): Configuration file path.
    * **`script`** (optional): Configuration script path.

### Screenshots and Icon

* **`screenshots`** (optional): Array of relative paths to tool interface screenshots.
* **`icon`** (optional): Relative path to the tool icon.

## Tool Directory Structure

Your tool directory structure should be as follows:

```
tool-name/
├── manifest.json
├── icon.png (optional)
├── screenshots/ (optional)
│   ├── screenshot1.png
│   └── screenshot2.png
└── README.md (optional)
```

## Validation

Before submitting your tool, ensure your `manifest.json` file is valid by using a JSON schema validator. The JSON schema for `manifest.json` is available in the `schemas` folder of the `sunshine-aio-library` repository.

## Submission

To submit your tool, create a pull request on the `sunshine-aio-library` GitHub repository. Your submission will be reviewed by moderators before being accepted.