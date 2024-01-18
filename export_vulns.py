from datetime import date, datetime
import requests
import os
import json
import base64


# GraphQL Severity level filtering
# Severity of the vulnerability (INFO, UNKNOWN, LOW, MEDIUM, HIGH, CRITICAL).

def get_vulnerabilities(end_cursor = ''):

    # Get The API Token From The Project CI / CD Variables
    token = os.environ.get("GRAPHQL_API_TOKEN")

    # Get The URL To Your GraphQL API From The Project CI / CD Variables
    url = os.environ.get("GRAPHQL_API_URL")

    # Get Th The Path Of The Project You Want Vulnerabilities For From The Project CI / CD Variables
    project_path = os.environ.get("PROJECT_PATH")

    # GraphQL Query To Get List Of Vulnerabilities For A Project
    # TODO: This is a hack to insert variables into a multi line string
    # TODO: Fetch specific scanner, solution, evidence, location
    vulnerability_query = """
    query {
        project(fullPath: "<project_path>") {
            vulnerabilities(state: [DETECTED, CONFIRMED], severity: [CRITICAL, HIGH]<end_cursor>) {
                nodes {
                    detectedAt
                    title
                    severity
                    primaryIdentifier {
                        name
                    }
                    scanner {
                        reportTypeHumanized
                    }
                    project {
                        path
                        webUrl
                    }
                    links {
                        name
                        url
                    }
                    identifiers {
                        name
                        url
                    }
                    description
                    webUrl
                }
                pageInfo {
                    endCursor
                    hasNextPage
                }
            }
        }
    }
    """
    vulnerability_query = vulnerability_query.replace("<project_path>", project_path)

    if len(end_cursor) > 0:
        vulnerability_query = vulnerability_query.replace("<end_cursor>", f', after: "{end_cursor}"')
    else:
        vulnerability_query = vulnerability_query.replace("<end_cursor>", '')

    # Set Headers And Make THe Request
    headers = {"Authorization": f'Bearer {token}'}
    project_request = requests.post(url, json={'query': vulnerability_query}, headers=headers)

    # Convert The Response To JSON
    json_data = json.loads(project_request.text)
    vulnerability_list = json_data["data"]["project"]["vulnerabilities"]["nodes"]
    has_next_page = json_data["data"]["project"]["vulnerabilities"]["pageInfo"]["hasNextPage"]
    end_cursor = json_data["data"]["project"]["vulnerabilities"]["pageInfo"]["endCursor"]   

    return vulnerability_list, has_next_page, end_cursor

def create_tickets(vulnerability):
    print(vulnerability)

    # Get Jira API request info
    jira_url = os.environ.get("JIRA_API_URL")
    jira_email = os.environ.get("JIRA_EMAIL")
    jira_token_decoded = os.environ.get("JIRA_API_TOKEN")
    jira_token = base64.b64encode(bytes(jira_email+':'+jira_token_decoded, 'utf-8')).decode('utf-8')
    jira_headers = {'Content-Type':'application/json', 'Authorization':'Basic '+jira_token}
    
    project_key = os.environ.get("JIRA_PROJECT")
    # Set the Jira ticket description text
    description_text = '''
    {desc}

    **Primary identifier**: {identifier}

    **Scanner**: {scanner}

    **Detected at**: {detected_at}

    **Project**: {project_url}

    **Vulnerability page**: {vuln_link}
    '''.format(desc = vulnerability["description"],
               identifier = vulnerability["primaryIdentifier"]["name"],
               scanner = vulnerability["scanner"]["reportTypeHumanized"],
               detected_at = datetime.strptime(vulnerability["detectedAt"], "%Y-%m-%dT%H:%M:%SZ").strftime("%B %d, %Y"),
               project_url = vulnerability["project"]["webUrl"],
               vuln_link = vulnerability["webUrl"])

    # Fetch the vulnerability's unique ID from GitLab, to allow for easy searching and prevent duplicates in Jira
    vuln_id = vulnerability["webUrl"][vulnerability["webUrl"].rfind('/')+1:]

    # Data to be sent as part of POST request
    data={
        "fields": {
            "project": {
                "key": project_key
            },
            "summary": vulnerability["title"] + ' ['+vuln_id+']',
            "description": description_text,
            "issuetype": {
                "name": "Task"
            },
            "labels": [
                vulnerability["severity"].lower().capitalize()
            ]
        }
    }
    
    # Check if a ticket already exists for this vulnerability in Jira
    search_jira = requests.get(url=jira_url.replace('issue/','search?jql=summary~'+vuln_id), headers=jira_headers)
    print(search_jira.json())
    # If no ticket exists in Jira, then create one
    if len(search_jira.json()['issues']) == 0:
        submit_jira = requests.post(url=jira_url, json=data, headers=jira_headers)
        print(submit_jira.status_code)
        print(submit_jira.text)

if __name__ == "__main__":

    has_next_page = True
    end_cursor = ''

    while has_next_page:

        vulnerability_response = get_vulnerabilities(end_cursor)
        vulnerability_list = vulnerability_response[0]
        has_next_page = vulnerability_response[1]
        end_cursor = vulnerability_response[2]

        for vulnerability in vulnerability_list:
            create_tickets(vulnerability)
