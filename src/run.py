import os
from views import app
from database import db

''' Adiciona a página static no monitoramento do use_reloader=True '''
extra_dirs = ['static','templates']
extra_files = extra_dirs[:]
for extra_dir in extra_dirs:
    for dirname, dirs, files in os.walk(extra_dir):
        for filename in files:
            filename = os.path.join(dirname, filename)
            if os.path.isfile(filename):
                extra_files.append(filename)

if __name__ == '__main__':
    try:
        with app.app_context():
            db.drop_all()
            db.create_all()
            port = int(os.environ.get("PORT", 5000))
            app.run(host='0.0.0.0',port=app.config['PORT'],debug=False,use_reloader=True,threaded=True)
    except Exception as error:
        print('\n*** Exception ***\nerror: %s\n' %str(error))