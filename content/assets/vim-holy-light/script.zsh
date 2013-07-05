while ((1)) {
    # set paths
    local hl="$HOME/.vim/bundle/holylight/bin/holylight-checker"
    local csv="data.csv"

    # create "{{ timestamp }},{{ value }}\n" CSV entry
    date '+%s,' | tr -d '\n' >> $csv
    $hl >> $csv

    # wait for it...
    sleep 5
}
