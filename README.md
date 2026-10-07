# JD Fit Screener

**A Claude skill that tells you which job postings actually fit you, by reading what the posting asks for instead of the job title.**

Give it a profile and a pile of postings. It returns a short ranked list with the reason for each score, the biggest gap, and which postings you should not spend time on.

## Background
I apply to many roles at once. For each one I had to read the JD, compare it with my experience, and rewrite my resume. That took several hours per posting.

Job titles did not help. The same work appears as "Solutions Consultant", "Customer Success" or "Business Analyst". I also noticed that liking a company can quietly look like a better skill match.

I wanted a systematic way to judge how well my experience fits a position. So I built this skill.

## What it does
- Reads a posting from pasted text, a file or a public URL. It judges the real responsibilities and requirements, not the title.
- Compares them with your profile. Every profile entry needs evidence.
- Scores the fit from 0 to 100, with one line quoted from the posting and one from your profile. Missing information is marked "not stated", not filled in.
- Checks hard gates: location, work authorization, language and required experience. Each is pass, fail or unknown.
- Names the biggest gap for each posting.
- Merges duplicate postings, and prefilters long lists by keyword.
- Orders postings of similar fit by freshness and your preferences. This never changes the score.
- For the top three, shows what matches, what is missing, and one question to ask the employer.
- Lists the postings it dropped, with the reason.

## Install
Claude Code reads skills from `~/.claude/skills/`.

```bash
git clone https://github.com/kellychiu00718/jd-fit-screener ~/.claude/skills/jd-fit-screener
```

For one project only, put the folder in `<your project>/.claude/skills/` instead.

## Use
1. Copy `references/profile-template.md` to `profile.md` in your working folder and fill it in, or let the skill interview you.
2. Paste postings, point it at files, or give public URLs:
   - "Screen these three postings against my profile."
   - "Rank the postings in `jobs/` and give me the top 5."
   - "Is this role a good fit? <paste posting>"
3. For long lists (more than 20), the skill can run a keyword prefilter first:
   ```bash
   python3 scripts/prefilter.py jobs/ --profile profile.md
   ```
   It uses only the Python standard library.

See `examples/` for a fictional profile, three fictional postings and a sample report.

## What is inside
```text
SKILL.md                      the instructions Claude follows
references/scoring-rubric.md  how fit is scored (0 to 100) and how gates work
references/profile-template.md what to put in your profile
scripts/prefilter.py          optional keyword prefilter and duplicate merge
examples/                     fictional profile, postings and sample output
```

## What it does not do
- It does not scrape job sites, log in for you, or get around bot checks. If a page cannot be read, you paste the text.
- It does not apply, send messages or edit your resume unless you ask.
- It cannot know whether a posting is still open or what the employer really wants. Treat the score as a way to order your reading, not as a prediction of an interview.

## Limits
- Scores come from a language model's judgement against a written rubric. Compare it with your own view on five or six postings you already know before you rely on it.
- The result is only as good as your profile. If you list a skill you do not have, the skill will score you as if you do.

## Results
Reading a JD and finishing my resume used to take several hours. Now it takes under 30 minutes. I timed it myself.

The skill makes that possible through the steps listed in "What it does". It tells me what matches, what is missing and which gap is biggest, so I know which experience to put first.

Nobody else has used it yet.

## Challenges & learnings
- Separating fit from priority took the most thought. My first design added company preference to the score, which made a preferred employer look like a better skill match.
- Removing the scrapers and API keys from my own tool left the part that other people can actually use: the judgment logic.

## About this project
I took the scoring logic from my own job-matching tool and turned it into a skill anyone can use: the rubric, the profile template, the rules about evidence and gates, and the examples. I used Claude Code to help write the skill files and the script. It has not been tested by other users yet.

## Origin
Distilled from the scoring logic of my own daily job-matching tool, [korea-job-matcher](https://github.com/kellychiu00718/korea-job-matcher), which collects postings from Korean job boards. This skill keeps the part that is useful to anyone and drops the scrapers, API keys and scheduling.

## License
MIT. See `LICENSE`.
