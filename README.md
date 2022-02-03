# pybagger
Bag a directory, supplying an existing txt file for the bag-info.txt output

This replicates the functionality of bagit-java, which has been superseded by bagit-python. bagit-java allowed users to provide a bag-info.txt file that would be included in the resulting bag (with Bag-Size, Bagging-Date, Bag-Software-Agent, and Payload-Oxum fields added during the bagging process). The newer bagit.py requires that the bag-info information be stored as a dictionary and does not accept a text file. This script reads a text file and structures its contents into a dictionary that bagit.py can output as a new bag-info.txt file. bagit.py sorts the output bag-info.txt file alphabetically by dictionary key (i.e. field) name, so the resulting bag-info.txt file may be a different order than the user-supplied text file.

The script matches the contents of the input text file against a set of allowed fields declared at the top of the script in the <code>fieldsDict</code> dictionary. The default set of allowed fields are based on the University of Texas Libraries' local bag-info specification, but this dictionary can be edited to match other specifications as needed.

Because bagit.py does not output an easy-to-read bag size apart from the Payload-Oxum, this script calculates the bag size and outputs the appropriate value and unit (TB, GB, MB, KB, or bytes).

Default usage:

<code>pybagger.py --baginfo <path_to_baginfo_txt_file></code>

By default, all allowed fields identified in the <code>fieldsDict</code> dictionary are required. Fields can be made optional by changing their dictionary value to <code>False</code>.
  
By default, the script bags the current working directory. To bag a different directory, use the <code>-d --directory</code> switch, followed by the path to that directory:
 
<code>pybagger.py --baginfo <path_to_baginfo_txt_file> --directory <path_to_directory></code>

Use the <code>-u --unpack</code> switch to "unbag" a bag at the target directory:
  
  <code>pybagger.py -u -d <path_to_directory></code>
  
Because the unpack function will invalidate a bag at the target directory, the script displays a warning message and asks the user to confirm that they wish to proceed.
