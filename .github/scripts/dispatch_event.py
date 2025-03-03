import os
import requests

def trigger_github_workflow(org, repo, cli_version, github_token):
    """
    Trigger a GitHub Actions workflow using the repository_dispatch event.

    :param org: GitHub organization or user name (e.g., 'Checkmarx')
    :param repo: Repository name (e.g., 'ast-github-action')
    :param cli_version: The CLI version to be dispatched
    :param github_token: Personal Access Token (PAT) with appropriate permissions
    """
    url = f'https://api.github.com/repos/{org}/{repo}/dispatches'
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'token {github_token}'
    }
    payload = {
        'event_type': 'cli-version-update',
        'client_payload': {
            'cli_version': cli_version
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 204:
        print(f'Success: Dispatched event to {org}/{repo}.')
    else:
        print(f'Error: Failed to dispatch event to {org}/{repo}. Status code: {response.status_code}')
        print(f'Response: {response.json()}')
        sys.exit(1)

if __name__ == "__main__":
    GH_ORG = os.getenv('GH_ORG')
    GH_REPO = os.getenv('GH_REPO')
    CLI_VERSION = os.getenv('CLI_VERSION', '')
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

    if not GH_ORG or not GH_REPO or not GITHUB_TOKEN:
        raise ValueError("GH_ORG, GH_REPO, and GITHUB_TOKEN environment variables must be set.")

    trigger_github_workflow(GH_ORG, GH_REPO, CLI_VERSION, GITHUB_TOKEN)
