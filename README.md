# zippy
A simple compression tool implemented from scratch as part of the [Build Your Own Compression Tool
](https://codingchallenges.fyi/challenges/challenge-huffman) challenge.

## Install
1. Clone the repository: ```git clone https://github.com/ravil-gasanov/zippy.git```
2. Use _uv_ to create a virtual environment (venv) and install the dependencies: ```uv sync```
3. Install the project as a package: ```uv pip install .```

## Use
1. Create or [download](https://www.dropbox.com/scl/fi/w227qldw9qnpgaw8a8u0k/challenge-huffman.zip?rlkey=biu7wnugjy9nziev8ejzogsm9&st=jxmfe3fs&dl=0) a text file, e.g. ```data/test.txt```
2. Compress the text file: ```uv run zippy -c -r "data/test.txt"```
3. Decompress: ```uv run zippy -d -r "data/test.txt.zippy"```


## Check
Compare the file sizes of the original, compressed, and the decompressed files. Is it:

```original == decompressed > compressed```?

Compare the contents of the original and decompressed file - are they identical?