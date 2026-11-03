# Round 3 plan

Written on 1 November 2026, before any answer in this round existed. The results go in the main README whatever
they show, including if the board loses.

## Why a round 3

- Round 2 reused the 15 questions that exposed the Chair's flaw, so it may flatter the fix.
- The board has changed since then: three Claude models instead of one, and an extreme Skeptic and Advocate. That
  board has never been tested.
- Two seats now run on Opus, so beating Sonnet on its own proves less than it did. The fair opponent is Opus on its own.

## What is tested

- **Questions:** 15 new everyday decisions in [`questions.json`](questions.json) (money, work, small business and
  everyday life), written for this round and not used to change anything in the app.
- **The board:** a full meeting exactly as the app runs it: four statements, four anonymous cross-examinations, then
  the Chair. Seats as in `members.json`: Chair Opus, Skeptic Opus, Advocate Haiku, Operator Sonnet and Scout Sonnet
  (with web search).
- **Opus on its own:** one Claude Opus call with the same web tools (search and fetch), told where the owner lives as
  the board is, and given the same instructions, headings and 500-word limit as the single answers in rounds 1 and 2.
- **A frozen app:** `boardroom.py` and `members.json` do not change until judging ends. Their fingerprints for this
  run: boardroom.py `d653179507aa`, members.json `c168a9c6083c`. `run.py` saves the fingerprint with every answer,
  so a change mid-test would show.

## Restarted on 2 November 2026

The first attempt began with boardroom.py `00ab813fbfd2`. While checking the code for publishing, I found that the
cross-examination was not really blind: members signed their own statements ("Skeptic's statement: ..."), and in
the 12 meetings run so far 22 of the first 32 reviews named who wrote what. I stopped the run, fixed it (names are
now taken out of the statements before review, and members are asked not to sign), and started again from
question 1. The answers from the first attempt were set aside without being judged or read. The questions,
the judge and members.json did not change.

## How it is judged

The same judge as rounds 1 and 2, unchanged: Claude Opus scores usefulness, accuracy, risk spotting and clarity from
1 to 10 and picks a winner. Each pair is judged twice with the order swapped, and a win only counts when both orders
agree. Member names and the word "board" are replaced with neutral labels first.

## What will be reported

Wins, ties and losses, and the average scores, whatever they are. Every question, both answers and the judge's
reasons go in this folder.

## Known limits, stated in advance

- The judge is an AI from the same family, and the same model as the single answer. The board's final write-up is
  also written by Opus (the Chair), so both answers the judge compares come from Opus.
- Fifteen questions is a small sample, and each question is run once; a second run could come out differently.
- Board answers tend to be longer, and AI judges can favour length.

## Running it

Double-click `run-round3.bat` in this folder. It uses your own Claude plan: about 180 calls, 90 of them on Opus.
It saves after every question and stops by itself at a usage limit, so it can run over several sittings.
