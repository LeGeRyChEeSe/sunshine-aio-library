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

* **`name`** (required): Le nom complet de l'outil.
* **`slug`** (required): Un identifiant unique pour l'outil, en minuscules, avec des tirets comme séparateurs.
* **`short-description`** (required): Une brève description de l'outil.
* **`long-description`** (optional): Une description détaillée de l'outil, ses fonctionnalités et son but.
* **`author`** (required): Le nom de l'auteur de l'outil ou de l'organisation qui le maintient.
* **`website`** (optional): L'URL du site web officiel de l'outil.
* **`repository`** (required): L'URL du dépôt du code source de l'outil.
* **`tags`** (required): Une liste de mots-clés décrivant l'outil.

### Compatibility

* **`compatibility`** (required):
    * **`sunshine`** (required): `true` si l'outil est compatible avec Sunshine.
    * **`apollo`** (required): `true` si l'outil est compatible avec Apollo.
    * **`platforms`** (required): Liste des systèmes d'exploitation supportés.

### Installation

* **`installation`** (required):
    * **`type`** (required): Le type d'installation (`"executable"`, `"zip"`, `"script"`, `"msi"`, `"portable"`).
    * **`args`** (optional): Arguments en ligne de commande pour l'installation.
    * **`postInstall`** (optional): Chemin relatif vers un script à exécuter après l'installation.
    * **`checksum`** (optional): Somme de contrôle pour vérifier l'intégrité du fichier téléchargé.

### Uninstallation

* **`uninstallation`** (required):
    * **`type`** (required): Le type de désinstallation (`"executable"`, `"script"`).
    * **`path`** (required): Chemin complet vers l'exécutable de désinstallation.
    * **`args`** (optional): Arguments en ligne de commande pour la désinstallation.

### Configuration

* **`configuration`** (optional):
    * **`type`** (optional): Type de configuration (`"url"`, `"file"`, `"script"`, `"registry"`).
    * **`url`** (optional): URL de l'interface de configuration.
    * **`file`** (optional): Chemin complet vers le fichier de configuration.

### Screenshots et Icon

* **`screenshots`** (optional): Un tableau de chemins relatifs vers les captures d'écran de l'outil.
* **`icon`** (optional): Le chemin relatif vers l'icône de l'outil.

## Structure du dossier de l'outil

La structure de votre dossier d'outil doit être la suivante :

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

Avant de soumettre votre outil, assurez-vous que votre fichier `manifest.json` est valide en utilisant un validateur de schéma JSON. Le schéma JSON pour `manifest.json` sera disponible dans le dossier `templates` du dépôt `sunshine-aio-library`.

## Soumission

Pour soumettre votre outil, créez une pull request sur le dépôt GitHub `sunshine-aio-library`. Votre soumission sera examinée par les modérateurs avant d'être acceptée.