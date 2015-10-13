from flask import Flask, Response, redirect
from gitvotal import github

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return Response('Welcome to Gitvotal!', status=200, mimetype='text/plain')


@app.route("/github_issues", methods=['GET'])
def get_github_issues():
    return Response(github.get_github_issues(), status=200, mimetype="application/xml")


@app.route("/open/<issue_id>", methods=['GET'])
def to_github_issue(issue_id):
    return redirect(github.issue_url(issue_id))


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
