# TODO

## postprocessing.sh ?

```bash
#!/bin/bash

# Post-process the speaker labels. $1 = transcript123.txt.
sed -i '' 's/SPEAKER_00/Host/g' $1
sed -i '' 's/SPEAKER_01/Guest/g' $1
```


## process-file.sh ?

```bash
#!/bin/bash

# Get the file name, without the path or extension.
FILENAME_ROOT=""

# Run transcribe_podcast.py on $1

# Wait forever

# Then run postprocessing.sh $1
```
