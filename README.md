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