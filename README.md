# Markdown Table of Contents generator

[![Ruff](https://github.com/Electronic-Mango/markdown-toc-generator/actions/workflows/ruff.yml/badge.svg)](https://github.com/Electronic-Mango/markdown-toc-generator/actions/workflows/ruff.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/markdown-toc-generator)](https://pypi.org/project/markdown-toc-generator/)

Basic Markdown Table of Contents generator written in `Python`.

The script generates ToC in a form of a nested list based on headings in Markdown files.
The ToC can be printed to console, or inserted/updated into analyzed files.

> **Warning**: Inserting/updating ToC into the files can be destructive, as entire file is read, ToC is inserted/updated, then entire file is overwritten. The remaining contents of the file shouldn't be affected, but be careful.

The project is managed by [uv](https://docs.astral.sh/uv/).


## Usage

Package is available through PyPi - [`markdown-toc-generator`](https://pypi.org/project/markdown-toc-generator/).

You can install it directly:
```bash
pip install markdown-toc-generator
markdown-toc-generator --help
```

Run through isolated environment like uv, or pipx:
```bash
pipx run markdown-toc-generator --help
uvx markdown-toc-generator --help
```

Or download this repo and run the main script directly:
```bash
./src/markdown-toc-generator/toc.py --help
```


### Arguments

 * **`--root`, `-r`** - **required**, path in which files will be analyzed (recursively)
 * **`--exclude`, `-e`** - paths to files, or directories, which should be excluded from analysis
 * **`--in-place`, `-i`** - update analyzed files with generated ToC, **potentially destructive** and will request confirmation before any changes are done
 * **`--force`, `-f`** - skip confirmation for potentially destructive operations, like for `--in-place` flag
 * **`--skip`, `-s`** - skip *n* highest level headings from generated ToC
 * **`--take`, `-t`** - control how many headings are inserted into the ToC, starting from not-skipped by `--skip` - e.g. `--skip 1 --take 2` will include levels 2-4
 * **`--toc-regex`** - regex used for updating/inserting ToC into files when using `--in-place` flag
 * **`--summary`** - generate summary from all analyzed headings into one output - all ToCs with their respective files generated into one Markdown output
 * **`--summary-only`** - analyze all files, but print/write only the summary
 * **`--summary-path`** - write the generated summary to a file under passed path (`--in-place` flag is still required), **potentially very destructive** as the summary will overwrite everything in that file; this path is automatically excluded
 * **`--summary-heading`** - prefix added to the generated summary as the highest level heading


### ToC regular expression

The default regex used to insert ToC into the file itself is:
```
^(#[^#].+)$(\s*-.+\n)*\s*
```
It will look for the first heading available and treat the list right after it as the ToC to replace. So by default the script assumes, that file structure will be something like:

```markdown
# First heading in file (but doesn't have to be level 1)

- First element of ToC
  - First subelement of ToC
- Second element of ToC

Something else, not a list, which won't be modified.
The rest of the file doesn't matter.
```

These regexes should include two groups - first looks for the section right before the ToC (which won't be modified in the resulting file), the second looks for the ToC itself (which will be replaced).


### Summary

The generated summary will have a structure of:

```markdown
Summary heading as per `--summary-heading` flag, or "# Summary:" by default

## Link to directory with notes, text is the directory name

### Link to a note, text is taken from the heading level 1 from that note

- [Heading 2 name](link to file and section)
 - [Heading 3 name](link to file and section)
- [Heading 2 name](link to file and section)
```

And so on.

When flags `--in-place` and `--summary-path PATH_TO_FILE` are passed the resulting summary will be written to `PATH_TO_FILE` as is overwritting everything else in the file, so **it can be very destructive**.


### Examples

Generate ToC based on files in `notes/stuff` subdirectory, except for `README.md` and files under `ignore/notes`; ignore the highest level heading and include only 2 levels after that; only print to console, without summary:
```bash
./src/toc.py -r notes/stuff -e README.md ignore/notes -s 1 -t 2
```

The same as above, but print a summary as well, with `# Some stuff:` prefix:
```bash
./src/toc.py -r notes/stuff -e README.md ignore/notes -s 1 -t 2 --summary --summary-heading '# Some stuff:'
```

Insert ToC into files, print summary to console:
```bash
./src/toc.py -r notes/stuff -e README.md ignore/notes -s 1 -t 2 -i --summary --summary-heading '# Some stuff:'
```

Write summary to `README.md`:
```bash
./src/toc.py -r notes/stuff -e README.md ignore/notes -s 1 -t 2 -i --summary --summary-heading '# Some stuff:' --summary-path README.md
```
