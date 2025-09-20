# Installation Metadata Guide

This guide explains how to properly configure installation metadata for tools in the Sunshine-AIO library.

## Overview

The installation metadata system supports robust, multi-platform tool installation with automatic release detection, checksum verification, and platform-specific configurations.

## Format Types

### Multi-Platform Format (Recommended)

The modern multi-platform format provides granular control over installation for each supported platform:

```json
{
  "installation": {
    "platforms": {
      "windows": {
        "type": "executable",
        "download_strategy": "github_releases",
        "file_pattern": "*.exe",
        "install_flags": ["/S", "/SILENT", "/VERYSILENT"],
        "install_dir_flag": "/DIR=",
        "requires_admin": true,
        "checksum_verification": true,
        "silent": true
      },
      "linux": {
        "type": "appimage",
        "download_strategy": "github_releases",
        "file_pattern": "*.AppImage",
        "install_flags": ["--silent"],
        "requires_admin": false,
        "checksum_verification": true,
        "silent": true
      },
      "macos": {
        "type": "dmg",
        "download_strategy": "github_releases",
        "file_pattern": "*.dmg",
        "install_flags": ["-allowUntrusted"],
        "requires_admin": false,
        "checksum_verification": true,
        "silent": true
      }
    }
  }
}
```

### Legacy Single-Platform Format

The legacy format is simpler but less flexible:

```json
{
  "installation": {
    "type": "executable",
    "args": [],
    "postInstall": "",
    "checksum": ""
  }
}
```

## Platform Configuration

### Common Properties

All platform configurations support these properties:

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `type` | string | Yes | Installation method type |
| `download_strategy` | string | No | How to download the installer |
| `file_pattern` | string | No | Pattern to match release files |
| `url` | string | No | Direct download URL |
| `executable` | string | No | Specific executable name |
| `install_flags` | array | No | Silent installation flags |
| `install_dir_flag` | string | No | Directory specification flag |
| `requires_admin` | boolean | No | Whether admin privileges are needed |
| `checksum_verification` | boolean | No | Whether to verify file integrity |
| `checksum` | string | No | File checksum for verification |
| `silent` | boolean | No | Whether installation should be silent |

### Installation Types by Platform

#### Windows
- `executable` - Standard .exe installer
- `msi` - Windows Installer package
- `zip` - Compressed archive
- `script` - PowerShell/batch script
- `portable` - Portable executable
- `package-manager` - Package manager (Chocolatey, winget)

#### Linux
- `deb` - Debian package
- `rpm` - RPM package
- `appimage` - AppImage portable application
- `zip` - Compressed archive
- `script` - Shell script
- `portable` - Portable binary
- `package-manager` - Package manager (apt, yum, snap)

#### macOS
- `dmg` - Disk image
- `pkg` - Package installer
- `app` - Application bundle
- `zip` - Compressed archive
- `script` - Shell script
- `portable` - Portable binary
- `package-manager` - Package manager (Homebrew)

### Download Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| `github_releases` | Fetch from GitHub releases using file patterns | Most common for GitHub projects |
| `github_latest` | Use GitHub's latest release redirect | When you need the latest version URL |
| `direct_url` | Use provided URL directly | Custom download locations |
| `package_manager` | Install via system package manager | Distribution through package repos |

### Installation Flags

Platform-specific silent installation flags:

#### Windows
- NSIS: `["/S"]`
- Inno Setup: `["/VERYSILENT", "/SUPPRESSMSGBOXES"]`
- MSI: `["/quiet", "/norestart"]`
- InstallShield: `["/s", "/v/qn"]`

#### Linux
- APT: `["-y", "--force-yes"]`
- YUM: `["-y"]`
- AppImage: `["--silent"]`

#### macOS
- PKG: `["-allowUntrusted"]`
- DMG: `["--silent"]`

## Validation and Security

### Verification Configuration

```json
{
  "verification": {
    "status": "verified",
    "date": "2025-09-19T00:00:00Z",
    "method": "automated",
    "score": 85
  },
  "validation": {
    "checksum_required": false,
    "signature_verification": false,
    "trust_level": "community_verified",
    "auto_update": true
  }
}
```

### Trust Levels

| Level | Description |
|-------|-------------|
| `unverified` | No verification performed |
| `community_verified` | Verified by community members |
| `maintainer_verified` | Verified by tool maintainer |
| `official` | Official release from trusted source |

## Best Practices

### 1. Use Multi-Platform Format
Always prefer the multi-platform format for new tools, even if you only support one platform initially.

### 2. GitHub Releases Strategy
For GitHub-hosted projects, use `github_releases` with appropriate file patterns:

```json
{
  "download_strategy": "github_releases",
  "file_pattern": "*.exe"
}
```

### 3. Silent Installation
Configure appropriate silent installation flags:

```json
{
  "install_flags": ["/S", "/SILENT"],
  "silent": true
}
```

### 4. Security Considerations
- Enable checksum verification when possible
- Use appropriate trust levels
- Specify admin requirements accurately

### 5. File Patterns
Use specific patterns to avoid downloading wrong files:

```json
{
  "file_pattern": "*-windows-*.exe"
}
```

## Example: Complete Tool Configuration

```json
{
  "name": "Example Tool",
  "slug": "example-tool",
  "category": "utilities/system-tools",
  "description": "An example tool for demonstration",
  "repository": "https://github.com/user/example-tool",
  "license": "MIT",
  "platforms": ["Windows", "Linux", "macOS"],
  "language": "Go",
  "compatibility": {
    "sunshine": true,
    "apollo": true,
    "platforms": ["windows", "linux", "macos"]
  },
  "verification": {
    "status": "verified",
    "date": "2025-09-19T00:00:00Z",
    "method": "automated",
    "score": 85
  },
  "validation": {
    "checksum_required": true,
    "signature_verification": false,
    "trust_level": "community_verified",
    "auto_update": true
  },
  "installation": {
    "platforms": {
      "windows": {
        "type": "executable",
        "download_strategy": "github_releases",
        "file_pattern": "*-windows-*.exe",
        "install_flags": ["/S", "/SILENT"],
        "requires_admin": true,
        "checksum_verification": true,
        "silent": true
      },
      "linux": {
        "type": "deb",
        "download_strategy": "github_releases",
        "file_pattern": "*-linux-*.deb",
        "install_flags": ["-y"],
        "requires_admin": true,
        "checksum_verification": true,
        "silent": true
      },
      "macos": {
        "type": "dmg",
        "download_strategy": "github_releases",
        "file_pattern": "*-macos-*.dmg",
        "install_flags": ["-allowUntrusted"],
        "requires_admin": false,
        "checksum_verification": true,
        "silent": true
      }
    }
  },
  "uninstallation": {
    "type": "executable",
    "path": "",
    "args": []
  },
  "configuration": {
    "type": "url",
    "url": "https://localhost:8080",
    "file": ""
  }
}
```

## Migration from Legacy Format

To migrate from the legacy single-platform format to the new multi-platform format:

1. **Wrap existing configuration** in a `platforms` object
2. **Add platform-specific properties** like `download_strategy` and `file_pattern`
3. **Configure security settings** with `verification` and `validation` objects
4. **Test with validation script** to ensure correctness

The validation script will automatically detect legacy formats and provide migration guidance.