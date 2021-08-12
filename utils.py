import csv
import codecs
import gitlab


def csv_write(path, data):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, dialect="excel")
        writer.writerow(codecs.BOM_UTF8)
        for row in data:
            writer.writerow(row)
    return True


class GitLabOps():
    def __init__(self, gitlab_host, token):
        self.gitlab_host = gitlab_host
        self.token = token
        self.gitObj = gitlab.Gitlab(self.gitlab_host, self.token)

    def get_project_issues(self, project_id):
        project = self.gitObj.projects.get(project_id)
        issues = project.issues.list(all=True)
        return issues


def generate_csv(issues, file_path):
    title = ["id", "iid", "project_id", "title", "description", "state", "created_at", "updated_at", "closed_at", "labels", "milestone_id", "milestone_iid", "milestone_project_id", "milestone_title",
             "milestone_description", "milestone_state", "milestone_create_at", "milestone_updated_at", "milestone_state", "milestone_due_date", "assignees_id", "assignees_name", "assignees_username",
             "assignees_state", "assignees_avatar_url", "assignees_web_url", "author_id", "author_name", "author_username", "author_state", "author_avatar_url", "author_web_url", "assignee_id",
             "assignee_name", "assignee_username", "assignee_state", "assignee_avatar_url", "assignee_web_url", "user_notes_count", "upvotes", "downvotes", "due_date", "confidential", "web_url"]
    all_issues = []
    all_issues.append(title)
    for issue in issues:
        id_ = issue.id
        iid = issue.iid
        project_id = issue.project_id
        title = issue.title
        description = issue.description
        state = issue.state
        created_at = issue.created_at
        updated_at = issue.updated_at
        closed_at = issue.closed_at
        labels = ";".join(issue.labels)
        milestone = issue.milestone
        if milestone:
            milestone_id = milestone.get("id")
            milestone_iid = milestone.get("iid")
            milestone_project_id = milestone.get("project_id")
            milestone_title = milestone.get("title")
            milestone_description = milestone.get("description")
            milestone_state = milestone.get("state")
            milestone_create_at = milestone.get("created_at")
            milestone_updated_at = milestone.get("updated_at")
            milestone_state = milestone.get("state")
            milestone_due_date = milestone.get("due_date")

        else:
            milestone_id = ""
            milestone_iid = ""
            milestone_project_id = ""
            milestone_title = ""
            milestone_description = ""
            milestone_state = ""
            milestone_create_at = ""
            milestone_updated_at = ""
            milestone_state = ""
            milestone_due_date = ""

        assignees = issue.assignees
        assignees = issue.assignees[0] if assignees else None

        if assignees:
            assignees_id = assignees.get("id")
            assignees_name = assignees.get("name")
            assignees_username = assignees.get("username")
            assignees_state = assignees.get("state")
            assignees_avatar_url = assignees.get("avatar_url")
            assignees_web_url = assignees.get("web_url")
        else:
            assignees_id = ""
            assignees_name = ""
            assignees_username = ""
            assignees_state = ""
            assignees_avatar_url = ""
            assignees_web_url = ""

        author = issue.author
        if author:
            author_id = author.get("id")
            author_name = author.get("name")
            author_username = author.get("username")
            author_state = author.get("state")
            author_avatar_url = author.get("avatar_url")
            author_web_url = author.get("web_url")
        else:
            author_id = ""
            author_name = ""
            author_username = ""
            author_state = ""
            author_avatar_url = ""
            author_web_url = ""

        assignee = issue.assignee
        if assignee:
            assignee_id = assignee.get("id")
            assignee_name = assignee.get("name")
            assignee_username = assignee.get("username")
            assignee_state = assignee.get("state")
            assignee_avatar_url = assignee.get("avatar_url")
            assignee_web_url = assignee.get("web_url")
        else:
            assignee_id = ""
            assignee_name = ""
            assignee_username = ""
            assignee_state = ""
            assignee_avatar_url = ""
            assignee_web_url = ""

        user_notes_count = issue.user_notes_count
        upvotes = issue.upvotes
        downvotes = issue.downvotes
        due_date = issue.due_date
        confidential = issue.confidential
        web_url = issue.web_url

        goal = [id_, iid, project_id, title, description, state, created_at, updated_at, closed_at, labels, milestone_id, milestone_iid, milestone_project_id, milestone_title,
                milestone_description, milestone_state, milestone_create_at, milestone_updated_at, milestone_state, milestone_due_date, assignees_id, assignees_name, assignees_username,
                assignees_state, assignees_avatar_url, assignees_web_url, author_id, author_name, author_username, author_state, author_avatar_url, author_web_url, assignee_id, assignee_name,
                assignee_username, assignee_state, assignee_avatar_url, assignee_web_url, user_notes_count, upvotes, downvotes, due_date, confidential, web_url]

        all_issues.append(goal)

    csv_write(file_path, all_issues)
    return all_issues
