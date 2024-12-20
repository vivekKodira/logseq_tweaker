## Trigger
[This reddit post](https://www.reddit.com/r/logseq/comments/1hhnwhs/logseq_and_what_happens_if_i_want_to_change_the/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button)

## Goal
A program that parses journal entries & finds tags that only exist in journals and (optionally) fixes them

## Structure
- sample_workspace: A sample Logseq workspace
- script/logseq_tweaker.py: The script that does the work

## Execution
* Run `python ./script/logseq_tweaker.py`
* The code will prompt you for the location of your workspace
* It will go through all the journals & get a list of unique `[[pages]]` or `#tags`
* Then it searches the pages folder for any files with that name

## Roadmap
_Will work on this when/if I find time_
* Tell the user about references which have sub-blocks (today it just lists all missing ones)
* Add a user prompt to confirm & if they approve, create the missing page, and move any blocks from the journal to the page
* Handle sub-folders and namespaces

## Misc
I wanted to also experiment with python - a language I'm not familiar with so most of the code was generated using ChatGPT
* [Prompt log 1](https://chatgpt.com/share/6764dcd0-7d58-800e-b2ac-9cdc7636553c)
* [Prompt log 2](https://chatgpt.com/share/6764dcf8-49a4-800e-9e01-514a8e3e6be8)