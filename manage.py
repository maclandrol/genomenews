#!/usr/bin/env python
import os
import sys
from django.db import connection

def execute_query(query):
    pass


def make_query(exclude):
    pass


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "genomenews.settings")

    from django.core.management import execute_from_command_line

    # I'm adding this because I recently got a ProgrammingError :
    # "relation X does not exist" when attempting to migrate
    # And this is frustrating.
    # So here is my take to do a force migration

    if(len(sys.argv)>1 and sys.argv[1]=="forcemigrate"):
        from django.core import management
        from django.core.management.base import CommandError
        import django

        django.setup()
        currentdata = "currentdata.json"
        with open(currentdata, 'w+') as IN:
            # first we dump the current data into a json file
            try:
                management.call_command('dumpdata', stdout=IN)
                # This could raise a CommandError
                # We are just going to discard that error
            except CommandError:
                pass

        if(os.stat(currentdata).st_size != 0):
            # If the file is not empty, then data is dumped into it
            # We flush the database
            a = management.call_command('sqlflush', verbosity=1)
            from django.db import connection
            tables = connection.introspection.table_names()
            seen_models = connection.introspection.installed_models(tables)
            print tables
            print seen_models
            print len(tables)
            print len(seen_models)

            print a
            management.call_command('dbshell', verbosity=1)
            # now we sync the db
            management.call_command('syncdb')
            # and we load our previous data
            management.call_command('loaddata', currentdata,  verbosity=0)

            try:
                # if we want to delete the json file
                if(sys.argv[2] == "clean"):
                    os.remove(tempfile)
            except (OSError, NameError, IndexError):
                # do nothing
                pass

    else:
        execute_from_command_line(sys.argv)
