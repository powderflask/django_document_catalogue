from demo.settings.defaults import *

SECRET_KEY = 'acj2u5f*lsp7g)68u#^v&bn#1w6ajy*)y=cxu5g45@_jmi0x5x'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(BASE_DIR), 'db.sqlite3'),
    }
}