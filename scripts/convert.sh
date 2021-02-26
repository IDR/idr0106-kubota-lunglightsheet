#/bin/bash

# Converts the tiff file to ome.tiffs
# Run with:
# find /uod/idr/filesets/idr0106-kubota-lunglightsheet/20210217-ftp/* -type f -iname "*.tiff" -exec ./convert.sh {} \;

in_file=$1
tmpdir=tmp

in_filename=${in_file##*/}
out_filename=${in_filename%.*}.ome.tiff

echo "$in_filename -> $out_filename"
bioformats2raw-0.2.6/bin/bioformats2raw "$in_file" "$tmpdir"
raw2ometiff-0.2.8/bin/raw2ometiff $tmpdir "$out_filename"
rm -rf $tmpdir
