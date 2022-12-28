import json, sys, os, tarfile
args = sys.argv[1:]
with open('config.json') as file:
    config = json.load(file)
if not args:
    print(f'Usage: python {sys.argv[0]} [command] [args]')
    sys.exit(1)

match args[0]:
    case 'install':
        if len(args) == 1:
            print('Do you want to install nothing?')
            sys.exit(0)
        else:
            if os.path.isfile(args[1] + '.sopm'):
                try:
                    archive = tarfile.open(args[1] + '.sopm')
                    assert 'data.json' in archive.getnames()
                    metadata = json.loads(archive.extractfile('data.json').read().decode())
                except Exception as e:
                    print(f'Archive was corruted. {e}')
                    sys.exit(0)
                print(f'Installing {metadata["name"]} ...')
                for filename in metadata['files'].keys():
                    print(f'Extracting {filename} ...')
                    with open(metadata['files'][filename], 'wb') as file:
                        file.write(archive.extractfile('files/' + filename).read())
                if metadata.get('script'):
                    print('Running post-install script ...')
                    try:
                        exec(archive.extractfile(metadata.get('script')).read().decode())
                    except:
                        pass
                print('Successfully installed!')
                archive.close()
            else:
                print(f'No such package: "{args[1]}"')
    case 'update':
        print('N/I')
    case other:
        print(f'No such command: "{args[0]}"')
