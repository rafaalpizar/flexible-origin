import sys
sys.path.insert(0,  '/srv/flexible_origin')

from flexorigin import app as application


# TO USE IN PRODUCTION UBUNTU SERVER

# python_home = '/srv/flexible_origin_venv'

# activate_this = python_home + '/bin/activate_this.py'
# with open(activate_this) as file_:
#      exec(file_.read(), dict(__file__=activate_this))

# import sys
# sys.path.insert(0,  '/srv/flexible_origin')
# from flexorigin import app as application