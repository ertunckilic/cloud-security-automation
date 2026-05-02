# OverTheWire Bandit Solutions

## Level 0 - 1
- Command: `cat readme`
- Password for Level 1: ZjLjTmM6FvvyRnrb2rfNWOZOTa6ip5If

## Level 1 - 2
- Command: `cat ./-`
- Password for Level 2: 263JGJPfgU6LtdEvgfWU1XP5yac29mFx

## Level 2 - 3
- Command: `cat "spaces in this filename"`
- Password for Level 3: MNk8KNH3Usiio41PRUEoDFPqfxLPlSmx

## Level 3 - 4
- Command: `ls -la` then `cat [hidden-file]`
- Password for Level 4: 2WmrDFRmJIq3IPxneAaMGhap0pFhF3NJ

## Level 4 - 5
- Command: `file ./*` then `cat [text-file]`
- Password for Level 5: 4oQYVPkxZOOEOO5pTW81FB8j8lxXGUQw

## Learnings
- Always use `ls -la` to see hidden files (start with .)
- Use quotes for filenames with spaces
- Use `./` prefix for weird filenames like `-`
- Use `file` command to identify file types
## Level 5 - 6
- Command: `find . -type f -size 1033c`
- Concept: Find files by size attribute
- Password for Level 6: DccwKySJqB1R58vXrWvZohQrvsFX337lm

## Level 6 - 7
- Command: `find / -user bandit7 -group bandit6 -size 33c 2>/dev/null`
- Concept: Find files by owner, group, and size
- Password for Level 7: cvX2JJa4CFALtqS87jk27qwqGhBM9plV

## Level 7 - 8
- Command: `grep "millionth" data.txt`
- Concept: Search for text patterns in files
- Password for Level 8: UsvVyFSfZccR06b6PArJ8P27zrQH3sCj

## Level 8 - 9
- Command: `sort data.txt | uniq -u`
- Concept: Sort and find unique lines
- Password for Level 9: NvEJF7oWe4enljYj0w7MfgkbD4NyScsj

## Level 9 - 10
- Command: `strings data.txt | grep "==="`
- Concept: Extract printable strings and search
- Password for Level 10: truKLdjsbJ5g7yyJ2X2R0O9T5Yj5YKNJ

## Advanced Learnings (Levels 6-10)
- `find` command is powerful: find by size, owner, permissions, name
- `grep` searches for text patterns
- `sort | uniq -u` finds unique lines
- `strings` extracts printable characters from binary files
- Always use `2>/dev/null` to suppress error messages
## Level 5 - 6
- Command: `find . -type f -size 1033c`
- Concept: Find files by size attribute
- Password for Level 6: DccwKySJqB1R58vXrWvZohQrvsFX337lm

## Level 6 - 7
- Command: `find / -user bandit7 -group bandit6 -size 33c 2>/dev/null`
- Concept: Find files by owner, group, and size
- Password for Level 7: cvX2JJa4CFALtqS87jk27qwqGhBM9plV

## Level 7 - 8
- Command: `grep "millionth" data.txt`
- Concept: Search for text patterns in files
- Password for Level 8: UsvVyFSfZccR06b6PArJ8P27zrQH3sCj

## Level 8 - 9
- Command: `sort data.txt | uniq -u`
- Concept: Sort and find unique lines
- Password for Level 9: NvEJF7oWe4enljYj0w7MfgkbD4NyScsj

## Level 9 - 10
- Command: `strings data.txt | grep "==="`
- Concept: Extract printable strings and search
- Password for Level 10: truKLdjsbJ5g7yyJ2X2R0O9T5Yj5YKNJ

## Advanced Learnings (Levels 6-10)
- `find` command is powerful: find by size, owner, permissions, name
- `grep` searches for text patterns
- `sort | uniq -u` finds unique lines
- `strings` extracts printable characters from binary files
- Always use `2>/dev/null` to suppress error messages
