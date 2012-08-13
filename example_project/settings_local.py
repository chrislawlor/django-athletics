DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'athletics',                      # Or path to database file if using sqlite3.
        'USER': 'athletics',                      # Not used with sqlite3.
        'PASSWORD': 'athletics',                  # Not used with sqlite3.
        'HOST': 'webstack-vm',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}