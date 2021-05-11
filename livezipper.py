import sys, os, gzip, shutil
import xml.etree.ElementTree as ET
from os import path

# check arguments
args = sys.argv
if len(args) < 2:
    print('No file selected')
    quit()

# check if file exists
if not path.isfile(args[1]):
    print(f'File does not exist: {args[1]}')
    quit()

#check if file is Live set
if path.splitext(args[1])[1] != '.als':
    print(f'Invalid Live set: {args[1]}')
    quit()

# get project file, name, and directory
file = args[1]
filename = path.splitext(path.basename(file))[0]
dir = path.dirname(file)
print(f'Opened Live set: {file}')

# decompress Live set and extract XML
if not path.exists(path.join(dir, 'livezipper')):
    os.mkdir(path.join(dir, 'livezipper'))
with gzip.open(file, 'rb') as f_in:
    with open(path.join(dir, 'livezipper', filename + '.xml'), 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
file = path.join(dir, 'livezipper', filename + '.xml')

# create collection folder
if path.exists(path.join(dir, 'livezipper', filename)):
    shutil.rmtree(path.join(dir, 'livezipper', filename))
os.mkdir(path.join(dir, 'livezipper', filename))

# collect files and edit paths
transferred = 0
failed = 0
tree = ET.parse(file)
root = tree.getroot()
for file_ref in root.findall('.//MultiSamplePart/SampleRef/FileRef') + root.findall('.//AudioClip/SampleRef/FileRef'):
    rel_path = file_ref.find('RelativePath')
    abs_path = file_ref.find('Path')
    src = abs_path.get('Value')
    if path.isfile(src):
        src_base = path.basename(src)
        with open(src, 'rb') as f_in:
            with open(path.join(dir, 'livezipper', filename, src_base), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print(f'Transferred file: {src}')
        transferred += 1
        if path.isfile(src + '.asd'):
            with open(src + '.asd', 'rb') as f_in:
                with open(path.join(dir, 'livezipper', filename, src_base + '.asd'), 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            print(f'Transferred file: {src}.asd')
            transferred += 1
        rel_path.set('Value', src_base)
        abs_path.set('Value', '')
    else:
        print(f'Could not find file: {src}')
        failed += 1
tree.write(file, encoding='utf-8', xml_declaration=True)

# check if 'Ableton Project Info' folder exists
if path.isdir(path.join(dir, 'Ableton Project Info')):
    shutil.copytree(path.join(dir, 'Ableton Project Info'), path.join(dir, 'livezipper', filename, 'Ableton Project Info'))
    print(f"Transferred folder: {path.join(dir, 'Ableton Project Info')}")

# create list of plugins
print('Getting plugin list')
vst = set()
vst3 = set()
for vst_name in root.findall('.//VstPluginInfo/PlugName'):
    vst.add(vst_name.get('Value') + '\n')
for vst3_name in root.findall('.//Vst3PluginInfo/Name'):
    vst3.add(vst3_name.get('Value') + '\n')
with open(path.join(dir, 'livezipper', filename, 'plugins.txt'), 'w') as f:
    f.write('VST:\n')
    f.writelines(vst)
    f.write('\nVST3:\n')
    f.writelines(vst3)

# compress XML into Live set
print('Writing Live set')
with open(file, 'rb') as f_in:
     with gzip.open(path.join(dir, 'livezipper', filename, filename + '.als'), 'wb') as f_out:
         shutil.copyfileobj(f_in, f_out)

# make zip archive
print('Zipping folder')
file = path.join(dir, 'livezipper', filename)
shutil.make_archive(file, 'zip', path.join(dir, 'livezipper', filename))

print(f'Done: {file}.zip ({transferred} files transferred, {failed} files failed)')