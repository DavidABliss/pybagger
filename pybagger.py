# -*- coding: utf-8 -*-

import bagit
import uuid
import os
import argparse
import sys

parser = argparse.ArgumentParser(description='Bag a directory, supplying an existing txt file for the bag-info.txt output')
parser.add_argument('-d', '--directory', help="directory to be bagged", action="store", dest="d", default=os.getcwd())
parser.add_argument('-b', '--baginfo', required=False, help="bag-info.txt file to included in the resulting bag", action="store", dest="b")
parser.add_argument('-u', '--unpack', required=False, help="unpack existing bag at the directory location", action="store_true", dest="u")

args = parser.parse_args()

bagPath = args.d

if args.u:
    import shutil

if not args.u:
    try:
        bagInfo = args.b
    except:
        sys.exit('No bag-info.txt provided. Please provide a bag-info.txt file with -b/--baginfo')

# Declare accepted bag-info fields and whether they are required ("True") or optional ("False")
fieldsDict = {'Source-Organization': False, 'Organization-Address': False, 'Contact-Name': False, 'Contact-Phone': False, 
              'Contact-Email': False, 'External-Description': False, 'External-Identifier': False, 'Internal-Sender-Description': False, 
              'Internal-Sender-Identifier': False, 'Rights-Statement': False, 'Bag-Group-Identifier': False, 'Bag-Size': True}

baginfoDict = {}
# Read the user-supplied bag-info file and load the text into a dictionary
def bagInfoReader(baginfoPath):
    with open(baginfoPath, 'r', encoding='utf-8') as baginfoFile:
        for line in baginfoFile:
            line = line.strip()
            if line == '':
                continue
            # If the line's label is in the allowedFi, the line can go in the baginfo dict
            if line.split(':')[0] in fieldsDict:
                label = line.split(':')[0]
                value = ':'.join(line.split(':')[1:]).strip()

                # If a label is present in the line but that label is already found in the baginfo dict,
                # it is a repeated field. Append to the existing dictionary entry, separated by a pipe
                if label in baginfoDict:
                    baginfoDict[label] = baginfoDict[label] + ' | ' + value
                    
                # If the label is not yet in the baginfo dict, create a new dict entry with the label and value
                elif not label in baginfoDict:
                    baginfoDict[label] = value
                    # If a label is present but the associated key already has a value in the dictionary, join with a pipe    

                        
            # If a label is not present, the line should be a continuation of the previous line. Append to the existing value
            else:
                value = line
                try:
                    baginfoDict[label] = baginfoDict[label] + ' ' + value
                except UnboundLocalError:
                    sys.exit('Error: bag-info line "' + value + '" does not meet required bagging specifications')
                    
# Bag the user-supplied directory in place. Create a UUID External-Identifier
def bagCreator(bagPath):
    """
    bagUUID = str(uuid.uuid4())
    # Add the UUID External-Identifier to the bag-info dictionary. If other
    # External-Identifier values are present, insert the UUID first.
    if not baginfoDict['External-Identifier'] == None:
        baginfoDict['External-Identifier'] = bagUUID + ' | ' + baginfoDict['External-Identifier']
    else:
        baginfoDict['External-Identifier'] = bagUUID
    """
    # Calculate the bag size
    baginfoDict['Bag-Size'] = sizeCalculator(bagPath)
    
    for key in fieldsDict.keys():
        if fieldsDict[key] == True:
            if not key in baginfoDict:
                sys.exit('Error: missing required bag-info field "' + key + '"')
    bag = bagit.make_bag(bagPath, baginfoDict, checksum=['sha256']) # Specify a sha256 hash algorithm
    print('Bag created: ' + bagPath)

# Calculate bag size and convert to the appropriate unit to improve readability
def sizeCalculator(bag):
    total = 0
    for root, dirs, files in os.walk(bag):
        for file in files:
            filepath = os.path.join(root, file)
            total += os.path.getsize(filepath)
    kbTotal = total / 1024
    mbTotal = total / 1048576
    gbTotal = total / 1073741824
    tbTotal = total / 1099511627776
    
    if tbTotal > 1:
        return(str(round(tbTotal, 1)) + ' TB')
    if gbTotal > 1:
        return(str(round(gbTotal, 1)) + ' GB')
    elif mbTotal > 1:
        return(str(round(mbTotal, 1)) + ' MB')
    elif kbTotal > 1:
        return(str(round(kbTotal, 1)) + ' KB')
    else:
        return(str(total) + ' bytes')
    
def bagUnpacker(bag):
    os.remove(os.path.join(bag, 'bag-info.txt'))
    os.remove(os.path.join(bag, 'bagit.txt'))
    try:
        os.remove(os.path.join(bag, 'manifest-sha256.txt'))
    except FileNotFoundError:
        os.remove(os.path.join(bag, 'manifest-md5.txt'))
    try:
        os.remove(os.path.join(bag, 'tagmanifest-sha256.txt'))
    except FileNotFoundError:
        os.remove(os.path.join(bag, 'tagmanifest-md5.txt'))
    dataPath = os.path.join(bag,'data')
    for item in os.listdir(dataPath):
        if not item == 'data':
            shutil.move(os.path.join(dataPath, item), bag)
        elif item == 'data':
            # Move any items named "data" and give them a temporary name before 
            # removing "dataPath" and renaming the temporary item "data"
            origPath = os.path.join(dataPath, item)
            tempPath = os.path.join(bag, (item + '_temp'))
            os.rename(origPath, tempPath)
    os.rmdir(dataPath)
    try:
        os.rename(tempPath, dataPath)
    except:
        next
    print('Unpacked: ' + bag)
    
if args.u:
    try:
        print("WARNING: This will unpack all the bag at " + bagPath + ", moving the contents of the data directory up one level and deleting the bag-info, bagit, manifest, and tagmanifest files.") 
        print("This will INVALIDATE the bag. Do not proceed if you are not absolutely certain that this is what you want to do!") 
        input("Press Enter to continue, or CTRL+C to abort...")
    except KeyboardInterrupt:
        sys.exit('\nScript aborted by user.')
    bagUnpacker(bagPath)
    
else:
    bagInfoReader(bagInfo)
    bagCreator(bagPath)
