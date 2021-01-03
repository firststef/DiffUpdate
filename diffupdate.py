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

    if len(argv) == 1 or argv[1] == 'help':
        print(help_txt)
    elif argv[1] == 'create':
        db_name = None
        param_at_i = None
        if len(argv) >= 4:
            for i in range(2, len(argv)-1):
                if argv[i] == '-n' or argv[i] == '--name':
                    db_name = argv[i+1]
                    param_at_i = i
                    break
        else:
            print('Too few names passed')
            exit(0)

        db_name = db_name if db_name else argv[2].split('.')[0]
        files = argv[2:]
        param_at_i -= 2
        if param_at_i:
            files = [j for i, j in enumerate(files) if i not in (param_at_i, param_at_i + 1)]
        db = DDBFile(db_name, files)

        db.dump()
        print('Created new db: ' + db.out_file)
    elif argv[1] == 'update':
        assert len(argv) >= 4, "Too few names passed"
        db_name = None
        if len(argv) == 5:
            if argv[3] == '-n' or argv[3] == '--name':
                db_name = argv[4]
        db_name = db_name if db_name else argv[3].split('.')[0]

        print('Updating')
        db = DDBFile(db_name)
        db.update(argv[2])
        with open(argv[2], 'wb') as f:
            f.write(db.updated)


if __name__ == "__main__":
    main(sys.argv)
