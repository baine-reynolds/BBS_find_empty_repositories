import requests
import getpass
import json

url = input("Please enter the Source instance's Base URL (i.e. https://bitbucket.mycompany.com (Server)):\n")
admin_user = input("Please enter the Admin username for your source environment:\n")
admin_password = getpass.getpass("Please enter the Admin password for your source environment:\n")

session = requests.Session()
session.auth = (admin_user, admin_password)


def get_projects(projects_endpoint, paged_start=None, paged_limit=None):
    while True:
        params = {'start': paged_start, 'limit': paged_limit}
        r = session.get(projects_endpoint, params=params)
        r_data = r.json()
        for project_json in r_data['values']:
            yield project_json
        if r_data['isLastPage'] == True:
            return
        paged_start = r_data['nextPageStart']

def get_user_names(users_endpoint, paged_start=None, paged_limit=None):
    while True:
        params = {'start': paged_start, 'limit': paged_limit}
        r = session.get(users_endpoint, params=params)
        r_data = r.json()
        for repo_json in r_data['values']:
            yield repo_json
        if r_data['isLastPage'] == True:
            return
        paged_start = r_data['nextPageStart']

def get_repos(repos_endpoint, paged_start=None, paged_limit=None):
    while True:
        params = {'start': paged_start, 'limit': paged_limit}
        r = session.get(repos_endpoint, params=params)
        r_data = r.json()
        for repo_json in r_data['values']:
            yield repo_json
        if r_data['isLastPage'] == True:
            return
        paged_start = r_data['nextPageStart']

def check_if_empty(single_repo_endpoint):
    r = session.get(single_repo_endpoint)
    if r.status_code == 204:  # No Content
        return True
    else:
        return False

def check_if_fork(fork_endpoint):
    r = session.get(fork_endpoint)
    r_data = r.json()
    try:
        if r_data['origin']['slug'] != "":  # If the 'origin' block exists
            return True
    except KeyError:
        return False

def run():
    # Primary project/repos
    print(f"##### The following are Standard Repositories #####")
    projects_endpoint = f"{url}/rest/api/latest/projects"
    for project in get_projects(projects_endpoint):
        repos_endpoint = f"{projects_endpoint}/{project['key']}/repos"
        for repo in get_repos(repos_endpoint):
            single_repo_endpoint = f"{repos_endpoint}/{repo['slug']}/branches/default"

            fork_endpoint = f"{repos_endpoint}/{repo['slug']}"
            if check_if_fork(fork_endpoint):
                fork_status = " (Fork)"
            else:
                fork_status = ""
                
            if check_if_empty(single_repo_endpoint):
                print(f"The Repository '~{project['key']}/{repo['slug']}' has an empty default branch, likely indicating that the repo itself is empty. {fork_status}")

    # Personal repos
    print(f"\n##### The following are personal Repositories #####")
    users_endpoint = f"{url}/rest/api/latest/admin/users"
    for user in get_user_names(users_endpoint):
        repos_endpoint = f"{projects_endpoint}/~{user['slug']}/repos"
        for repo in get_repos(repos_endpoint):
            single_repo_endpoint = f"{repos_endpoint}/{repo['slug']}/branches/default"

            fork_endpoint = f"{repos_endpoint}/{repo['slug']}"
            if check_if_fork(fork_endpoint):
                fork_status = " (Fork)"
            else:
                fork_status = ""

            if check_if_empty(single_repo_endpoint):
                print(f"The Repository '~{project['key']}/{repo['slug']}' has an empty default branch, likely indicating that the repo itself is empty. {fork_status}")

if __name__ == '__main__':
    run()