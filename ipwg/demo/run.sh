#!/usr/bin/env bash

set -eux

# copy the notebook to the execution directory so that it can be updated by quarto
cp $bin/ipwg/a.qmd .


# fetch parameters
params=""
for p in "${@}"; do
    params="$params -P $p"
done



# Run and render the notebook
#quarto render main.ipynb -o output.html --execute $params
#jupytext a.py --to qmd
quarto render a.qmd -o output.html | cat

# create an iframe for the IPOL page
viewer_url="https://ipolcore.ipol.im/api/core/shared_folder/run/${IPOL_DEMOID}/${IPOL_KEY}/output.html"
cat >>algo_info.txt <<EOF
url=<iframe src="$viewer_url" onload='javascript:(function(o){o.style.height=o.contentWindow.document.body.scrollHeight+"px";}(this));' style='width:100%;border:none;overflow:hidden;'></iframe>
EOF
