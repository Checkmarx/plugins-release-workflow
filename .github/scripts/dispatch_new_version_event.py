import os
import requests
import sys

def trigger_github_workflow(org, repo, event_type, payload, github_token):
    """
    Trigger a GitHub Actions workflow using the repository_dispatch event.

    :param org: GitHub organization or user name (e.g., 'Checkmarx')
    :param repo: Repository name (e.g., 'ast-github-action')
    :param event_type: The type of event to trigger
    :param payload: The client payload to send with the event
    :param github_token: Personal Access Token (PAT) with appropriate permissions
    """
    url = f'https://api.github.com/repos/{org}/{repo}/dispatches'
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'token {github_token}'
    }
    data = {
        'event_type': event_type,
        'client_payload': payload
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 204:
        print(f'Success: Dispatched {event_type} event to {org}/{repo}.')
    else:
        print(f'Error: Failed to dispatch event to {org}/{repo}. Status code: {response.status_code}')
        print(f'Response: {response.json()}')
        sys.exit(1)

if __name__ == "__main__":
    GH_ORG = os.getenv('GH_ORG')
    GH_REPO = os.getenv('GH_REPO')
    CLI_VERSION = os.getenv('CLI_VERSION', '')
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    IS_CLI_RELEASE = os.getenv('IS_CLI_RELEASE', 'false').lower() == 'true'
    IS_JS_RELEASE = os.getenv('IS_JS_RELEASE', 'false').lower() == 'true'
    IS_JS_RUNTIME_RELEASE = os.getenv('IS_JS_RUNTIME_RELEASE', 'false').lower() == 'true'
    IS_JAVA_RELEASE = os.getenv('IS_JAVA_RELEASE', 'false').lower() == 'true'

    if not GH_ORG or not GH_REPO or not GITHUB_TOKEN:
        raise ValueError("GH_ORG, GH_REPO, and GITHUB_TOKEN environment variables must be set.")

    if IS_CLI_RELEASE:
        event_type = 'cli-version-update'
        payload = {
            'cli_version': CLI_VERSION
        }
    elif IS_JS_RELEASE:
        event_type = 'js-wrapper-version-update'
        payload = {
            'cli_version': CLI_VERSION
        }
    elif IS_JS_RUNTIME_RELEASE:
        event_type = 'js-runtime-wrapper-version-update'
        payload = {
            'cli_version': CLI_VERSION
        }
    elif IS_JAVA_RELEASE:
        event_type = 'java-wrapper-version-update'
        payload = {
            'cli_version': CLI_VERSION
        }
    else:
        raise ValueError("At least one release type environment variable must be set to true.")

    trigger_github_workflow(GH_ORG, GH_REPO, event_type, payload, GITHUB_TOKEN)
