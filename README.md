# pybagger
Bag a directory, optionally supplying an existing txt file for the bag-info.txt output:

<code>pybagger.py <path_to_directory></code>

This replicates the functionality of bagit-java, which has been superseded by bagit-python. bagit-java allowed users to provide a bag-info.txt file that would be included in the resulting bag (with Bag-Size, Bagging-Date, Bag-Software-Agent, and Payload-Oxum fields added during the bagging process). The newer bagit.py requires that the bag-info information be stored as a dictionary and does not accept a text file. This script allows the user to supply a text file which the script reads and structures into a dictionary that bagit.py can output as a new bag-info.txt file. bagit.py sorts the output bag-info.txt file alphabetically by dictionary key (i.e. field) name, so the resulting bag-info.txt file may be a different order than the user-supplied text file.

The script matches the contents of the input text file against a set of allowed fields declared at the top of the script in the <code>fieldsDict</code> dictionary. The default set of allowed fields are based on the list found in Section 2.2.2 "Bag Metadata" bag-info.txt of the following BagIt specification document: https://www.digitalpreservation.gov/documents/bagitspec.pdf. The dictionary can be edited to match other specifications as needed.

Because bagit.py does not output an easy-to-read bag size apart from the Payload-Oxum, this script calculates the bag size and outputs the appropriate value and unit (TB, GB, MB, KB, or bytes).

Use <code>-d/--description'</code>, followed by a doublequote-enclosed text string, to add descriptive info to the <code>External-Description</code> field of the bag-info.txt file:
	
	<code>pybagger.py --description "Description of the contents of the bag" <path_to_directory></code>

Use <code>-b/--baginfo</code>, followed by the path to a text file, to bag a directory and use that text file as the basis for the resulting bag's bag-info.txt file:

	<code>pybagger.py --baginfo <path_to_baginfo_txt_file> <path_to_directory></code>

By default, the script inserts values used by the Carleton College Archives for <code>Source-Organization</code>, <code>Contact-Name</code>, and <code>Contact-Email</code> fields. The name of the bag is used as the <code>External-Identifier</code> field.

By default, no fields identified in the <code>fieldsDict</code> dictionary are required, apart from the <code>Bag-Size</code> field whose value is calculated as part of the script. Fields can be made required by changing their dictionary value to <code>True</code>.

Use the <code>-v/--validate</code> switch to validate a bag immediately after it has been created:

	<code>pybagger.py <path_to_directory_> --validate

Use the <code>-u/--unpack</code> switch to "unbag" a bag at the target directory:
  
  <code>pybagger.py -u <path_to_directory></code>
  
Because the unpack function will invalidate a bag at the target directory, the script displays a warning message and asks the user to confirm that they wish to proceed.