import os
import time
import json
from app import app, db
from flask_cors import CORS
from getpass import getuser
from ast import literal_eval
from models import Settings, GitIssues
from forms import GitLabForm, UserForm
from utils import GitLabOps, generate_csv
from flask import render_template, redirect, url_for, flash, Blueprint, jsonify
from flask.views import MethodView


class GetIssuesAPI(MethodView):
    def get(self):
        try:
            git_issues_settings = Settings.query.filter(Settings.name == 'git_issues').first()
            git_issues_settings_content = json.loads(git_issues_settings.content)

            host = git_issues_settings_content.get('gitlab_host')
            token = git_issues_settings_content.get('token')
            project_id = int(git_issues_settings_content.get('project_id'))
            store_path = git_issues_settings_content.get('store_path')
            if not os.path.exists(store_path):
                return jsonify({
                    "message": "Path of %s not exist" % store_path
                }), 400
            else:
                git = GitLabOps(host, token)
                issues = git.get_project_issues(project_id)
                csv_file_name = 'Gitlab_issues_result_' + str(project_id) + '_' + str(int(time.time())) + '.csv'
                csv_file = os.path.join(store_path, csv_file_name)
                all_issues = generate_csv(issues, csv_file)
                db.get_engine().execute("truncate table gitissues")
                for issue in all_issues:
                    new_issue = GitIssues(settings=str(git_issues_settings.content), content=str(issue))
                    db.session.add(new_issue)
                    db.session.commit()
                return jsonify({
                    "message": "Result generated at: %s" % csv_file
                }), 200
        except Exception as e:
            return jsonify({
                "message": "internal error at: %s" % e
            }), 500


api_v1 = Blueprint('api_v1', __name__)
CORS(api_v1)

api_v1.add_url_rule('/get_issues', view_func=GetIssuesAPI.as_view('get_issues'), methods=['GET'])
# app.register_blueprint(api_v1, url_prefix='/api/v1')


@app.route('/')
def index():
    user_info = Settings.query.filter(Settings.name == 'user_info').first()
    user_info_content = json.loads(user_info.content)
    host_user = getuser()

    return render_template('index.html', user_info=user_info_content, host_user=host_user)


@app.route('/user')
def user():
    user_info = Settings.query.filter(Settings.name == 'user_info').first()
    user_info_content = json.loads(user_info.content)

    return render_template('user.html', user_info=user_info_content)


@app.route('/user/edit', methods=['GET', 'POST'])
def edit_user():
    user_info = Settings.query.filter(Settings.name == 'user_info').first()
    user_info_content = json.loads(user_info.content)

    form = UserForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        new_content = {"name": name, "email": email}
        user_info.content = json.dumps(new_content)
        db.session.commit()
        flash('Edit User Successfully.', 'success')
        return redirect(url_for('.user'))
    form.name.data = user_info_content.get('name')
    form.email.data = user_info_content.get('email')

    return render_template('edit_user.html', form=form, user_info=user_info_content)


@app.route('/gitlab/project/issues/settings')
def git_issues_settings():
    user_info = Settings.query.filter(Settings.name == 'user_info').first()
    user_info_content = json.loads(user_info.content)
    git_issues_settings = Settings.query.filter(Settings.name == 'git_issues').first()
    git_issues_settings_content = json.loads(git_issues_settings.content)

    return render_template('gitlab_info.html', gitlab_info=git_issues_settings_content, user_info=user_info_content)


@app.route('/gitlab/project/issues/settings/edit', methods=['GET', 'POST'])
def git_issues_settings_edit():
    user_info = Settings.query.filter(Settings.name == 'user_info').first()
    user_info_content = json.loads(user_info.content)
    git_issues_settings = Settings.query.filter(Settings.name == 'git_issues').first()
    git_issues_settings_content = json.loads(git_issues_settings.content)

    form = GitLabForm()
    if form.validate_on_submit():
        host = form.host.data
        token = form.token.data
        project_id = form.project_id.data
        store_path = form.store_path.data

        new_content = {"gitlab_host": host, "token": token, "project_id": project_id, "store_path": store_path}
        git_issues_settings.content = json.dumps(new_content)
        db.session.commit()

        flash('Edit Gitlab Settings Successfully.', 'success')
        return redirect(url_for('.git_issues_settings'))

    form.host.data = git_issues_settings_content.get('gitlab_host')
    form.token.data = git_issues_settings_content.get('token')
    form.project_id.data = git_issues_settings_content.get('project_id')
    form.store_path.data = git_issues_settings_content.get('store_path')

    return render_template('edit_gitlab.html', form=form, user_info=user_info_content)


@app.route('/gitlab/issues/generate', methods=['GET', 'POST'])
def generate_gitlab_issues():
    try:
        user_info = Settings.query.filter(Settings.name == 'user_info').first()
        user_info_content = json.loads(user_info.content)
        git_issues_settings = Settings.query.filter(Settings.name == 'git_issues').first()
        git_issues_settings_content = json.loads(git_issues_settings.content)

        host = git_issues_settings_content.get('gitlab_host')
        token = git_issues_settings_content.get('token')
        project_id = int(git_issues_settings_content.get('project_id'))
        store_path = git_issues_settings_content.get('store_path')
        if not os.path.exists(store_path):
            flash('Path:%s not exist!' % store_path, 'danger')
            return redirect(url_for('.git_issues_settings'))
        else:
            git = GitLabOps(host, token)
            issues = git.get_project_issues(project_id)
            csv_file_name = 'Gitlab_issues_result_' + str(project_id) + '_' + str(int(time.time())) + '.csv'
            csv_file = os.path.join(store_path, csv_file_name)
            all_issues = generate_csv(issues, csv_file)
            db.get_engine().execute("truncate table gitissues")
            for issue in all_issues:
                new_issue = GitIssues(settings=str(git_issues_settings.content), content=str(issue))
                db.session.add(new_issue)
                db.session.commit()

            flash('Generated CSV at: %s' % csv_file, 'success')
            return redirect(url_for('.git_issues_settings'))
    except Exception as e:
        flash('Error: %s!' % e, 'danger')
        return redirect(url_for('.git_issues_settings'))


@app.route('/gitlab/project/issues/table')
def git_issues_table():
    user_info = Settings.query.filter(Settings.name == 'user_info').first()
    user_info_content = json.loads(user_info.content)
    git_issues_settings = Settings.query.filter(Settings.name == 'git_issues').first()
    git_issues_settings_content = json.loads(git_issues_settings.content)

    issues = GitIssues.query.filter(GitIssues.id).all()
    if len(issues) >= 2:
        issues = [literal_eval(i.content) for i in issues[1:]]
    else:
        issues = []

    return render_template('issues_table.html', gitlab_info=git_issues_settings_content, user_info=user_info_content, issues=issues)
