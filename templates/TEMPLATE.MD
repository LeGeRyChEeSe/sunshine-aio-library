# Tool Submission Template for Sunshine-AIO-Library

This document serves as a template for submitting new tools to the Sunshine-AIO community library. By following this template, you ensure that your tool is compatible with the Sunshine-AIO API and can be easily integrated into the application.

## Structure of the `manifest.json` file

Your submission must include a `manifest.json` file in the root directory of your tool. This file contains all the necessary metadata to describe and manage your tool. Here is the complete structure, with detailed explanations for each field:

```json
{
  "name": "Tool Name",
  "slug": "tool-name",
  "description": "Detailed description of the tool, its features, and its purpose.",
  "version": "1.0.0",
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
    "url": "https://download-link.com/tool.exe",
    "linuxUrl": "",
    "macOSUrl": "",
    "args": ["--silent", "--install"],
    "linuxArgs": [],
    "macOSArgs": [],
    "postInstall": "post-installation-script.ps1",
    "checksum": "sha256:...",
    "versionDetection": {
      "method": "file",
      "file": "%PROGRAMFILES%\\Tool\\version.txt",
      "regex": "(\\d+\\.\\d+\\.\\d+)"
    }
  },
  "uninstallation": {
    "type": "executable",
    "path": "%PROGRAMFILES%\\Tool\\uninstall.exe",
    "args": ["--silent"],
    "linuxPath": "",
    "linuxArgs": [],
    "macOSPath": "",
    "macOSArgs": []
  },
  "configuration": {
    "type": "url",
    "url": "http://localhost:8080/config",
    "file": "",
    "format": "",
    "registryPath": "",
    "registryKey": ""
  },
  "updates": {
    "checkUrl": "https://api.github.com/repos/author/tool/releases/latest",
    "versionRegex": "v(\\d+\\.\\d+\\.\\d+)",
    "changelogUrl": ""
  },
  "rating": {
    "average": 4.5,
    "count": 120
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

*   **`name`** (required): The full name of the tool. Be descriptive and clear.
*   **`slug`** (required): A unique identifier for the tool, in lowercase, with hyphens as separators (e.g., `tool-name`). This identifier is used in the tool's URL and must not change.
*   **`description`** (required): A complete description of the tool. Explain what it does, what it is for, and what its advantages are. Feel free to be detailed.
*   **`version`** (required): The current version of the tool, following the semantic versioning format (e.g., `1.0.0`, `2.3.1-beta`).
*   **`author`** (required): The name of the tool's author, or the organization that maintains it.
*   **`website`** (optional): The URL of the tool's official website (if applicable).
*   **`repository`** (required): The URL of the tool's source code repository (e.g., GitHub, GitLab, Bitbucket).
*   **`tags`** (required): A list of keywords describing the tool. Use relevant terms to facilitate searching.
*   **`icon`** (required): The relative path to the application's icon in the repository.

### Compatibility

*   **`compatibility`** (required):
    *   **`sunshine`** (required): `true` if the tool is compatible with Sunshine, `false` otherwise.
    *   **`apollo`** (required): `true` if the tool is compatible with Apollo, `false` otherwise.
    *   **`platforms`** (required): List of supported operating systems (`"windows"`, `"linux"`, `"macos"`).

### Installation

*   **`installation`** (required):
    *   **`type`** (required): The type of installation. Possible values: `"executable"`, `"zip"`, `"script"`, `"msi"`, `"portable"`.
    *   **`url`** (required if `type` is `"executable"`, `"zip"`, or `"msi"`): The direct download URL for Windows.
    *   **`linuxUrl`** (required if `platforms` includes `"linux"` and if `type` is `"executable"`, `"zip"`, or `"msi"`): The direct download URL for Linux.
    *   **`macOSUrl`** (required if `platforms` includes `"macos"` and if `type` is `"executable"`, `"zip"`, or `"msi"`): The direct download URL for macOS.
    *   **`args`** (optional): Command-line arguments for the installation (Windows).
    *   **`linuxArgs`** (optional): Command-line arguments for the installation (Linux).
    *   **`macOSArgs`** (optional): Command-line arguments for the installation (macOS).
    *   **`postInstall`** (optional): Relative path to a script to be executed after installation (e.g., `.ps1` for PowerShell, `.sh` for Bash).
    *   **`checksum`** (optional): Checksum to verify the integrity of the downloaded file (e.g., `sha256:...`).
    *   **`versionDetection`** (required): How to detect the installed version:
        *   **`method`** (required): Detection method. Possible values: `"file"` (read a file), `"registry"` (read the Windows registry).
        *   **`file`** (required if `method` is `"file"`): Full path to the file containing the version.
        *   **`registryPath`** (required if `method` is `"registry"`): Path to the registry key.
        *   **`registryKey`** (required if `method` is `"registry"`): Name of the registry value.
        *   **`regex`** (required): Regular expression to extract the version from the file or registry value.

### Uninstallation

*   **`uninstallation`** (required):
    *   **`type`** (required): The type of uninstallation. Possible values: `"executable"`, `"script"`.
    *   **`path`** (required if `type` is `"executable"`): Full path to the uninstallation executable (Windows).
    *   **`args`** (optional): Command-line arguments for uninstallation (Windows).
    *   **`linuxPath`** (required if `platforms` includes `"linux"` and `type` is `"executable"`): Full path to the uninstallation executable (Linux).
    *   **`linuxArgs`** (optional): Command-line arguments for uninstallation (Linux).
    *   **`macOSPath`** (required if `platforms` includes `"macos"` and `type` is `"executable"`): Full path to the uninstallation executable (macOS).
    *   **`macOSArgs`** (optional): Command-line arguments for uninstallation (macOS).

### Configuration

*   **`configuration`** (required):
    *   **`type`** (required): Type of configuration. Possible values: `"url"`, `"file"`, `"script"`, `"registry"`.
    *   **`url`** (required if `type` is `"url"`): URL of the configuration interface.
    *   **`file`** (required if `type` is `"file"`): Full path to the configuration file.
    *   **`format`** (required if `type` is `"file"`): Format of the configuration file (`"json"`, `"ini"`, `"properties"`).
    *   **`registryPath`** (required if `type` is `"registry"`): Path to the registry key.
    *   **`registryKey`** (required if `type` is `"registry"`): Name of the registry value.

### Updates

*   **`updates`** (optional):
    *   **`checkUrl`** (required if `updates` is present): URL to check for the availability of an update (e.g., GitHub API).
    *   **`versionRegex`** (required if `updates` is present): Regular expression to extract the latest version.
    *   **`changelogUrl`** (optional): URL to the changelog.

### Rating (optional)

*   **`rating`** (optional):
    *   **`average`** : Average rating (e.g., `4.5`).
    *   **`count`** : Total number of ratings.

### Screenshots and Icon

*   **`screenshots`** (optional): An array of relative paths to screenshots of the tool. Screenshots should be placed in a `screenshots` subfolder next to the `manifest.json` file.

## Tool Folder

The structure of your tool folder should be as follows:

```
tool-name/
├── manifest.json
├── icon.png
├── screenshots/
│   ├── screenshot1.png
│   └── screenshot2.png
└── README.md (optional, but recommended)
```

*   `manifest.json`: The metadata file (required).
*   `icon.png`: An icon for the tool (required, PNG format, recommended size: 256x256 pixels).
*   `screenshots/`: A folder containing screenshots (optional).
*   `README.md`: A README file specific to the tool (optional, but recommended).

## Validation

Before submitting your tool, make sure your `manifest.json` file is valid using a JSON Schema validator. You can use online tools like [https://www.jsonschemavalidator.net/](https://www.jsonschemavalidator.net/) or code editor extensions. The JSON schema for `manifest.json` will be available in the `templates` folder of the `sunshine-aio-library` repository.

## Submission

To submit your tool, create a pull request on the `sunshine-aio-library` GitHub repository. Your submission will be reviewed by moderators before being accepted.