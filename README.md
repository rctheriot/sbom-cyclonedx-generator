## SBOM Generator

Generate a CycloneDX SBOM for a container image using Syft, enrich it with vulnerability findings from Grype, and save the merged result.

### What this does
- Runs Syft to produce a CycloneDX JSON SBOM for the given image
- Runs Grype to produce CycloneDX JSON vulnerability data for the same image
- Merges the Grype `vulnerabilities` into the Syft SBOM and writes a single JSON file

### Prerequisites
- **Python 3.8+** (use the `python3` command)
- **Syft** (CLI) installed and on your `PATH`
- **Grype** (CLI) installed and on your `PATH`
- Network access to pull the image (authenticate to your registry if required)

### Install Syft and Grype

macOS (Homebrew):
```bash
brew install anchore/syft/syft
brew install anchore/grype/grype
```

Alternative (Linux/macOS) via install scripts:
```bash
# Syft
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin
# Grype
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin
```

Verify installation:
```bash
syft version
grype version
```

### Usage
From the project root:
```bash
python3 main.py <image_ref> <output_sbom.json>
```

Example:
```bash
python3 main.py alpine:3.19 merged_sbom.json
```

This will:
- Create a Syft CycloneDX JSON SBOM for `alpine:3.19`
- Generate Grype CycloneDX JSON vulnerability data
- Merge vulnerabilities into the Syft SBOM and write `merged_sbom.json`

### Notes
- If your image is in a private registry, log in first (e.g., `docker login`) or configure registry credentials per Syft/Grype docs.
- If no vulnerabilities are found by Grype, a warning is printed and the output SBOM will not include a `vulnerabilities` array.

### Troubleshooting
- "command not found": Ensure `syft` and `grype` are installed and available on your `PATH`.
- Registry/permission errors: Confirm you can pull the image (try `docker pull <image_ref>` or configure credentials).

### License
MIT (or your preferred license). 