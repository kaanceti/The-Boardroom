# The Boardroom

[![tests](https://github.com/kaanceti/The-Boardroom/actions/workflows/tests.yml/badge.svg)](https://github.com/kaanceti/The-Boardroom/actions/workflows/tests.yml)

An AI advisory board that runs on your own Claude subscription. Four members with different
specialities answer your question on their own, review each other anonymously, and a Chair
makes the final decision and, when it matters, gives you honest criticism.

Inspired by Andrej Karpathy's [llm-council](https://github.com/karpathy/llm-council).

## Why it exists

AI tells people what they want to hear. A Stanford study published in *Science* in March 2026
found that AI chatbots affirmed people's actions 49% more often than other humans did, even when
the person was in the wrong. The Boardroom is built to push back:

- Four members answer on their own, and two of them are deliberately extreme (one cautious, one
  bold), so the board cannot drift into a comfortable consensus.
- Every member is told to spot the answer you are hoping for and judge your idea as if you wanted
  the opposite.
- They cross-examine each other without names, and the Chair overrules weak arguments.
- Every resolution is stamped: agreed with you, partly agreed, or disagreed. The app keeps a running
  pushback rate, so you can see how often it tells you no.

**Try it in your browser:** the [live demo](https://kaanceti.github.io/The-Boardroom/) replays three
saved meetings, no install needed.

| Seat | Speciality | Model |
| --- | --- | --- |
| Chair | Judgement and final decision | Opus |
| Skeptic | Risk and failure analysis | Opus |
| Advocate | Opportunity and upside | Haiku |
| Operator | Execution, numbers and timelines | Sonnet |
| Scout | Evidence and fact-checking (uses web search) | Sonnet |

**Three models, not one.** Five calls to the same model share the same training, so they tend to
think alike. The board mixes three Claude models, each matched to its job: Opus for the two seats
that need the deepest reasoning (the final judgement and hunting for risks), Sonnet for planning
and web research, and Haiku, the fastest, for the Advocate's bold ideas, which the Chair then
checks. You can switch any seat's model in the app.

## How a meeting works

1. **Statements.** Each member answers on their own, from their speciality.
2. **Cross-examination.** In a full meeting, each member reviews the others' answers without seeing names.
   Members tend to sign their work ("Skeptic's statement"), so names are taken out of the text first. Style
   can still give someone away (only the Scout cites links), but no name ever reaches a reviewer.
3. **Resolution.** The Chair decides, overrules weak points, lists next steps and stamps whether the
   board agreed with what you wanted.

## Files in and out

- **Attach files** to a meeting: PDF, Word, Excel (.xlsx or .xlsm), CSV, text or images, up to 5 files and 20 MB.
  The text of Word, Excel, CSV and text files goes straight to every member. PDFs and images are
  opened by each member with Claude Code's Read tool.
- **Get files back.** Ask for one ("put the forecast in a spreadsheet", "draft the plan as a
  document") and the Chair creates it: an Excel workbook for tables (bold header row, £ and %
  formats and live formulas, plus a CSV copy) or a Word document. Download it from the meeting page.
- **Minutes.** Every meeting can be downloaded as a Word or Markdown file.

Members can only read the files attached to their own meeting, and the Chair can only write into
that meeting's `outputs` folder. Everything is saved in `data/files/`, which git ignores. File
contents are treated as information, not instructions, but only attach documents you trust.

## Does a board beat one Claude?

I tested it. Fifteen everyday decisions (money, career, small business) were each answered two
ways, with the same model (Sonnet) and the same web tools:

- **Single:** one Claude call, asked for a decision, the main risks, honest criticism and next steps.
- **Board:** a full Boardroom meeting: four statements, four cross-examinations, then the Chair.

A separate Claude (Opus) compared each pair blind. It scored usefulness, accuracy, risk spotting
and clarity out of 10 and picked a winner. Each pair was judged twice with the order swapped, and
a win only counts when both orders agree. Member names and the word "board" were replaced with
neutral labels first.

![Blind test results](benchmark/results.png)

**Round 1 was a draw: 6 wins each, 3 ties.** The board was better at spotting risks (8.2 vs 7.2)
and slightly more accurate (7.5 vs 7.1), but far less clear (6.1 vs 8.4). The judge kept giving the
same reason: the Chair spent its answer narrating where the members agreed and disagreed, instead
of answering the person.

**Round 2: the board won 14, tied 1 and lost none.** I changed only the Chair's write-up, so it
reads on its own (decision, why, risks, criticism and next steps, then short "Board notes"), and
re-ran the Chair on the same 15 meetings. The members' statements were not touched.

| Average score out of 10 | Round 1 board | Round 1 single | Round 2 board | Round 2 single |
| --- | --- | --- | --- | --- |
| Usefulness | 7.5 | 7.6 | **8.4** | 7.2 |
| Accuracy | 7.5 | 7.1 | **7.6** | 6.9 |
| Risk spotting | 8.2 | 7.2 | **8.9** | 6.6 |
| Clarity | 6.1 | 8.4 | 7.1 | **8.1** |
| Wins out of 15 | 6 | 6 | **14** | 0 |

A board answer costs about 9 Claude calls and 55 seconds; a single answer costs 1 call and 10 seconds.

Limits, honestly:

- The judge is an AI from the same model family, not a panel of people.
- Fifteen questions is a small sample, and round 2 reused the questions that exposed the flaw, so it
  may flatter the fix. A fresh set of questions is the proper next test.
- Board answers are longer (550 vs 450 words) and AI judges can favour length. They were also longer
  in round 1 (527 words), when the board only drew.
- The judge was told not to mark an answer down for mentioning analysts, because in the app you can
  read every member's statement.
- The single answers were identical in both rounds. Their scores moved because the judge scores each
  pair side by side.
- The test ran every seat on Sonnet, with the earlier, milder Skeptic and Advocate. The mixed models
  and the extreme members came later.

**Round 3 is running now.** Today's board (three models, extreme Skeptic and Advocate) against Claude
Opus on its own, on 15 new questions, with the same judge. The [plan](benchmark/round3/PLAN.md) was
written and committed before any answer existed, and the results go here whatever they show.

Every question, both answers and the judge's reasons: [`benchmark/all-answers.md`](benchmark/all-answers.md).
Method and scripts: [`benchmark/`](benchmark/).

## Personalities

Each member also has a temperament, borrowed from the classic four temperaments. That is an old
model of personality, not a scientific one, and here it is only a character brief: it shapes how a
member argues and what they notice, never the facts. The app does not show it. It lives in
`members.json` if you want to change it.

| Seat | Temperament | What it adds |
| --- | --- | --- |
| Skeptic | Melancholic, **extreme** | The deliberate pessimist: argues the most cautious case, including doing nothing |
| Advocate | Sanguine, **extreme** | The deliberate optimist: argues the boldest case and the unusual move most advisers would not suggest |
| Operator | Choleric | Decisive and blunt; pushes for owners, dates and numbers |
| Scout | Phlegmatic | Calm and even-handed; reports the evidence without spin |
| Chair | Balanced | Weighs what the members say, not how they say it |

The idea: four calls to the same model tend to agree with each other, so different temperaments give
the Chair more distinct angles to weigh.

**Why two extremes.** Ask a model to pick a number from 1 to 10 and it usually says 7. So the
Skeptic and the Advocate first name "the usual answer", then argue for the far end of it, while the
Operator and Scout stay moderate. In a test meeting asking exactly that, the Operator and Scout both
said 7, the Skeptic said 1, the Advocate said 10, and the Chair settled on 4. The Chair is told to
test the middle against the extremes and only back one when the evidence supports it.

## Make it yours

Click a member's name to rename them (up to 10 letters) and pick a face from the five defaults or
nine more, including two cats. Their speciality and instructions stay the same. The board uses your
names everywhere, including in what it writes. Your choices are saved only in your browser, so
they never travel with the code.

**Punishment corner.** Drag a member who annoyed you into the corner at the end of the room. They
turn their chair to the wall, sit out the next meeting and mutter while the others talk. Drag them
back whenever you like, or they come back on their own after sitting out one meeting. The app asks
why you cornered them ("too long", "wrong facts" or your own words), and their last three reasons
go with them into future meetings so they adjust. The corner also shows who you send there most.

**The room.** Every time you open the app, the board walks in through the door one by one, the
Chair last (click to skip). An office cat sleeps in its bed and wanders over now and then; click it
to pet it. Members react with little emotes while they argue, and the Chair bangs a gavel when it
decides. Click Decorate to change the wall colour, or turn on calm mode to skip the entrance and let
the cat sleep.

To add faces of your own, for example of friends, put them in `my_faces.json` next to
`boardroom.py`. Each face is 16 rows of 16 characters plus a colour for each character (see
`EXTRA_FACES` in `static/index.html` for examples). The file is ignored by git, so it stays on
your computer.

## The office cat

The cat asleep in the corner runs its own language model. It is not Claude and uses none of your
plan. It is a tiny transformer, the same basic design as large language models, with about 1.2 million
numbers instead of billions. It is written from scratch with only NumPy in `cat/tinycat.py`, and
the same maths runs in your browser from `cat/tinycat.js`, so the cat talks without a server call.

- **It learns how to talk** from about 2,400 original lines in `cat/teacher/`: lazy, food-obsessed,
  a bit dim, and quietly judging the board. Sentences from public-domain books give it more words.
- **It learns what to talk about** from your meetings. After each meeting it practises for a few
  minutes in the background, at low priority, so it picks up your topics and some of the board's
  words. You can also double-click `teach-cat.bat`.
- **Click it** to open Kibi's notebook: pet it, talk to it, rename it and see what it has learned.
  The Thoughts page keeps everything it has said, and the Wishes page has one wish a day, written by its
  own brain, for you to grant. After the Chair decides, it has a word about the topic too.
- **It answers what you say.** It reads your whole message, and has practised on about 300 ways people
  talk to chatbots and pets, from "are you real?" to "get off the keyboard". If a message sounds like
  someone is having a hard time, it skips the jokes and gives a kind reply written by hand that points
  to real people and helplines.
- **It only writes real words.** A brain this small likes to half-invent words ("the bake saleep"). As it
  writes, each letter must keep the word on its way to one it has read in its lessons, or one in your
  message, so its words are always real even when its sentences are silly.
- **Its body follows its words.** When it writes a move between stars, like `*stretches*`,
  `*licks paw*` or `*knocks pen off table*`, it acts it out. It decides when, because it wrote it.
- **It is a toy, not an adviser.** Before it learns anything, `cat/safety.py` leaves out anything
  that sounds like advice, violence, and swearing.
- **It makes everything up.** Kibi knows nothing about the world. Ask it about a person, a company or
  the news and it strings together words from its cat lines, so whatever it says is invented nonsense,
  not a fact and not anyone's opinion, least of all the author's.
- **Your cat stays yours.** Its brain is saved in `data/cat/` next to your meetings and is never
  published. The repo ships `cat/starter-brain.npz`, trained only on the teacher lines, everyday
  topics and the books, so a fresh copy has a cat that can already talk.

A small brain makes a small cat: expect cheerful, remixed nonsense, not wisdom.

## Run it

- **Windows:** double-click `setup.bat` once (installs Claude Code and signs you in), then `start.bat`.
- **Mac or Linux:** install [Claude Code](https://docs.claude.com/en/docs/claude-code) and [uv](https://docs.astral.sh/uv/),
  run `claude` once to sign in, then `uv run --no-project boardroom.py` and open http://localhost:8765.

Each member is a separate `claude -p` call, so a meeting uses your Claude plan's allowance instead
of paid API credit. A full meeting is about 9 calls; a quick meeting is about 5. It is built for
personal use with your own account.

To run one meeting in a terminal: `uv run --no-project boardroom.py ask "your question" --file report.pdf`
(`--file` is optional and can be repeated).

## Files

- `boardroom.py`: the local web server and the meeting logic (Python standard library only).
- `office.py`: reads Word and Excel files and writes Word and Excel files, also with the standard library only.
- `members.json`: the seats, their instructions, the model and `owner_location` (set to where you live, so advice uses your laws and currency). Edit it to change the board.
- `static/index.html`: the pixel-art boardroom. The character sprites are original.
- `cat/`: the office cat's own tiny language model (`tinycat.py`, `tinycat.js`), its starter lines, the training text builder and the starter brain.
- `teach-cat.bat`: makes the cat practise on your meetings now, instead of waiting for the next one.
- `tests/`: runs a whole meeting against a fake Claude (so it costs nothing) and checks the reviews are blind, the
  cat's maths against a slow numerical check, that the browser cat and the Python cat write the same lines, that
  it only writes real words, and the Word and Excel files. Run them with `python -m unittest discover tests`.
- `my_faces.json` (optional): your own faces. Private, and ignored by git.
- `data/files/`: files you attached and files the board made, one folder per meeting. Private, and ignored by git.
- `data/meetings/`: your meetings as JSON plus readable Markdown minutes. Private, and ignored by git.
- `data/cat/`: your cat's brain and what it has learned from. Private, and ignored by git.
