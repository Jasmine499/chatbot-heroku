from jira.client import JIRA

jira=JIRA(basic_auth=('dtejashwini@stratapps.com','0DoVu9iM9acCZ795ngv20AEC'),options={'server': 'https://xamplify.atlassian.net/'})

#Creating an issue:

new_issue = jira.create_issue(project={'key': 'XBI'}, summary='sample issue-summary',   description='sample issue-description', issuetype={'name': 'Bug'})

print(new_issue)
# or creating issues using dict:

# issue_dict = {
#     'project': {'key': 'PROJ'},
#     'summary': 'New issue from jira-python',
#     'description': 'Look into this one',
#     'issuetype': {'name': 'Bug'},
# }
# new_issue = jira.create_issue(fields=issue_dict)
