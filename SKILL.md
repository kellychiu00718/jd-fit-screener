---
name: jd-fit-screener
description: Reads job postings (pasted text, local files or public URLs) and scores how well each one fits the user's own profile by what the posting actually asks for, not by the job title. Keeps fit and priority separate and returns a short ranked list with evidence and gaps. Use when the user shares one or more job postings, or asks "which of these jobs fit me", "screen these postings", "rank these JDs", or "is this role a good fit".
---

# JD fit screener

Goal: help a job seeker decide which postings deserve their time. The person makes the final decision. Never apply, send messages or edit documents without being asked.

## Before you start
1. **Find the profile.** Look for `profile.md` in the current folder, then `~/.jd-fit/profile.md`. If there is none, build one with the user from `references/profile-template.md`. Ask only for what is missing. Do not invent skills, numbers or experience. A profile entry needs evidence (what the user did, with a number or an output if they have one).
2. **Collect the postings.** Accept pasted text, local files and public URLs. For URLs, use whatever web-reading tool is available. If a page needs a login, shows a bot check or cannot be read, ask the user to paste the text. Do not try to get around logins or bot checks.
3. **Set the list size.** Default to a shortlist of 10. Ask if the user wants a different number.

## Steps
1. **Merge duplicates.** The same company and the same title on several sites is one posting. Keep the version with the fullest description and note the other sources.
2. **Prefilter when there are more than 20 postings.** Run `scripts/prefilter.py` (standard library only) with the keyword lists from the profile. It ranks postings by keyword hits and drops the ones with negative keywords. Treat its output as a cheap first cut, not a verdict. Say how many postings it dropped.
3. **Score each remaining posting** with `references/scoring-rubric.md`:
   - Judge the responsibilities and requirements in the posting, not the title. Similar work hides under different titles, and similar titles hide different work.
   - For every score, quote one line from the posting and one line from the profile that support it.
   - Check the hard gates (location, work authorization, language, hard experience requirement). Mark each as pass, fail or unknown. Do not guess an unknown gate.
4. **Rank by priority separately.** Priority uses freshness and the user's stated preferences (for example company type). These only order postings with similar fit. They never change the fit score.
5. **Report** in the format below.

## Output format
1. A table of the shortlist: rank, company, title, fit score (0 to 100), gates, one-line reason, biggest gap.
2. For the top three: what in the posting matches the profile (with the quoted lines), what is missing, and one question to ask the employer.
3. A short list of postings that were dropped and why (gate failed, negative keyword, low fit).
4. Offer a next step, such as tailoring the resume for one posting. Do not start it unprompted.

## Rules
- Do not claim the user has a skill or result that is not in the profile. If a requirement is not covered, say it is a gap.
- If the posting is thin, lower the confidence and say so. Do not fill in details from the company's reputation.
- Report scores as judgement, not measurement. A score of 72 versus 75 means nothing; say that the bands in the rubric are what matter.
- Keep the user's profile and the postings private. Do not paste them into other tools or services.
- Dates, salary and visa terms: report what the posting says. If it does not say, write "not stated".
