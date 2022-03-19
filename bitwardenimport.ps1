$BW_SESSION=$(bw login <email> <password> --raw)

bw import bitwardencsv bwimport.csv --organizationid <organizationID> --session $BW_SESSION --quiet

bw logout --quiet
