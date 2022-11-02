#!/bin/bash
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

echo "$parent_path"
pushd "$parent_path"

input="./nltk_dependencies.txt"
output="../resources/nltk_data"

for line in $( sed "s/\r$//" $input )
do
    echo "Downloading $line..."
    python -m nltk.downloader $line -d $output
done 

popd