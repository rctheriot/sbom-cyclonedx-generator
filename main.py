import json
import subprocess
import sys

def run_command(command):
    """Run a shell command and return its stdout."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {command}")
        print(result.stderr)
        sys.exit(1)
    return result.stdout

def merge_sboms(base_sbom, vuln_sbom):
    vulns = vuln_sbom.get('vulnerabilities', [])
    if vulns:
        base_sbom['vulnerabilities'] = vulns
    else:
        print("Warning: No vulnerabilities found in vulnerability SBOM.")
    return base_sbom

def main(image_ref, output_path):
    print(f"Generating SBOM with Syft for image: {image_ref}")
    syft_cmd = f"syft {image_ref} -o cyclonedx-json"
    syft_output = run_command(syft_cmd)
    syft_sbom = json.loads(syft_output)

    print(f"Generating vulnerability data with Grype for image: {image_ref}")
    grype_cmd = f"grype {image_ref} -o cyclonedx-json"
    grype_output = run_command(grype_cmd)
    grype_sbom = json.loads(grype_output)

    print("Merging vulnerabilities into Syft SBOM...")
    merged_sbom = merge_sboms(syft_sbom, grype_sbom)

    with open(output_path, 'w') as f:
        json.dump(merged_sbom, f, indent=2)
    print(f"Merged SBOM saved to {output_path}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 main.py <image_ref> <output_sbom.json>")
        sys.exit(1)

    image_ref = sys.argv[1]
    output_file = sys.argv[2]
    main(image_ref, output_file)
