import os
import requests

def main():
    repo = os.getenv('REPO')
    cli_version = os.getenv('CLI_VERSION')
    github_token = os.getenv('GITHUB_TOKEN')

    if not repo or not github_token:
        raise ValueError("REPO and GITHUB_TOKEN environment variables must be set.")

    api_url = f"https://api.github.com/repos/{repo}/dispatches"
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'token {github_token}'
    }
    payload = {
        'event_type': 'cli-version-update',
        'client_payload': {
            'cli_version': cli_version
        }
    }

    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 204:
        print(f"Successfully dispatched event to {repo}")
    else:
        print(f"Failed to dispatch event to {repo}: {response.status_code} {response.text}")

if __name__ == "__main__":
    main()
