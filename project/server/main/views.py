import requests

from flask import render_template, Blueprint, request, jsonify, redirect, session, url_for, flash
from builtins import KeyError
from requests_oauthlib import OAuth2Session
from project.server.main.models import GitHubFormater
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
    """Step 1: User Authorization."""
    github = OAuth2Session(client_id)
    authorization_url, state = github.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)

# Step 2: User authorization, this happens on the provider.

@main_blueprint.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token."""

    github = OAuth2Session(client_id, state=session['oauth_state'])
    token = github.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)

    session['oauth_token'] = token

    return redirect(url_for('.repositories'))

@main_blueprint.route('/repositories', methods=['GET', 'POST'])
def repositories():
    if request.method == 'POST':
        query_string = request.form.get('query_string')
        if query_string == '':
            flash('please enter a search term.')
            return render_template('main/repositories.html')
        try:
            github = OAuth2Session(client_id, token=session['oauth_token'])
        except KeyError:
            flash('github authorization has gone lost.')
            return redirect(url_for('.authorization'))

        formater = GitHubFormater(github)

        return render_template('search/template.html', repositories=formater.getRepositories(query_string), query_string=query_string)

    return render_template('main/repositories.html')
