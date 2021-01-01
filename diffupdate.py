import sys

from DDBFile import DDBFile


def main(argv: list):
    help_txt = """
    DiffUpdate stores different versions of binary files in an efficient manner
    - by retaining differences between versions instead of the entire files
    
    "create":
        'Creates a version db for the specified file'
        'usage:'
        'diffupdate create <file.version1> <file.version2> <...>'
        'note: the order of the passed files does not matter, you will change between versions either by names or assigned id'
    
    "--name"
        'By default, the db has the name of the first passed file, use this to change the db name'
        'usage:'
        'diffupdate create <file.version1> <file.version2> <...> --name my_file_history.ddb'
    
    "update"
        'Using a previously created db, navigate to the specified version'
        'usage:'
        'diffupdate update <file.version2> <db_file.ddb>'
    
    "list"
    '[FUTURE] Using a previously created db, list all the files in the given db'
    """

    if len(sys.argv) == 1 or sys.argv[1] == 'help':
        print(help_txt)
    elif sys.argv[1] == 'create':
        db_name = None
        if len(sys.argv) >= 4:
            for i in range(2, len(sys.argv)-1):
                if sys.argv[i] == '-n' or sys.argv[i] == '--name':
                    db_name = sys.argv[i+1]
        else:
            print('Too few names passed')
            exit(0)

        db_name = db_name if db_name else sys.argv[2].split('.')[0]
        db = DDBFile(db_name, sys.argv[2:])

        db.dump()
        print('Created new db: ' + db.out_file)
    elif sys.argv[1] == 'update':
        assert len(sys.argv) >= 4, "Too few names passed"
        db_name = None
        if len(sys.argv) == 5:
            if sys.argv[3] == '-n' or sys.argv[3] == '--name':
                db_name = sys.argv[4]
        db_name = db_name if db_name else sys.argv[3].split('.')[0]

        print('Updating')
        DDBFile(db_name).update(sys.argv[2])


if __name__ == "__main__":
    main(sys.argv)
