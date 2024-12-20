## Goal
A program that parses journal entries, helps find tags & child blocks in journals and (will one day) move them to the actual page

## Trigger
[This reddit post](https://www.reddit.com/r/logseq/comments/1hhnwhs/logseq_and_what_happens_if_i_want_to_change_the/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button)

## Structure
- sample_workspace: A sample Logseq workspace
- script/logseq_tweaker.py: The script that does the work

## Execution
* Clone this repo locally
* Install dependencies
  * `pip install python-dotenv`
* Tweak the .env file appropriately (ex: specify the path to your workspace)
* Run `python ./script/logseq_tweaker.py`
  * The script will go through all the journals & get a list of unique `[[pages]]` or `#tags`
  * Then it searches the pages folder for any references which don't exist as files
* The output is written to the file `logseq_tweaker_output.md` in your workspace

## Features/Roadmap
_Add any you'd like to see as issues_

- [x] Find all references in journals
- [x] List all references which don't exist as files 
- [x] List all references which have sub-blocks directly in a journal
- [ ] Add a user prompt to confirm & if the user approves, move the blocks from the journal to the page
- [ ] Handle sub-folders and namespaces

## Misc
I wanted to also experiment with python - a language I'm not familiar with so most of the code was generated using ChatGPT & CoPilot on VS Code
* [Prompt log 1](https://chatgpt.com/share/6764dcd0-7d58-800e-b2ac-9cdc7636553c)
* [Prompt log 2](https://chatgpt.com/share/6764dcf8-49a4-800e-9e01-514a8e3e6be8)

## Unit tests
* Install pytest: `pip install pytest-html`
* Run all tests: `pytest --html=report.html`