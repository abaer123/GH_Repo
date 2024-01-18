# External Vulnerability Tracking

This project can be used to automatically export a project's vulnerabilities to Jira.

## Getting started

To run this script, Fork or Import this project add the following [CI / CD Variables](https://docs.gitlab.com/ee/ci/variables/):

| Variable Name | Description | Example Value|
|---------------|------------|---------------|
| GRAPHQL_API_TOKEN 	| [Personal Access Token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) with read_api access 	| secure value                                                            	|
| GRAPHQL_API_URL   	| The URL to your GraphQL API. For SaaS this will be https://gitlab.com/api/graphql                                 	| https://gitlab.com/api/graphql or https://your-gitlab-url/api/graphql 	|
| PROJECT_PATH      	| The project path that you want to get vulnerabilities for.                                                        	| jwagner-demo/vandelay-industries/engineering/rails-saas                 	|
| JIRA_API_TOKEN        | Jira [Personal Access Token](https://id.atlassian.com/manage-profile/security/api-tokens)                           | ABCDEF_21341-23509=abcdefg      |
| JIRA_API_URL       	| The issue endpoint URL for your Jira API. For SaaS this will be https://ORG_NAME.atlassian.net/rest/api/latest/issue/ | https://ORG_NAME.atlassian.com/rest/api/latest/issue/ or http://host:port/context/rest/api-name/api-version/issue/              |
| JIRA_EMAIL        | Jira account email to authenticate as                           | smathur@gitlab.com      |
| JIRA_PROJECT     	    | The Jira project key where you want to create vulnerability tickets.                                                  | ABC           |


## How it works

1. When the pipeline runs, it runs `export_vulns.py`.
2. `export_vulns.py` gets the vulnerabilities for your project using the [GraphQL Vulnerability API](https://docs.gitlab.com/ee/api/graphql/reference/#queryvulnerabilities).
3. `export_vulns.py` then sends requests to Jira's API to create a ticket for each vulnerability, unless a ticket for that vulnerability already exists.


## Resources

- [GitLab GraphQL API - Vulnerabilities](https://docs.gitlab.com/ee/api/graphql/reference/index.html#fields-1042)
- [Jira REST API Examples](https://developer.atlassian.com/server/jira/platform/jira-rest-api-examples)


## Disclaimer

This script is provided for educational purposes. It is **not supported by GitLab**. However, you can create an issue if you need help or propose a Merge Request. This script reads data via the GitLab API and performs write actions to Jira. This script requires a read_api token with Developer access for GitLab, as well as a token for Jira. Make sure to rotate/expire the tokens regularly.

This script produces Jira tickets containing vulnerability info. Please use this script and its outputs with caution and in accordance to your local data privacy regulations.
