# utils
Various utilities I've built but don't regularly maintain

# dm3_process

Quality-of-life scripts to convert negative-stain EM images from dm3 format to mrc format for processing in cryosparc/relion.  Starting from a directory containing the dm3 image files:
 - convert.sh will use dm2mrc to create mrc files for each image
 - convert2.sh will use proc2d to create full-res png image files for each image
 - thumbnail_prep.sh will transfer the png files to a new directory called "test"
 - thumbnail.py will create reasonably sized thumbnail images for each image in "test", and output them into the "test" subdirectory

# gb2fa

 - Convert genbank files to fasta files for plain-text (no annotations) storage of plasmid data
 - Hooray, documentation of your constructs has survived nuclear winter (even though your constructs probably didn't)

# json2bfactor

 - Convert AlphaFold2 json plDDT outputs into a text file formatted as B-factors for pymol import
