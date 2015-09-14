# A Program for viewing a dll's import section on Windows
import pefile

target_file = raw_input("The file you wish to inspect: ")

pe = pefile.PE(target_file)
print "*************************************"
print "***********IMPORT TABLE**************"
for entry in pe.DIRECTORY_ENTRY_IMPORT:
  print entry.dll							# Print each DDL on the import table
  for imp in entry.imports:
    print '\t', hex(imp.address), imp.name  # Print each imported function and its address
print "*************************************"
