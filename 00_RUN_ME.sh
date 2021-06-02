#!/bin/bash

set -e

if [ "$(whoami)" = "meren" ]
then
    # re-generate the pre-processed raw data from the raw raw survey outputs
    python 01_PRE_PROCESS_RAW_SURVEY_DATA.py

    # compile the output
    Rscript -e "rmarkdown::render('mentorship.Rmd')"

    sed 's/mentorship_files\/figure-gfm/{{images}}/g' mentorship.md \
                    | sed 's/!NOTICE! /{:.notice}\n/g' \
                    | sed 's/!WARNING! /{:.warning}\n/g'  > /Users/meren/github/merenlab.org/_includes/_mentorship_data.md

    mkdir -p /Users/meren/github/merenlab.org/images/mentorship-survey

    rm -rf /Users/meren/github/merenlab.org/images/mentorship-survey/*

    cp mentorship_files/figure-gfm/*png /Users/meren/github/merenlab.org/images/mentorship-survey/

    if test -f "mentorship_wisdom.md"; then
        cp mentorship_wisdom.md /Users/meren/github/merenlab.org/_includes/_mentorship_wisdom.md
    else
        echo
        echo "mentorship_wisdom.md does not exist. Probably you don't have the 'mentorship-RAW.tsv' in this directory :/"
    fi
else
    Rscript -e "rmarkdown::render('mentorship.Rmd')"

    echo
    echo "There must be some new files generated from the 'mentorship.Rmd' file in your work directory now."
fi
