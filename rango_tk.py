import os
import csv
import time
import codecs
import gitlab
import tkinter
import threading
from tkinter.filedialog import askdirectory


def csv_write(path, data):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, dialect="excel")
        writer.writerow(codecs.BOM_UTF8)
        for row in data:
            if len(row) > 10:
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


class Rango(object):
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title('Rango')
        self.window.geometry("600x496")
        self.window.resizable(False, False)
        self.window.configure(bg='#adae78')
        self.initUI()
        self.window.mainloop()

    def initUI(self):
        self.host_label = tkinter.Label(self.window, text="Git Host:", bg='orange', font='楷体 16 bold')
        self.token_label = tkinter.Label(self.window, text="Git Token:", bg='orange', font='楷体 16 bold')
        self.project_label = tkinter.Label(self.window, text="Project ID:", bg='orange', font='楷体 16 bold')
        self.store_label = tkinter.Label(self.window, text="Store Path:", bg='orange', font='楷体 16 bold')

        self.host_entry = tkinter.Entry(self.window)
        self.token_entry = tkinter.Entry(self.window)
        self.project_entry = tkinter.Entry(self.window)
        self.store_entry = tkinter.Entry(self.window, state='readonly')

        self.text = tkinter.Text(self.window, bg='#bbbbbb', fg='black', font='楷体 16 bold', state='disabled')

        self.path_btn = tkinter.Button(self.window, text='Choice Path', font='楷体 16 bold', bg='orange', command=self.set_path)
        self.run_btn = tkinter.Button(self.window, text='Run', font='楷体 16 bold', bg='orange', command=lambda: self.run(self.get_data))

        self.host_label.place(x=2, y=10, width=97)
        self.token_label.place(x=2, y=50, width=97)
        self.project_label.place(x=2, y=90, width=97)
        self.store_label.place(x=2, y=130, width=97)

        self.host_entry.place(x=100, y=10, width=496)
        self.token_entry.place(x=100, y=50, width=496)
        self.project_entry.place(x=100, y=90, width=496)
        self.store_entry.place(x=100, y=130, width=496)

        self.text.place(x=2, y=170, width=596, height=280)
        self.path_btn.place(x=440, y=455, width=100, height=30)
        self.run_btn.place(x=540, y=455, width=50, height=30)

    def set_path(self):
        p = askdirectory(title='选择保存路径')
        self.store_entry['state'] = 'normal'
        self.store_entry.delete(0, tkinter.END)
        self.store_entry.insert(tkinter.END, p)
        self.store_entry['state'] = 'readonly'

    @staticmethod
    def run(func, *args):
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()

    def get_data(self):
        try:
            host = self.host_entry.get().strip()
            token = self.token_entry.get().strip()
            project_id = self.project_entry.get().strip()
            store_path = self.store_entry.get().strip()
            self.text['state'] = 'normal'
            self.text.delete(0.0, tkinter.END)
            self.text['state'] = 'disabled'

            if not all([host, token, project_id, store_path]):
                self.text['state'] = 'normal'
                self.text.insert(tkinter.END, "请填写上面所有字段\n")
                self.text['state'] = 'disabled'
                return

            try:
                p_id = int(project_id)
            except Exception:
                self.text['state'] = 'normal'
                self.text.insert(tkinter.END, "Project id must be int\n")
                self.text['state'] = 'disabled'
                return
            self.text['state'] = 'normal'
            self.text.insert(tkinter.END, "Connect to host: %s by token: %s\n\n" % (host, token))
            self.text['state'] = 'disabled'
            git = GitLabOps(host, token)
            self.text['state'] = 'normal'
            self.text.insert(tkinter.END, "Connect to host: %s success\n" % host)
            self.text.insert(tkinter.END, "Getting Project %s issues.....\n" % project_id)
            self.text['state'] = 'disabled'
            issues = git.get_project_issues(project_id)
            self.text['state'] = 'normal'
            self.text.insert(tkinter.END, "Getting Project %s issues finished\n" % project_id)
            self.text['state'] = 'disabled'
            csv_file_name = 'Gitlab_issues_result_' + str(project_id) + '_' + str(int(time.time())) + '.csv'
            csv_file = os.path.join(store_path, csv_file_name)
            self.text['state'] = 'normal'
            self.text.insert(tkinter.END, "Generating CSV .....\n")
            self.text['state'] = 'disabled'
            generate_csv(issues, csv_file)
            self.text['state'] = 'normal'
            self.text.insert(tkinter.END, "Generated CSV at:%s\n" % csv_file)
            self.text['state'] = 'disabled'

        except Exception as e:
            self.text['state'] = 'normal'
            self.text.insert(tkinter.END, e)
            self.text['state'] = 'disabled'


if __name__ == '__main__':
    rango = Rango()
