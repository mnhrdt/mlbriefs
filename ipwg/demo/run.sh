#!/usr/bin/env bash

set -eu

notebook_path=$bin/$1

# copy the notebook to the execution directory so that it can be updated by quarto
cp $notebook_path main.ipynb


### fetch parameters
# Always provide the working directory
params="-P SRCDIR:$(dirname $notebook_path)"
# Then add remaining parameters
# Start from the second argument: $1 is the notebook path
for p in "${@:2}"; do
    params="$params -P $p"
done



# Run and render the notebook
quarto render main.ipynb -o output.html --execute $params

# create an iframe for the IPOL page
viewer_url="https://ipolcore.ipol.im/api/core/shared_folder/run/${IPOL_DEMOID}/${IPOL_KEY}/output.html"
cat >>algo_info.txt <<EOF
url=<iframe src="$viewer_url" onload='javascript:(function(o){o.style.height=o.contentWindow.document.body.scrollHeight+"px";}(this));' style='width:100%;border:none;overflow:hidden;'></iframe>
EOF
