STUDENTS_TABLES = (
    'Admission',
    'StudentSugestionsBox',
    'Performance',
)


'''
helpful for Python. As shown on Ruddra’s Blog, install the following packages:

$ pip install pep8
$ pip install autopep8
$ pip install pylint

And then add the following settings:
{
    "team.showWelcomeMessage": false,
    "editor.formatOnSave": true,
    "python.linting.pep8Enabled": true,
    "python.linting.pylintPath": "/path/to/pylint",
    "python.linting.pylintArgs": [
        "--load-plugins",
        "pylint_django"
    ],
    "python.linting.pylintEnabled": true
}

Editor settings may also be language-specific. For example, to limit automatic formatting to Python files only:
{
    "[python]": {
        "editor.formatOnSave": true
    }
}

Make sure to set the pylintPath setting to the real path value. Keep in mind that these settings are optional.

Launch VS Code Quick Open (Ctrl+P), paste the following command, and press enter. for auto import py libs
ext install brainfit.vscode-importmagic
'''


Default error handlers:

It's worth reading the documentation of the default error handlers, page_not_found, server_error, 
permission_denied and bad_request. By default, they use these templates if they can find them, 
respectively: 404.html, 500.html, 403.html, and 400.html.

So if all you want to do is make pretty error pages, just create those files in a 
TEMPLATE_DIRS directory, you don't need to edit URLConf at all. Read the documentation to 
see which context variables are available.

In Django 1.10 and later, the default CSRF error view uses the template 403_csrf.html.

