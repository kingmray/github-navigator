import requests
import json
from flask import render_template, Blueprint, request, jsonify, redirect, session, url_for
from builtins import KeyError
from requests_oauthlib import OAuth2Session
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# This information is obtained upon registration of a new GitHub OAuth
# application here: https://github.com/settings/applications/new
client_id = "dcc59b5cfaf0ad630a72"
client_secret = "9313122755cedd4f2200d119466180e6c7d7bf17"
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'


################
#### config ####
################

main_blueprint = Blueprint('main', __name__,)


################
#### routes ####
################

@main_blueprint.route("/")
def authorization():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    """
    github = OAuth2Session(client_id)
    authorization_url, state = github.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)

# Step 2: User authorization, this happens on the provider.

@main_blueprint.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    github = OAuth2Session(client_id, state=session['oauth_state'])
    token = github.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)

    session['oauth_token'] = token

    return redirect(url_for('.repositories'))

@main_blueprint.route('/repositories', methods=['GET', 'POST'])
def repositories():
    if request.method == 'POST':
        query_string = request.form.get('query_string')
        github = OAuth2Session(client_id, token=session['oauth_token'])
        url = 'https://api.github.com/search/repositories?q={0}&sort=updated&page=1&per_page=5'.format(query_string)
        repositories_response = github.get(url)
        repositories = json.loads(repositories_response.text)
        formated_repositories = []
        for item in repositories['items']:
            commits_url = 'https://api.github.com/repos/{0}/{1}/commits'.format(item['owner']['login'], item['name'])
            commits_response = github.get(commits_url)
            commits = json.loads(commits_response.text)
            #return jsonify({'results': commits})
            if commits:
                #return 'commits {0}'.format(commits[0])
                commit = commits[0]

                repository = {
                    'name': item['name'],
                    'avatar_url': item['owner']['avatar_url'],
                    'html_url': item['html_url'],
                    'created_at': item['created_at'],
                    'owner_login': item['owner']['login'],
                    'sha': commit['sha'],
                    'commit_message': commit['commit']['message'],
                    'commit_author_name': commit['commit']['author']['name'],
                    'commit_class': commits.__class__.__name__
                }
                formated_repositories.append(repository)

        #return jsonify({'results': render_template('search/template.html', repositories=formated_repositories)})
        return render_template('search/template.html', repositories=formated_repositories)
    return render_template('main/repositories.html')
