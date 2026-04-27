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
