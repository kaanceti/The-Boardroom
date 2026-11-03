# Round 3 results: today's board against Claude Opus on its own

The [plan](PLAN.md) was written before any answer existed. Fifteen new questions, each answered by a full Boardroom meeting and by one Claude Opus call with the same web tools, then judged blind by Claude Opus, twice per question with the order swapped. A win only counts when both orders agree.

**Board 11, tie 4, Opus alone 0.**

| Average score out of 10 | Board | Opus alone |
| --- | --- | --- |
| Usefulness | **8.5** | 7.6 |
| Accuracy | 7.5 | 7.5 |
| Risk spotting | **8.9** | 7.5 |
| Clarity | 7.4 | **8.1** |

- **The ties.** In all 4 ties the judge picked whichever answer it read second, both times. That is a judge leaning on order, not a loss for either side, and it is why every pair is judged twice.
- **Cost.** A board answer took 9 Claude calls and 74 seconds on average; Opus alone took 1 call and 22 seconds.
- **Length.** Board answers averaged 670 words, Opus alone 573. Both ran over the 500-word limit they were given. AI judges can favour longer answers.
- **Where the board lost points.** Clarity, and in questions 2 and 8 (both ties) the judge marked it down for survey figures it could not verify. Both came from the Scout's web research and the Chair kept them.
- **The app did not change during the test.** Every answer carries the same fingerprint: boardroom.py `d653179507aa`, members.json `c168a9c6083c`.
- **Blind reviews.** No reviewer was shown a name. One of the 60 reviews guessed a member from their style ("Operator-style caution"). In the first attempt, before the fix, 22 of the first 32 reviews named who wrote what.
- **Incomplete meetings.** Ten meetings stopped when the Claude plan hit its session limit and were run again later. Only complete meetings count; the stopped ones are in [incomplete/](incomplete/).

Limits stated before the test: the judge is the same model as Opus alone and as the Chair, fifteen questions is a small sample, and each question was run once.

## Every question

| # | Question | Winner | Judge, board shown first | Judge, Opus shown first | Score (board vs Opus) |
| --- | --- | --- | --- | --- | --- |
| [1](#question-1) | I'm 29 with £8,000 on a credit card at 24% interest and £3,000 in… | Board | Board | Board | 8.0 vs 7.8 |
| [2](#question-2) | My partner and I earn very different salaries. Should we split shared… | Tie | Opus alone | Board | 8.1 vs 8.1 |
| [3](#question-3) | I'm self-employed and made £38,000 profit this year. Should I set up… | Board | Board | Board | 8.2 vs 7.6 |
| [4](#question-4) | Someone has offered me £25,000 for my small website, which earns… | Board | Board | Board | 8.2 vs 7.6 |
| [5](#question-5) | My manager has offered me a team lead role for £3,000 more, but I… | Board | Board | Board | 8.5 vs 7.8 |
| [6](#question-6) | My company wants everyone in the office four days a week instead of… | Board | Board | Board | 8.5 vs 7.8 |
| [7](#question-7) | I'm 35 and want to retrain as a primary school teacher, which means a… | Board | Board | Board | 7.9 vs 7.6 |
| [8](#question-8) | I have a job offer from another company. Should I tell my manager to… | Tie | Opus alone | Board | 7.9 vs 7.8 |
| [9](#question-9) | I sell handmade candles at weekend markets. Should I rent a small… | Board | Board | Board | 7.8 vs 7.5 |
| [10](#question-10) | My dog-walking business has a waiting list. Should I hire my first… | Tie | Opus alone | Board | 7.6 vs 7.9 |
| [11](#question-11) | I run a small online clothing shop. Should I start offering free… | Board | Board | Board | 8.2 vs 8.2 |
| [12](#question-12) | I'm a freelance designer. Should I raise my day rate from £300 to… | Tie | Opus alone | Board | 8.0 vs 8.1 |
| [13](#question-13) | Our family restaurant gets complaints about slow service on… | Board | Board | Board | 8.0 vs 7.0 |
| [14](#question-14) | Should I take a six-month unpaid career break to travel, using about… | Board | Board | Board | 7.6 vs 7.1 |
| [15](#question-15) | Should I buy an electric car now or wait two more years? | Board | Board | Board | 8.4 vs 7.4 |

## Question 1

**I'm 29 with £8,000 on a credit card at 24% interest and £3,000 in savings. Should I use my savings to pay off part of the card?**

| | Board | Opus alone |
| --- | --- | --- |
| Usefulness | 8.5 | 7.5 |
| Accuracy | 7.5 | 7.5 |
| Risk spotting | 8.5 | 8.0 |
| Clarity | 7.5 | 8.0 |
| **Winner** | Board | |

Judge, board shown first (A is the board): "Both give the same sound £2,000/£1,000 split, but A edges ahead with concrete payoff scenarios, the cash-withdrawal and 60–90 day transfer-window risks, and smart sequencing so the transfer fee falls on £6,000, though its interest figures run slightly low and B adds useful debt-help resources."

Judge, Opus shown first (A is Opus alone): "Both give the same sound plan, but B adds roughly correct payoff scenarios, sequences the £2,000 payment before the transfer so the fee falls on £6,000, and covers more transfer-deal pitfalls, while flagging its unverified figures."

<details>
<summary>Board answer (667 words)</summary>

#### Decision
Yes, use your savings on the card, but not all of them. Put £2,000 on the card now and keep £1,000 in cash as a buffer. Before then, use soft-search tools to check whether you could get a 0% balance transfer card for the rest. If you can, moving the balance to it is a bigger saving than anything you do with your savings.

#### Why
- The card charges 24%. Savings pay about 4% to 5%. Keeping £3,000 in savings while you owe on the card costs you about £600 a year.
- Here is how the amount you pay in changes things, assuming you pay £300 a month at 24% and spend nothing new on the card:
  - Pay in nothing: about 37 months to clear, about £3,000 interest.
  - Pay in £2,000: about 25 months, about £1,500 interest.
  - Pay in all £3,000: about 20 months, about £1,000 interest.
- That last £1,000 saves only about £500, and it leaves you with no cash at all. One car or boiler bill would then go back on the card at 24%, or cost even more as a cash withdrawal (often about 3% fee plus around 30% interest).
- A 0% transfer card usually charges a fee of about 3%. On £6,000 that is about £180. Paying the card at 24% instead costs over £1,000 in interest.

#### Main risks
- **Running the card back up.** This is the most likely way the plan fails. If the balance drops to £6,000 and then fills up again, you end up owing £8,000 with no savings.
- **Not getting a transfer card.** You may be refused, or offered a limit too low to move everything. You won't know until you check.
- **Breaking the 0% deal's terms.** One missed payment can cancel the 0% rate. Many deals also make you transfer within 60 to 90 days. Any balance left when the 0% period ends goes back to a high rate.
- **Using the card as your emergency fund.** The card company can cut your limit without warning. Cash you hold yourself is safer.

#### Honest criticism for the owner
You asked how to split your money, but the real question is why £8,000 built up on the card. If you regularly spend more than you earn, paying it down only treats the symptom and the card will fill up again within a year. Work out your actual monthly surplus. If it is under about £200, this is an income or spending problem, and no way of splitting your savings will fix it.

#### Next steps
1. **By 9 November:** Write down your monthly income, bills, and what you can really pay the card. Run soft-search eligibility checks for 0% balance transfer cards (MoneySavingExpert or a card provider's checker). These do not affect your credit file. Don't make full applications yet.
2. **By 16 November:** Pay £2,000 from savings onto the card. If a transfer looks likely, apply after that payment clears, so the fee is charged on about £6,000, not £8,000. Stop all new spending on the card.
3. **Set a direct debit for more than the minimum payment, for the day after payday.** Aim to clear the balance before any 0% period ends. Once the card is cleared, rebuild savings to £1,500 to £2,000 or more.

#### Board notes
- I overruled the Advocate's case for using all £3,000. The last £1,000 saves about £500, which doesn't justify having no cash. The Advocate's claim of about £1,200 a year in interest on the remaining £5,000 was also overstated. Because you'd be paying it down, the real figure is about £600.
- Still open: how big your buffer should be. £1,000 is thin. Standard advice is three months of essential costs. I accept it as a compromise only if your job is stable.
- Not checked: current transfer deal lengths and fees. The 34 to 38 month offers mentioned are unconfirmed. Check what's on offer today.

</details>

<details>
<summary>Opus alone (526 words)</summary>

#### Decision
Yes. Use £2,000 of your savings to pay down the card now, and keep £1,000 as an emergency buffer. Then move the remaining £6,000 to a 0% balance transfer card if you can get one. Paying all £3,000 would save a bit more, but it would leave you with no cushion at all.

#### Main risks
- **Losing your safety net.** If your boiler breaks or your income stops, you may end up back on the card at 24%. Your card provider can also cut your credit limit, so don't count on the card being there in an emergency.
- **The maths is not close.** £3,000 in an easy-access account at about 4% earns roughly £120 a year. I'm not sure of today's exact best rates, so check a comparison site. The same £3,000 on the card costs you about £720 a year in interest. Paying off £2,000 saves about £480 a year.
- **Balance transfer catches.** These cards usually charge a fee of about 3% to 4%, which is roughly £180 to £240 on £6,000. Their 0% periods have recently run up to about 2 years. I can't confirm what is on offer this month, and you may not be accepted. A missed payment can end the 0% rate.
- **Spending the money again.** If you clear part of the balance and then spend on the card again, you lose all the benefit.

#### Honest criticism for the owner
- You're asking about a one-off £3,000 move. The bigger question is your monthly plan for the whole £8,000. At 24%, the interest alone is around £160 a month. If you only pay the minimum, this debt could take well over a decade to clear.
- You haven't said how the £8,000 built up. If your monthly spending is more than your income, paying it down with savings only treats the symptom. The balance will creep back.
- Keeping £3,000 in savings while paying 24% feels safe, but it costs you about £50 a month. It's an expensive comfort blanket. Even so, £1,000 is still worth keeping.
- I don't know your income, job security, other debts or credit history. Any of these could change the advice. For example, if your job is at risk, I would keep more cash.

#### Next steps
1. **This week:** move £2,000 from savings to the card. Set up a direct debit for a fixed amount well above the minimum. Aim for £300 a month or more if your budget allows.
2. **Within 2 weeks:** use the soft-search eligibility checkers on MoneySavingExpert or a credit-reference site such as ClearScore. These don't harm your credit score. If you're likely to be accepted, apply for one balance transfer card. Then divide the balance by the number of 0% months and pay at least that much each month. For example, £6,000 over 24 months is £250 a month.
3. **This month:** write down a budget showing where your money goes each month. If you're struggling to keep up, get free help from StepChange or MoneyHelper before things get worse. Rebuild your savings to about £3,000 only once the card is cleared.

</details>

Full meeting: [statements and cross-examination](meetings/20261102-182531-17e2.md)

## Question 2

**My partner and I earn very different salaries. Should we split shared bills 50/50 or in proportion to our incomes?**

| | Board | Opus alone |
| --- | --- | --- |
| Usefulness | 8.5 | 8.0 |
| Accuracy | 7.5 | 8.0 |
| Risk spotting | 9.0 | 8.0 |
| Clarity | 7.5 | 8.5 |
| **Winner** | Tie | |

Judge, board shown first (A is the board): "Both recommend a proportional split based on take-home pay, and A covers more risks (joint liability, Scotland's section 28 time limit), but B's table uses verifiable 2026/27 figures, asks for the missing facts and adds practical steps like a declaration of trust and pension nominations, while A rests on an unverifiable YouGov statistic and ends with cluttered analyst notes."

Judge, Opus shown first (A is Opus alone): "Both give the same sound proportional-to-take-home recommendation with correct worked maths, but B covers more of the risks that matter (Scotland's section 28 claim and its one-year limit, joint liability on tenancies and loans, the leading English cases) and better scopes what the split covers, though its specific YouGov figures cannot be verified."

<details>
<summary>Board answer (677 words)</summary>

#### Decision
Split essential shared bills in proportion to your take-home pay, not gross pay and not 50/50. Pay them through one bills account that you each fund by standing order, and keep your own accounts for everything else. Before you settle the percentages, put in writing who owns the home and any deposit.

#### Why
- **The pay gap makes 50/50 lopsided.** Take a 2:1 gap: £4,000 and £2,000 take-home, with £2,400 of bills. At 50/50 the lower earner pays 60% of their pay and the higher earner pays 30%. Splitting by income makes it 40% each, which leaves the lower earner about £400 a month better off.
- **Take-home pay is the honest measure.** Gross pay hides tax bands, pension and student loan. On £60,000 and £30,000 salaries with £2,000 of bills, choosing gross or net moves about £46 a month.
- **The evidence is about opinions, not outcomes.** UK surveys show most people think splitting by income is fairer. YouGov in 2024 found 48% favour it and 37% favour equal splits. No study shows either method makes relationships last longer. That makes this a sensible default, not a proven answer.

#### Main risks
- **Who owns the property matters more than the split.** If you are not married, paying bills gives you no share in a home held in your partner's name. "Common law marriage" does not exist in the UK. In England and Wales, disputes over shares in a home end up in court; the leading cases are Stack v Dowden and Jones v Kernott. Scotland is different. There, a cohabitant can make a court claim under section 28 of the Family Law (Scotland) Act 2006, but only within one year of separating. I am unsure whether reform for unmarried couples in England and Wales has moved on, so check before relying on this.
- **Joint liability.** If you are both on a tenancy, council tax bill, overdraft or joint loan, each of you owes the full amount. Joint products can also link your credit files.
- **Life changes break a fixed formula.** A baby, part-time work or redundancy all change it. The partner who cuts their hours usually loses pension and earnings for good.
- **Arguments over what counts as "shared".** Not agreeing what the split covers causes more resentment than the percentage does.

#### Honest criticism for the owner
You have asked about the percentage, which is the smaller question. The costly mistakes are contributions nobody writes down: a deposit, mortgage payments on a home in one name, or a career break for childcare. If those are not recorded, the right split will not protect the lower earner.

#### Next steps
1. **This week, about 1 hour:** take both take-home figures from your latest payslips. List each essential bill (rent or mortgage, council tax, energy, broadband, food). Work out each share as your pay divided by combined pay, times total bills. Set up two standing orders into one bills account.
2. **Within 3 months:** write one page recording home ownership, deposits and what happens on job loss or separation. If you are unmarried and own property or have a joint tenancy, see a solicitor. The cost is likely in the hundreds to low thousands of pounds, but that is an estimate, so get two quotes.
3. **Review every 12 months**, or sooner if either income changes by more than 10% or either of you changes your hours.

#### Board notes
- I overruled Operator and Advocate on making equal personal money the default. As Skeptic showed, giving each of you the same spending money means pooling the whole surplus. That is a different system, so treat it as an option if you both want full pooling.
- Advocate wrote that cohabitants have no claim anywhere in the UK. That is wrong for Scotland. Skeptic's £60 figure for gross versus net is closer to £46.
- The idea that 50/50 is fine when salaries are within 10 to 15% of each other is a rule of thumb with no source behind it.

</details>

<details>
<summary>Opus alone (590 words)</summary>

#### Decision
Split shared bills in proportion to your take-home pay, not gross salary. Each of you keeps a set amount of personal spending money. Review the split once a year, or whenever either income changes by more than about 10%.

Here is a worked example. I don't know your real figures, so these are made up. The tax maths uses 2026/27 rates for England, with no pension contributions or student loan deductions.

- Partner A earns £60,000 gross, which is about £3,780 a month take-home.
- Partner B earns £30,000 gross, which is about £2,090 a month take-home.
- Shared bills are £2,000 a month.

| | A pays | B pays | A has left | B has left |
|---|---|---|---|---|
| 50/50 | £1,000 | £1,000 | £2,780 | £1,090 |
| Proportional (64/36) | £1,290 | £710 | £2,490 | £1,380 |

Under 50/50, the lower earner pays 48% of their pay on bills. The higher earner pays 26%. That gap usually turns into resentment.

#### Main risks
- **Property is the big one, not bills.** Unmarried couples in England and Wales have no "common law marriage" rights. If one of you puts in more of the deposit or mortgage capital and you split up, a court mostly looks at who legally owns what, not who paid the electricity. Paying bills proportionally can leave the lower earner with nothing if their name isn't on the deeds. Married couples and civil partners get far more protection on divorce.
- **Pensions drift apart.** A 64/36 bill split does nothing about the fact that one of you is building a much bigger pension. This gets worse if one partner cuts hours for children.
- **Unpaid work is ignored.** If the lower earner does more childcare or housework, even a proportional split may undervalue what they put in.
- **Scope arguments.** Is a takeaway a "shared bill"? What about holidays, or the car? Leave this vague and you will argue about it.

#### Honest criticism for the owner
- You've framed this as 50/50 versus proportional. The bigger question is what happens to savings, property and pensions. Bills are the easy part.
- You haven't said whether you are married, whether you own or rent, or whether you have or plan children. My advice changes a lot depending on those, especially the legal position.
- I don't know which of you earns more. If you're the higher earner hoping to justify 50/50: it's legal, but it means your partner subsidises a lifestyle set by your income. If you're the lower earner, push for proportional and get it agreed in writing.
- "Fair" is something you two agree on. It is not a formula. Some couples on very different incomes pool everything, and that works well too.

#### Next steps
1. **This week:** list every shared cost with its monthly amount. Agree which costs are in and which are out. Then work out each person's share from your actual take-home pay on your payslips.
2. **This month:** open a joint account just for bills. Set up standing orders from each of you on payday. Leave a buffer of about £200 in it.
3. **If you own or are buying property:** get a solicitor to draw up a declaration of trust recording who put in what. Expect to pay roughly £300 to £800, though I'm not sure of current fees. If you're unmarried, also think about a cohabitation agreement. And check you can each name the other on your pension nomination forms.

</details>

Full meeting: [statements and cross-examination](meetings/20261102-182714-6544.md)

## Question 3

**I'm self-employed and made £38,000 profit this year. Should I set up a limited company?**

| | Board | Opus alone |
| --- | --- | --- |
| Usefulness | 8.5 | 8.0 |
| Accuracy | 8.0 | 7.0 |
| Risk spotting | 9.0 | 7.0 |
| Clarity | 7.5 | 8.5 |
| **Winner** | Board | |

Judge, board shown first (A is the board): "Both reach the correct, well-calculated decision, but A covers the risks more fully (s455 charge, IR35, mortgage impact, filing fines) and is more careful about break-even, while B's £60,000 review trigger is unsupported on current rates even though it handles Making Tax Digital timing and rate uncertainty better."

Judge, Opus shown first (A is Opus alone): "Both get the core tax comparison right, but B covers more of the risks that matter (the s455 director's loan charge, IR35, late-filing fines, mortgage delays and payments on account) and avoids A's unsupported £60,000 trigger, though A usefully flags the £50,000 Making Tax Digital threshold that already applies."

<details>
<summary>Board answer (683 words)</summary>

#### Decision

Don't set up a limited company at £38,000 profit. If you take all the profit out to live on, a company costs about £1,200 a year more in tax. Add higher accountancy fees and you are roughly £2,000 to £2,700 a year worse off. Only look at it again if you can leave a set amount in the business every year, or a client or real liability risk demands it.

#### Why

These figures use 2026/27 rates for England, Wales and Northern Ireland, and assume this is your only income.
- **As a sole trader:** £5,086 income tax plus £1,526 Class 4 National Insurance (NI) comes to about £6,612. You keep about £31,390.
- **As a company paying you a £12,570 salary, with the rest as dividends:**
  - Employer NI: £1,136
  - Corporation tax: £4,616
  - Dividend tax at the new 10.75% rate: £2,062
  - Total: about £7,813. You keep about £30,190.
  - A £5,000 salary is worse, at about £8,276.
- **The old "incorporate at £30,000 to £40,000" rule is out of date.** Employer NI went up in April 2025 and dividend tax went up in April 2026.
- **Leaving profit in the company mostly delays tax rather than saving it.** Money taken out later costs about 27.7% in total (19% corporation tax, then 10.75% dividend tax on what is left). As a sole trader you pay 26%.
- **Pensions are the one real gain.** Company pension payments avoid corporation tax and NI. You can already get tax relief on pension payments as a sole trader, so the extra benefit is small. On £10,000 a year it is a few hundred pounds. That is our estimate.

#### Main risks

- **Paying more, not less.** This is the most likely outcome at your profit level.
- **Overdrawn director's loan.** If you take company money casually, as you can now, the company pays a 33.75% charge (section 455) on any amount not repaid within 9 months of the year end.
- **IR35.** If most of your work comes from one client who controls how you do it, working through a company can bring in these rules and wipe out any saving.
- **More admin and fines.** You would need payroll filings, company accounts, a corporation tax return and a £50 confirmation statement. Late-filing fines start at £150 at Companies House and £100 at HMRC.
- **Borrowing.** Mortgage lenders often want 2 years of company accounts, so switching can delay a mortgage. Limited liability is also weaker than it sounds: banks and landlords usually ask directors for personal guarantees.

#### Honest criticism for the owner

You are asking about a company structure before checking two things that matter more:
- **Is £38,000 your profit after expenses, and is it steady?** Your figures need to be right first.
- **Making Tax Digital.** It is based on turnover (your total sales), not profit. If your turnover is over £30,000, you will probably need to keep digital records and send quarterly updates from 6 April 2027. That is about 5 months away. Please confirm the date and threshold on gov.uk.

#### Next steps

1. **By 30 November 2026,** ask your accountant to compare three options in writing using your real figures: take everything out, keep £10,000 in the business, and pay £10,000 into a pension through the company.
2. **Now,** set aside about £550 a month for tax. Your payments on account are due on 31 January and 31 July.
3. **Before April 2027,** check your turnover against the Making Tax Digital threshold and choose compatible software.

#### Board notes

- I overruled the Advocate's correction of the £5,000 salary case. The Skeptic's £8,276 is right. The Advocate's figure leaves out the personal allowance that covers part of the dividends.
- I overruled the Operator's claim that a company starts to pay at £55,000. When all profit is taken out, it is still worse at that level. The break-even point is unclear, and may not exist at all on current rates.
- Still open: the exact pension advantage, and Scottish rates if you live in Scotland.

</details>

<details>
<summary>Opus alone (584 words)</summary>

#### Decision
No, not at £38,000 profit. Under 2026/27 rules, a limited company would leave you about £1,200 a year worse off in tax, and accountancy costs make it worse still. Stay a sole trader. Look at it again if your profit stays above about £60,000, or if a client insists on a company.

Rough figures for 2026/27:
- **Sole trader:** income tax £5,086 plus Class 4 National Insurance £1,526. Total about **£6,600**.
- **Limited company:** you pay yourself a £12,570 salary and take the rest as dividends. Employer National Insurance is about £1,136, corporation tax at 19% is about £4,616, and dividend tax at 10.75% is about £2,062. Total about **£7,800**.

The main reasons are the employer National Insurance rise to 15% (April 2025) and the dividend tax rise to 10.75% (April 2026). Every extra £1 of profit costs about 27.7p through a company and 26p as a sole trader. I worked these out by hand from rates I know as of mid-2026. I did not check them online today. The Budget in late November 2026 could change them.

#### Main risks
- **Higher running costs.** A company needs annual accounts, a corporation tax return, payroll and a Companies House confirmation statement (£50 a year). Accountants often charge £1,000 to £2,000 a year for this. A sole trader return usually costs a few hundred pounds.
- **Limited liability is weaker than it sounds.** Banks and landlords often ask directors for personal guarantees. Good business insurance may protect you more cheaply.
- **Getting money out is fiddly.** The company's money is not your money. Taking cash informally creates a director's loan, which can bring extra tax charges.
- **Hard to undo.** Closing a company later costs time and fees.

#### Honest criticism for the owner
- **You are basing this on one year.** If £38,000 was a good year, a company makes even less sense. If profit keeps growing, plan for that. Don't react to one figure.
- **"Limited company saves tax" is out of date.** That was true years ago. Tax rises since 2022 have removed most of the benefit at your income level.
- **You may be missing the deadline that actually matters.** Making Tax Digital for Income Tax is based on turnover, not profit. If your turnover was over £50,000 in 2024/25, you should already be filing quarterly since April 2026. If it is over £30,000, you will probably have to start from 6 April 2027. I am not sure what your turnover is, so check this.
- **If you don't need all the money, there are simpler options.** Personal pension contributions get tax relief as a sole trader too. Retaining profit in a company only helps if you leave it there for a long time.

#### Next steps
1. **Check Making Tax Digital this month.** Look up your turnover for 2024/25 and 2025/26. Then use HMRC's "Check if you need to sign up for Making Tax Digital" tool on GOV.UK. Choose compatible software before your start date.
2. **Get one accountant to check my numbers.** Ask for a sole trader versus limited company comparison using your real turnover, expenses and pension plans. Ask them to update it after the November 2026 Budget. It should be a one-off fee, typically £150 to £400.
3. **Set a trigger to look again.** Review when profit has been above about £60,000 for two years running, or when a client requires a limited company. Off-payroll working (IR35) rules then apply, and they need separate advice.

</details>

Full meeting: [statements and cross-examination](meetings/20261102-182900-12a1.md)

## Question 4

**Someone has offered me £25,000 for my small website, which earns about £800 a month. Should I sell it?**

| | Board | Opus alone |
| --- | --- | --- |
| Usefulness | 9.0 | 7.5 |
| Accuracy | 7.0 | 8.0 |
| Risk spotting | 9.0 | 7.0 |
| Clarity | 8.0 | 8.0 |
| **Winner** | Board | |

Judge, board shown first (A is the board): "A wins on risk: it flags contract warranty clawback, the need for a solicitor and the possible undeclared Self Assessment income, though it wrongly applies 6% Class 4 NI to £9,600 profit, which falls below the threshold, while B is accurate and clear but misses those sale-contract and tax-compliance risks."

Judge, Opus shown first (A is Opus alone): "B covers risks A misses (contract warranties and clawbacks, proof of funds, a walk-away price, unfiled Self Assessment, BADR only helping higher-rate taxpayers) and adds a useful after-tax keep-versus-sell comparison, though it wrongly applies 6% National Insurance to higher-rate earners, where the rate above £50,270 is 2%."

<details>
<summary>Board answer (632 words)</summary>

#### Decision
Don't accept £25,000 as it stands, but don't reject the idea of selling either. First confirm that the £800 a month is net profit and check the 12-month traffic trend. Then counter at £28,000 to £30,000. If the income is flat, falling or relies mostly on Google, sell at £25,000 to £28,000, through escrow only.

#### Why
- **The price is fair but low.** £25,000 is about 31 times monthly earnings, or 2.6 years of income. Common guidance for small, steady sites is 30 to 45 times monthly profit, which puts the low-to-middle value at £24,000 to £36,000. We could not confirm 2026 market figures, so treat that range as rough.
- **The trend decides it.** If income holds, keeping the site matches the sale proceeds in about 3 years. If a Google update cuts traffic, selling now is clearly better.
- **Keeping the site is taxed too.** Profit is taxed as income: 20% for a basic-rate taxpayer, 40% plus 6% National Insurance for a higher-rate taxpayer. That cuts £9,600 a year to roughly £5,200 to £7,700. A sale nets about £20,000 to £21,000 after Capital Gains Tax. Once both sides are taxed, selling looks better than it first appears.

#### Main risks
1. **A fake or haggling buyer.** The offer came to you unasked. Ask for proof of funds and use an escrow service such as Escrow.com. Don't give anyone logins or domain access until the money is secured.
2. **Price cut after checks.** Buyers often agree a price, then cut it during due diligence. Have your figures ready before you negotiate, so there is less to find.
3. **Money clawed back after the sale.** Broad promises in the sale contract about traffic or revenue can let the buyer claim money back later. Escrow does not protect you from this. Pay a solicitor to review the contract. I'd guess £500 to £1,500, but I'm not sure.
4. **Tax.** Capital Gains Tax is 18% or 24% on gains above £3,000. Business Asset Disposal Relief is now 18%, so it only helps higher-rate taxpayers, and only if the site is a genuine trade you've held for 2 years or more. If the site sits in a limited company, the tax works differently.
5. **Your counter ends the deal.** With only one buyer, this can happen. Decide your walk-away figure before you counter.

#### Honest criticism for the owner
You quoted "about £800 a month" without saying whether that is revenue or profit, or which way it is trending. Those facts decide the answer, and a buyer will ask for them on day one. Also, at £9,600 a year, you should already be filing Self Assessment for this income. If you haven't, fix that before you sell, because the buyer's checks may bring it to light.

#### Next steps
1. **This week:** pull 12 to 24 months of income, costs and traffic, including where the traffic comes from. If you can't produce this, you aren't ready to sell.
2. **Next week:** ask an accountant how the sale would be taxed. Ask the buyer for proof of funds and a written offer. Get a free comparison valuation from Flippa or Empire Flippers.
3. **Week 3:** counter at £28,000 to £30,000. Agree only to a written contract, escrow, no deferred or revenue-share payments, and 2 to 4 weeks of handover support at most.

#### Board notes
- I overruled the Advocate's revenue-share idea. After the sale the buyer controls the site and its income, so your share depends on their honesty and effort.
- I corrected the Operator's figures for keeping the site, which understated the income tax for a higher-rate taxpayer. That correction favours selling.
- Still open: the true 2026 market multiples, and Empire Flippers' switch to annual multiples. Neither was verified.

</details>

<details>
<summary>Opus alone (574 words)</summary>

#### Decision
Probably not at £25,000 yet. That offer is about 31 times monthly earnings, or 2.6 years of income. It is a normal price, not a generous one. Only accept if £800 is clean monthly profit and you have checked what it would sell for on the open market.

#### Main risks
- **Selling too cheap.** Small content and affiliate sites usually sell for about 25 to 45 times monthly net profit. Those figures are from broker guides I remember, such as Empire Flippers and Flippa, and I have not checked them for 2026. On £800 a month, that range is £20,000 to £36,000. Stable, low-effort sites with varied income sit at the top. Sites that depend on one traffic source sit at the bottom.
- **Revenue is not profit.** If £800 is revenue and you pay £150 a month for hosting, tools or writers, your real profit is £650. Then £25,000 is about 38 times profit, which is a good offer.
- **Keeping the site is risky too.** If most traffic comes from Google, a single algorithm update or more AI answers in search could cut income by 30 to 70% in a few months. £25,000 now is certain. 31 months of £800 is not.
- **Scams.** Unsolicited buyers sometimes take the domain and pay late or never. Always use escrow, such as Escrow.com.
- **Tax.** As a UK individual you will likely pay Capital Gains Tax on the gain above the £3,000 annual allowance. The rate is 18% if you are a basic-rate taxpayer and 24% if higher-rate. If the site counts as a trading business, Business Asset Disposal Relief might apply at 18% from April 2026. I am not sure how HMRC would classify your site, so check with an accountant. On a £25,000 gain, expect roughly £4,000 to £5,300 in tax.

#### Honest criticism for the owner
- You have one offer and no benchmark. The first unsolicited bid is almost never the best one. Buyers who approach you directly usually do so because they have spotted value.
- "About £800 a month" is too vague. Buyers will want 12 months of verified income and traffic data. If income is falling, seasonal, or was much lower last year, the value drops fast.
- You have not said what you would do with £25,000 or how many hours the site takes. If it takes 2 hours a month, it earns you £400 an hour and is worth keeping. If it takes 40 hours a month, selling looks much better.
- You may be underrating platform risk. If one affiliate programme, such as Amazon, brings in most of the income, that is fragile.

#### Next steps
1. **Work out real profit.** Do this by 9 November 2026. Take the last 12 months of revenue, subtract all costs, and divide by 12. Note the trend, and the share of traffic and income from each source.
2. **Get a second opinion on value.** Request a free valuation from Empire Flippers or Motion Invest, or list a draft on Flippa to see the bids. Go back to the buyer only after that. A reasonable counter-offer is £30,000 to £32,000 if your profit figure holds.
3. **Protect yourself on the sale.** Use escrow. Get full payment upfront rather than in instalments. Agree any handover support in writing, for example 30 days. Ask an accountant how CGT and the relief apply to you before you sign.

</details>

Full meeting: [statements and cross-examination](meetings/20261102-183046-59b6.md)

## Question 5

**My manager has offered me a team lead role for £3,000 more, but I would stop doing the hands-on work I enjoy. Should I take it?**

| | Board | Opus alone |
| --- | --- | --- |
| Usefulness | 9.0 | 8.0 |
| Accuracy | 8.0 | 7.5 |
| Risk spotting | 9.0 | 7.0 |
| Clarity | 8.0 | 8.5 |
| **Winner** | Board | |

Judge, board shown first (A is the board): "Both give sound, correctly calculated negotiate-first advice, but A covers more of the risks that matter, such as no legal right to return, possible loss of overtime pay, a new probation period and tribunal exposure, and it flags its uncertain claims, while B states unsourced figures like skills fading after 2 to 3 years as fact."

Judge, Opus shown first (A is Opus alone): "Both reach the same sound 'negotiate first' advice with correct take-home figures, but B adds material contract and legal risks (overtime loss, no legal right to return, new probation, 48-hour opt-out), flags uncertainty honestly, and gives concrete dated next steps."

<details>
<summary>Board answer (725 words)</summary>

#### Decision
Don't accept the offer as it stands. Your manager picked you, so you can negotiate, and asking costs you little. Before you decide, ask for three things in writing: a bigger raise, a protected share of hands-on work (at least 30 to 40%), and a 6-month review with a right to go back to your old role. If they refuse most of this and you don't want to manage people, say no and ask about a senior specialist route.

#### Why
- **The take-home gain is small.** For 2026/27, £3,000 gross leaves you about £2,160 a year (£180 a month) at basic rate. At higher rate it's about £1,740 (£145 a month). A student loan takes roughly £270 more. Pension contributions will change this a little.
- **Extra hours eat into it.** At 2 extra unpaid hours a week, the raise works out to about £19 to £24 net per extra hour. At 5 extra hours a week it's about £9.40. Compare that with your own current net hourly rate. Nobody knows yet how many hours this role adds.
- **Money rarely carries a management move.** In one survey, only about 1 in 10 leaders took the step mainly for pay, and about 26% had some regret in their first year. That's US-weighted data, so treat it as a weak signal.
- **Saying yes or no on the bare offer wastes your leverage.**

#### Main risks
- **No legal right to return.** UK law doesn't let you step back to your old role. Only a written contract term protects you. Even then, if your old role is filled during a trial, there may be no seat left, so ask what happens in that case.
- **Hidden contract costs.** Check for loss of overtime pay, which alone could cancel the raise. Also check for a new probation period, a longer notice period, and any request to opt out of the 48-hour week limit. The Employment Rights Act changes to unfair dismissal are expected around 2027. I'm unsure of the date, so check it before accepting a new probation.
- **Legal exposure as a lead.** You may run absence, discipline and grievance steps. Mistakes there can lead to tribunal claims, so ask for HR support and training.
- **Skills fade and the hands-on work gets squeezed.** Unless a percentage is written down, meetings tend to take over. That's plausible, but no hard data supports it.
- **The cost of saying no.** Someone else may get the role and become your lead. Nobody can measure how big this risk is.

#### Honest criticism for the owner
You've set this up as £3,000 against enjoyment. That leaves out the question that matters most: do you actually want to lead people? If you do, the money matters less and the terms matter more. If you don't, no realistic raise fixes it. You also seem ready to choose between yes and no without negotiating, which gives away your best leverage.

#### Next steps
1. **By Fri 6 Nov:** send your manager these questions in writing:
   - What share of my time stays hands-on?
   - How many reports would I have, and how many hours of meetings?
   - Would I lose overtime pay, and do the probation or notice terms change?
   - Is there a senior specialist grade, and what does it pay?
   - If I decline, who takes the role, and does that affect my next review?
2. **Before replying:** look at current job adverts for lead and senior specialist roles in your field. Use what you find to set a counter figure. £5,000 is a starting point the board picked, not market data.
3. **By Fri 20 Nov:** decide. Accept only with written protected hands-on time and a dated 6-month review with a return clause. Otherwise decline in writing and ask what other route leads to a raise.

#### Board notes
- I overruled Operator's comparison with the National Living Wage. It set take-home pay against a gross figure. The right test is your own hourly rate.
- I overruled Advocate's "take it". Its own conditions aren't met today, so the honest answer is "not yet".
- Several of Skeptic's claims have no source: leaving within 1 to 2 years, skills fading after 18 months, and middle layers being cut first. I treated them as plausible, not proven.

</details>

<details>
<summary>Opus alone (523 words)</summary>

#### Decision
Do not accept it as offered. £3,000 a year is too little to give up work you enjoy, unless you actually want a management career. Go back and ask for more money, a trial period, or a lead role that keeps some hands-on work. If you get none of these, decline politely.

#### Main risks
- **The take-home gain is small.** If you pay basic rate tax (20%) and 8% National Insurance, £3,000 is about £2,160 a year, or £180 a month. If the rise puts you over the higher rate threshold (£50,270), part of it is taxed at 40% plus 2% NI. In that case you keep closer to £1,740 a year, or £145 a month. I do not know your salary, so check where you sit.
- **The hours may grow.** Lead roles often bring evenings, people problems and meetings. Say you add 3 hours a week over 46 working weeks. That is about 138 hours, so your extra pay works out at roughly £13 to £16 an hour after tax.
- **Your skills will fade.** After 2 to 3 years away from hands-on work, getting back to a senior hands-on job gets harder.
- **Saying no has a cost too.** Some employers quietly sideline people who turn down promotion. I cannot tell whether yours does.
- **Going back down is awkward.** Few companies have a clean way to step back from leading a team.

#### Honest criticism for the owner
- You are treating this as a yes or no question. It is an opening offer. You have not asked whether it can be negotiated.
- You are looking at the headline £3,000 and not at what you actually keep or what it costs you in time.
- You say you enjoy hands-on work, but you have not said where you want to be in 5 years. If you want to be a head of department one day, this is a normal first step and enjoying it now matters less. If you do not, this is a detour.
- You may be assuming that "team lead" means no hands-on work at all. Many lead roles are 50/50 or 70/30. Find out what this one really involves before you decide.
- Check whether your company has a senior or principal track that pays more without managing people. If you have not asked, you may be missing the option you would like best.

#### Next steps
1. **This week, ask your manager for specifics in writing:** the hours per week of hands-on work, the team size, any on-call duties, and whether there is a senior individual contributor route instead.
2. **Benchmark the pay.** Look up team lead salaries for your field and region on Glassdoor, Reed or Hays. If the market gap is £6,000 to £10,000, ask for that, or for a review after 6 months.
3. **Make your decision depend on terms.** Something like: "I'll take it with £X, at least 30% hands-on time, and a review after 6 months." If they refuse all three, decline and ask what your path to a senior role without management looks like.

</details>

Full meeting: [statements and cross-examination](meetings/20261102-183209-4828.md)

## Question 6

**My company wants everyone in the office four days a week instead of two. Should I accept it, push back, or start looking for another job?**

| | Board | Opus alone |
| --- | --- | --- |
| Usefulness | 9.0 | 8.0 |
| Accuracy | 8.0 | 8.0 |
| Risk spotting | 9.0 | 7.5 |
| Clarity | 8.0 | 7.5 |
| **Winner** | Board | |

Judge, board shown first (A is the board): "A gives a concrete, dated plan and flags the key risk that working the new pattern without written protest can count as accepting a contract change, which B's 'accept for now' advice misses, though B helpfully raises disability and caring-duty protections."

Judge, Opus shown first (A is Opus alone): "Both give sound, well-hedged UK advice, but B adds key risks A misses (implied acceptance and complying under written protest, implied contract terms from long-running custom, not wasting one of the two statutory requests), uses accurate supporting evidence, and gives concrete dated next steps."

<details>
<summary>Board answer (629 words)</summary>

#### Decision
Push back in a measured way, and don't accept quietly or quit. Read your contract this week. Then send one well-prepared written flexible working request by Friday 13 November 2026, for example for 3 office days or fixed days. Start a quiet job search alongside it. Don't resign until you hold a signed written offer.

#### Why
- **Your contract decides how strong you are.** If it names home or hybrid as your place of work, the company may need your consent to change it. A hybrid pattern that ran for years and was never called temporary may also have become a contract term. If neither applies, the company can probably impose four days with reasonable notice.
- **The law gives you a request, not a right.** Since 6 April 2024 you can ask for flexible working from day one. The employer must consult you and decide within 2 months, including any appeal. It can refuse on any of 8 business grounds.
- **The cost is real.** Assume 45 minutes each way and £23 a day for fares and lunch. Then two extra days a week cost about 92 days, 138 hours and £2,120 after tax each year. That is about £2,940 of gross pay at basic rate. Use your own figures.
- **Visibility gains are probably small.** A 2024 randomised trial at Trip.com found that two home days a week had no effect on promotion. You already go in 2 days, so days 3 and 4 likely add little.

#### Main risks
- **Quitting without an offer.** A 3 to 6 month gap on £40,000 costs £10,000 to £20,000 before tax. Check the jobs market against the latest ONS figures.
- **Implied acceptance.** If you work the new pattern for weeks without objecting in writing, that can count as agreeing to it. If you comply while your request is pending, say in writing that you are complying "under protest".
- **Weak dismissal protection.** You currently need 2 years' service to claim unfair dismissal. The Employment Rights Act 2025 is expected to cut this to 6 months, possibly from 1 January 2027. The board has not confirmed the date, so check it on gov.uk or with Acas.
- **Wasting a request.** You get only 2 statutory requests in any 12 months. A rushed or badly argued request uses one up.
- **Being seen as resistant.** If the mandate is a quiet way to cut staff, objecting alone is riskier than objecting with colleagues.

#### Next steps
1. **By Friday 6 November:** find your place of work clause and any variation or hybrid policy. Note when the mandate starts, your notice period and your length of service. Work out your real yearly commute cost. If the wording is unclear, call Acas on 0300 123 1100.
2. **By Friday 13 November:** submit the written request. Give a specific pattern, your real cost figures and how your output will be maintained. Don't quote unverified studies. Find out whether colleagues are objecting too.
3. **Now:** update your CV and spend about 3 hours a week on a quiet search, using only your own devices and your own time. Review everything on Friday 15 January 2027, or sooner if they decide earlier. If they refuse and the cost is more than you can tolerate, search hard. Resign only with a signed offer.

#### Board notes
- I overruled the Advocate's "accept the four days". Accepting can weaken your contract position. The promotion upside also has no evidence behind it, and the Trip.com trial points the other way.
- I partly overruled the Skeptic. Complying is fine, but only under written protest, not silently.
- Still open: the exact start date of the 6-month qualifying period, and whether your contract fixes hybrid working.

</details>

<details>
<summary>Opus alone (590 words)</summary>

#### Decision
Accept for now, but push back in a formal way and quietly start looking. Make a statutory flexible working request for two or three office days. Start a low-effort job search at the same time, so you have a real option if the answer is no. Do not resign before you have an offer.

#### Main risks
- **Cost and time.** Two extra days a week over about 46 working weeks is roughly 92 more commutes a year. At £20 a day that is about £1,840 a year from taxed pay. At 1.5 hours a day it is about 140 hours a year. Use your own figures. I do not know them.
- **Your contract.** If your contract names home or hybrid as your place of work, the company generally needs your agreement to change it. If hybrid is only a policy, they can usually change it with notice. Check which it is. I have not seen your contract.
- **Weak legal position.** Since 6 April 2024 you can make a flexible working request from your first day. You can make two a year. The employer must consult you and decide within 2 months. But they can refuse on 8 business grounds, and challenging that is hard. The Employment Rights Act 2025 is meant to make refusals harder, but I am not sure when that part comes into force. Check before you rely on it.
- **Resigning and claiming constructive dismissal** usually needs 2 years' service and a fundamental breach. It is risky and slow. Treat it as a last resort.
- **Being marked as resistant.** If redundancies follow, people who openly refused may be more exposed.

#### Honest criticism for the owner
- You have given me no details: commute, caring duties, health, salary, length of service, the job market in your field. My advice can only be conditional. If you have a disability or caring duties, reasonable adjustment or discrimination rules may protect you much more. That changes the advice.
- You are framing this as three separate options. They are not. The strongest move is to do all three in order: comply, ask formally, keep an exit ready.
- "Push back" usually means complaining informally. That carries risk and achieves little. A written request that argues the business case does better. Point to your output, your results while hybrid, and how you would cover anything the office is said to need.
- Moving jobs to stay hybrid may cost more than it saves. Many UK employers have moved to 3 or more office days in 2025 and 2026. A new job could change the rules again, and you would start with fewer employment rights.

#### Next steps
1. **This week:** read your contract and the written announcement. Note the start date, whether "place of work" is defined, and any consultation. If a union or staff forum exists, ask what it is doing.
2. **Within 2 weeks:** submit a written statutory flexible working request. Ask for 2 or 3 days, give business reasons, and offer a 3 month trial. Keep copies. If you are refused, ask which statutory ground they used. Acas guidance and the free Acas helpline (0300 123 1100) can help.
3. **Now:** update your CV and LinkedIn. Talk to 2 or 3 recruiters about roles with written hybrid terms. Set a deadline, for example 3 months after the policy starts. If it still costs you too much by then, move only once you have an offer that guarantees hybrid working in the contract.

</details>

Full meeting: [statements and cross-examination](meetings/20261103-202341-aec0.md)

## Question 7

**I'm 35 and want to retrain as a primary school teacher, which means a £15,000 pay cut. Should I do it?**

| | Board | Opus alone |
| --- | --- | --- |
| Usefulness | 8.5 | 7.5 |
| Accuracy | 7.0 | 7.5 |
| Risk spotting | 8.5 | 7.5 |
| Clarity | 7.5 | 8.0 |
| **Winner** | Board | |

Judge, board shown first (A is the board): "A wins narrowly because it prices the unsalaried training year (£30–38k take-home), sets a 10-month savings target and a 2028 fallback, though it wrongly says the 2026/27 pay scale is unconfirmed and assumes the person is a parent, while B is better sourced on pay but less concrete about cash risk."

Judge, Opus shown first (A is Opus alone): "B puts a figure on the training-year cost, sets clear rules such as not resigning before an offer and saving 10 months of costs, and gives sharper deadlines; A is clearer and its pay-scale sourcing looks more current, but its plan is less concrete about the main financial risk."

<details>
<summary>Board answer (652 words)</summary>

#### Decision
Yes, retraining can be worth it, but don't resign or apply blind. In the next 6 weeks, spend at least 10 days in a primary classroom. Then apply for a September 2027 place. Only hand in your notice once you hold an offer and have savings to cover about 10 months with no salary. If the savings aren't there by June 2027, aim for September 2028 instead.

#### Why
- **The £15,000 cut is not your biggest cost. The training year is.** Most primary routes are an unsalaried PGCE. The fee for 2026/27 is £9,790, which a loan normally covers. Primary trainees get no bursary. If you earn about £48,000 now, the year out costs you roughly £30,000 to £38,000 of take-home pay.
- **The ongoing cut is smaller than it looks.** Starting pay outside London is about £33,000 to £34,000. The official 2026/27 scale isn't confirmed yet. The Teachers' Pension Scheme employer contribution is about 28.7%, against the 3% to 5% many private employers pay. In like-for-like terms that makes your real gap nearer £7,000 to £10,000 a year. But pension money doesn't pay the mortgage.
- **Pay does catch up, slowly.** The main scale tops out at about £45,000 after around 6 years. The upper pay range (about £49,000) and responsibility allowances can take you past £48,000, but neither is guaranteed.
- **Most new teachers stay.** About 70% are still teaching 5 years after qualifying. That figure is from a secondary source and undated. Treat it as rough.

#### Main risks
- **Cash runs out in the training year.** A mortgage, children or a partner who depends on your income could break the plan. Check your maintenance loan entitlement on GOV.UK. The board could not confirm the 2026/27 amounts.
- **The workload drives you out after you've paid to switch.** Term-time weeks of 50 hours or more are common. Leaving in year two or three leaves you with a gap on your CV and the money gone.
- **Fewer primary jobs.** Primary pupil numbers are falling, and London is worst hit. You may not find a secure post near home.
- **No degree means a different route.** Without one you generally can't do a PGCE. The route is longer and the case for retraining gets weaker.

#### Honest criticism for the owner
You've framed this as a £15,000 pay cut. That framing hides the real hit: a training year that could cost £30,000 to £38,000 in lost take-home pay. You also left out the facts that decide this: your savings, mortgage or rent, dependants, region, and whether you have a degree. Most importantly, nothing you wrote shows you've spent recent time in a classroom as anything other than a parent. Wanting to teach and liking the job day to day are not the same thing.

#### Next steps
1. **By 15 December 2026:** book and complete 10 days of school experience through the DfE "Get school experience" service, using annual leave. If you can, keep up regular contact afterwards, for example tutoring or becoming a school governor.
2. **By mid-December 2026:** apply through "Apply for teacher training". Applications open on a rolling basis and popular courses fill early. Apply for salaried or apprenticeship places alongside the PGCE, since a salaried place removes the lost year.
3. **This month:** write down your monthly essential costs. Set a savings target of 10 months of those costs by June 2027. Check local primary vacancies and your council's pupil forecasts.

#### Board notes
- I overruled Skeptic's £55,000 to £60,000 figure. It adds gross pay to fees that a loan covers. The cash you actually lose is about £30,000 to £38,000.
- I overruled Operator's "you never catch up". The upper pay range and allowances can go above £48,000, but slowly and with no guarantee.
- I set aside Advocate's hope of a bursary. Primary has none, and salaried places are scarce.

</details>

<details>
<summary>Opus alone (563 words)</summary>

#### Decision
Yes, do it, but only if two things are true by summer 2027. First, you have spent at least 10 days in a real primary classroom and still want the job. Second, you can get through a training year with little or no income. If both hold, the pay cut is smaller than it looks, and it shrinks after about five years.

#### Main risks
- **The training year costs more than £15,000.** A PGCE in England costs about £9,500 or more in fees. Primary trainees get no bursary, so you could lose a full year of salary on top. Salaried routes avoid this, such as the postgraduate teaching apprenticeship or school-led salaried places. But there are few of them and they are competitive.
- **Starting pay.** From September 2026 the starting salary outside London is about £34,068, after a 3.5% rise. A further 3% rise is due in September 2027. Moving up to the top of the main scale takes about five years, which should put you at roughly £47,000. I worked that figure out myself and have not checked it against the official pay document.
- **Fewer pupils.** Primary pupil numbers in England are falling. In some areas that means fewer jobs and some schools merging. I am not sure how bad this is where you live, so check local vacancies.
- **Burnout.** Many teachers leave within five years. Workload of around 50 hours a week during term is common. Your current job may be easier than you think.
- **A hidden plus.** The Teachers' Pension Scheme is a defined benefit scheme. Employers pay in about 28% of salary on top of your pay. Count that when you compare total pay. Your £15,000 figure probably leaves it out.

#### Honest criticism for the owner
- You are treating £15,000 as a permanent loss. It is probably a first-year figure. It ignores the training year, which costs more, and the pension and pay scale, which reduce the gap. Do the full maths over 10 years, not one.
- You have not said why you want this. "I want to work with children" is not enough. The job is mostly planning, behaviour management, marking, Ofsted and talking to parents. If you have never spent a full week in a Year 4 classroom, you are guessing.
- You have not said whether you have a degree. You need one for qualified teacher status (QTS) through a PGCE. Without one, the route is longer and different.
- At 35 you are not late. Career changers are common and schools value them. Age is not the risk. Money and stamina are.

#### Next steps
1. **Before Christmas 2026,** book classroom days through the government's Get School Experience service, or ask a local primary school directly. Aim for 10 days or more.
2. **In the same period,** write out a 10-year budget. Include the training year, starting pay of £34,068, yearly rises, the pension, and your fixed costs such as rent or mortgage. Then compare it with staying in your current job.
3. **By January 2027,** talk to a free Get Into Teaching adviser about salaried routes, and apply early for September 2027 entry. Good places fill quickly.

Sources:
- [DfE Education Hub: multi-year pay award](https://educationhub.blog.gov.uk/2026/07/teacher-pay-everything-you-need-to-know-about-the-latest-multi-year-pay-award/)
- [Edapt: teacher pay deal 2026](https://www.edapt.org.uk/blog/2026/07/teacher-pay-deal-2026/)
- [uknetpay: Teacher pay scale 2026-27](https://uknetpay.co.uk/insights/teacher-pay-scale-2026-27)
- [The Key: DfE announces 2026/27 award](https://schoolleaders.thekeysupport.com/administration-and-management/government-policies-and-legislation/need-to-knows/dfe-announces-teacher-pay-award-202627/)

</details>

Full meeting: [statements and cross-examination](meetings/20261103-202529-921d.md)

## Question 8

**I have a job offer from another company. Should I tell my manager to try for a counter-offer?**

| | Board | Opus alone |
| --- | --- | --- |
| Usefulness | 8.5 | 7.5 |
| Accuracy | 6.5 | 8.0 |
| Risk spotting | 9.0 | 7.5 |
| Clarity | 7.5 | 8.0 |
| **Winner** | Tie | |

Judge, board shown first (A is the board): "Both give sound conditional advice, but B adds a practical total-package comparison and a script while avoiding A's specific, hard-to-verify statistics such as the 40.8% Robert Half figure, though A uniquely covers after-tax value and the loss of unfair-dismissal protection."

Judge, Opus shown first (A is Opus alone): "B adds more practical and distinctive guidance: don't sign before negotiating, the after-tax value of a rise, a market-based pay review without revealing the offer, asking the new employer to improve its package, and the loss of unfair-dismissal protection in a new job, though a few of its statistics are hard to verify."

<details>
<summary>Board answer (690 words)</summary>

#### Decision
Only tell your manager if pay is the main reason you looked and you would really stay for a specific package you have already written down. If something else drives you, such as your manager, the work or a lack of progression, don't ask for a counter-offer. Decide which job you want and act on it. Before you speak to anyone, get the new offer unconditional and in writing, but do not sign it yet.

#### Why
- **A counter-offer only fixes pay.** If you looked for other reasons, staying for money just delays the move, and you will have lost some trust.
- **The numbers are less bleak than people say, but still not good.** The "80 to 90% leave within a year" claim has no traceable source. Better evidence is a Robert Half UK survey of 2,000 workers in 2021, which found 40.8% of people who accepted a counter-offer left within 12 months. Other figures are around 50%, and the sources conflict. So it is not a trap by default, but it is close to a coin flip.
- **The prize shrinks after tax.** Say you earn £50,000 and get a £5,000 rise. You keep about £2,900 a year, roughly £240 a month, at 40% tax plus 2% NI. Between £100,000 and £125,140 the marginal rate is about 62%, so you would keep roughly £1,900.
- **You may get nothing.** One UK survey found most employers have never made a counter-offer.

#### Main risks
- **Flight-risk label.** Once you say you have an offer, you may be quietly passed over for promotions or projects, even if you stay. You cannot undo this, and it is hard to prove.
- **Losing the new offer.** Slow talks, or signing and then backing out, can make the new employer withdraw and damage your name with them and any recruiter.
- **A weak counter.** It may be a one-off retention bonus with a clawback clause rather than a base pay rise. Check your current contract for clawback on bonuses or relocation, and for restrictive covenants.
- **"Congratulations, go."** Your employer may accept your resignation, bring your leaving date forward or put you on garden leave.
- **Weaker legal protection in a new job.** You currently need 2 years' service before you can claim unfair dismissal. The Employment Rights Act 2025 is reported to cut this to 6 months from January 2027. I am not certain of the date, so check gov.uk.

#### Honest criticism for the owner
You asked how to get a counter-offer, not which job you want. That suggests you may want the offer as leverage rather than as a real choice. A bluff shows, and if your manager calls it you are stuck with whatever you can get. Also, you can ask for a pay review based on market data without mentioning the offer at all, and you have not considered that.

#### Next steps
1. **Today, 1 hour.** Write down your main reason for leaving, your walk-away salary figure and two or three changes that would keep you for 12 months or more. If you would not stay for those, stop here and take the new job.
2. **Within 3 days.** Get the new offer unconditional and in writing, and check the salary, pension, start date, probation and notice period. Ask the new employer if they can improve the package. That costs you nothing.
3. **If you go ahead.** Hold one 30-minute meeting with your manager. Make one specific request and ask for a written answer within 3 working days. Accept only a base pay rise in writing. Otherwise, resign in writing.

#### Board notes
- I overruled the Operator's "tell your manager only once the offer is signed". Signing and then bargaining means backing out of a signed agreement. A written, unconditional offer is the right trigger.
- I overruled the Skeptic's rule that all six conditions must hold. That is too strict, because you cannot know your employer's past record on counter-offers.
- The Advocate's claim that "managers often prefer to pay now" has no evidence behind it, so I gave it little weight.

</details>

<details>
<summary>Opus alone (566 words)</summary>

#### Decision
Only ask for a counter-offer if you would truly be happy to stay for the right deal. If you are leaving because of the manager, the work, or how you are treated, take the new job and resign cleanly. I can't be firmer than that because you haven't told me why you looked elsewhere, what the pay gap is, or how much you like your current role.

#### Main risks
- **Your loyalty gets questioned.** Once you show an outside offer, some managers see you as a flight risk. That can affect who gets promotions, key projects or redundancy decisions over the next 12 to 24 months.
- **Money rarely fixes the real problem.** If you left because of workload, culture or career growth, a pay rise will not change it. You will likely start looking again.
- **The new offer can be lost.** Haggling takes time. The other company may withdraw an unsigned offer, fill the role, or lose trust in you. In the UK, a job offer can usually be withdrawn before you start, often with little or no notice pay owed.
- **A weak counter.** Some employers offer a one-off bonus or a vague "we'll review it in April" instead of a lasting salary rise. Get any counter in writing, with an effective date.
- **The numbers are uncertain.** You may have heard that "80% of people who accept counter-offers leave within a year." I could not verify that figure. It comes from recruiters, who have a reason to put you off staying. Treat it as anecdote.

#### Honest criticism for the owner
- You are asking how to get a counter-offer before you have said whether you want to stay. Answer that first. If the answer is "only for more money," you are using the new company as a bargaining chip. It may work, but it has a cost.
- You haven't compared the full packages. Look at base salary, bonus, pension contribution (for example 5% vs 10% employer match is a real difference), holiday, hybrid days, notice period and commute cost. A £5,000 rise can be wiped out by a worse pension and a longer commute.
- You may not have checked your own contract. Look at your notice period and any garden leave clause. Also check for restrictive covenants, such as non-compete or non-solicitation clauses. These affect your timing and your leverage.
- "Telling your manager" is resigning in all but name. Be ready for them to say "congratulations, good luck."

#### Next steps
1. **Today:** Write down your top 3 reasons for leaving and a total-package comparison in £ per year. If the reasons aren't mainly about pay, accept the new offer.
2. **Before you speak to your manager:** Get the new offer in writing and confirm the start date. Check your notice period. Decide your walk-away number, for example "I'd stay for £X base, effective next month, confirmed in writing."
3. **If you do raise it:** Keep it short and factual. Say: "I've had an offer of £X. I'd prefer to stay if we can get to £Y by [date]." Give a firm deadline of 2 to 3 working days. Don't reveal the other company's name, and keep the new employer warm in the meantime.

If you tell me the salaries, your reasons for leaving and your notice period, I can give you a firmer answer.

</details>

Full meeting: [statements and cross-examination](meetings/20261103-202657-bbb5.md)

## Question 9

**I sell handmade candles at weekend markets. Should I rent a small shop unit for £1,200 a month?**

| | Board | Opus alone |
| --- | --- | --- |
| Usefulness | 8.0 | 7.0 |
| Accuracy | 7.0 | 7.0 |
| Risk spotting | 9.0 | 8.0 |
| Clarity | 7.0 | 8.0 |
| **Winner** | Board | |

Judge, board shown first (A is the board): "Both answers give similar break-even maths and lease warnings, but A sees that a Christmas test would flatter demand and moves the test to January to March, while B recommends testing in peak season despite noting seasonality; A also covers dilapidations and 1954 Act renewal rights, though its wording is clumsier and its pass mark (30 a week vs 7 a day) is slightly inconsistent."

Judge, Opus shown first (A is Opus alone): "B sets clearer test criteria, rightly warns that a Christmas test will flatter demand, and covers more lease risks such as dilapidations and lost renewal rights, though its candle-count pass marks (30 a week against 180 a month) do not quite match."

<details>
<summary>Board answer (675 words)</summary>

#### Decision
No, do not sign for this unit on a standard lease now. First test whether people buy your candles away from markets. Use a shared maker shelf (about £50 to £150 a month) or a short licence from January to March 2027. Only take a unit if the test passes, the lease has a break clause at 12 months or sooner, and there is no personal guarantee.

#### Why
- **The shop has to sell a lot.** £1,200 rent plus utilities, insurance, card fees and maybe business rates comes to about £1,450 to £1,700 a month. At 60 to 65% gross margin, you would need about £2,500 to £2,850 in sales a month before you pay yourself. That is roughly 180 candles a month, or 7 a day.
- **It is a hidden swap, not extra income.** You work alone. Shop hours will clash with your weekend markets, so the shop must earn its costs plus the market profit you give up. Paying staff instead costs about £2,200 a month for 40 hours a week at £12.71 an hour, which is more than the rent. Check the current wage rate on gov.uk.
- **Market demand may not move with you.** Market shoppers came for the market. Nobody knows yet if they will find a side-street unit.
- **Setup costs.** Expect £6,000 to £8,000 up front for the deposit, fit-out, stock and legal fees. These are estimates.

#### Main risks
- **Personal guarantee.** If you sign one on a multi-year lease and the shop fails, the debt becomes yours personally, not just the business's. This is the most likely way this ends badly.
- **Seasonality.** Candles peak from October to December. If you sign a lease after a strong Christmas, you then carry £1,200 a month through January to September.
- **Exit costs.** Many leases make you pay to restore the unit when you leave (called dilapidations). Some also remove your right to renew the lease under the Landlord and Tenant Act 1954.
- **Fire and insurance.** Pouring wax, lit testers and workshops may break the lease's use clause or the landlord's insurance terms. You need product and public liability cover.
- **Business rates are unclear.** In England, units with a rateable value under £12,000 currently pay nothing under Small Business Rate Relief. Rules changed in April 2026 and the board could not confirm the details. Scotland and Wales have different rules.

#### Honest criticism for the owner
You asked about a specific unit without knowing your own numbers. No one on the board could judge this, because you have not said what your markets earn after pitch fees. A shop decision without that figure is a guess. Also, do not treat Christmas sales as proof. December will flatter any test.

#### Next steps
1. **Within 7 days:** write down your weekly market takings and costs for the last 6 months, after pitch fees. Include last December and January if you have them, so you can see how much of your trade is seasonal.
2. **Within 14 days:** ask the landlord for the unit's rateable value, lease length, break clause, deposit, guarantee terms, and whether wax work is allowed. Check the rateable value on the VOA website.
3. **January to March 2027:** run the shelf or licence test. Pass mark: about 30 extra candles a week, or about £2,500 a month in a unit-sized setting, from non-market sales.

#### Board notes
- I overruled the Advocate's test of "£1,500 a month stall profit". That is your current income, and the shop has to earn its costs on top of it.
- I rejected testing in November and December as proof. The Operator's 4-week test would run into the Christmas peak and mislead you. A Christmas pop-up is fine for the extra sales if you can set one up within days, but it does not settle the question.
- Still open: whether workshops and wholesale could fill quiet weekdays. No one gave evidence either way. Wholesale margins may be thin (one source says about 17%).

</details>

<details>
<summary>Opus alone (605 words)</summary>

#### Decision
Not yet. Don't sign a lease until your figures show the shop can cover about £1,700 a month in total costs, not just the £1,200 rent. Test demand first with a short pop-up or a shared shop over Christmas 2026. You haven't told me your sales or margins, so this is a cautious call, not a verdict on your business.

#### Main risks
- **True cost is higher than the rent.** £1,200 a month is £14,400 a year. On top of that come business rates, utilities, insurance, card fees, fit-out and often a service charge. Expect roughly £300 to £600 a month more. I'm not sure of the exact figure for your unit. Small Business Rate Relief in England can cut rates to zero if the rateable value is under £12,000 and this is your only business property. Check the unit on the GOV.UK "Find a business rates valuation" service.
- **Break-even is steep.** If your gross margin is about 65% (a guess for handmade candles), £1,700 of monthly costs means about £2,600 a month in extra sales. That's around £600 a week on top of what you sell now.
- **Seasonality.** Candles sell best from October to December. January to March is usually slow, but rent still has to be paid every month.
- **Lease lock-in.** Commercial leases often run 3 to 5 years and may come with a personal guarantee and a 3-month deposit. A bad year could mean you're personally liable for over £40,000.
- **Lost market income.** If you staff the shop yourself, you can't do your weekend markets as well. You might lose your best sales days.
- **Fire and insurance.** Burning candles on display, and making them on site, can raise premiums or break lease terms. Check before you sign.

#### Honest criticism for the owner
- You're asking about the rent, not about profit. The real question is whether the shop brings in enough extra sales to beat what you'd earn from markets alone. You haven't shown that it does.
- Market footfall comes from the event. A shop has to create its own. Weekend market customers may not walk into a side-street unit on a Tuesday.
- A shop needs to be open 5 to 6 days a week, around 40 or more hours. Either that's your time, which then isn't spent making candles, or it's wages. At the April 2026 National Living Wage of £12.71 an hour for over-21s, that's roughly £2,000 a month or more. Please check the current rate.
- It's November 2026. Signing now feels exciting because Christmas is close, but the lease will mostly be paid through the quiet months.

#### Next steps
1. **Run the numbers this week.** Look at your last 12 months of market sales, your margin per candle, and your best and worst months. If your current profit can't cover about £1,700 a month during the slow months, don't sign.
2. **Test cheaply before 31 December 2026.** Try a Christmas pop-up, a space in a shared maker shop, or a concession in a gift shop. These are often weekly or commission-based. Track sales per day against what you'd need for break-even.
3. **If you still want the unit, negotiate.** Ask for a 1-year lease or a break clause at 6 or 12 months, 3 months rent-free, no personal guarantee, and written confirmation that candle making and display are allowed. Get a solicitor to review the lease. Expect to pay around £500 to £1,500, though I'm not certain of local rates.

If you share your monthly sales and margins, I can tell you whether the numbers work.

</details>

Full meeting: [statements and cross-examination](meetings/20261103-202821-5b44.md)

## Question 10

**My dog-walking business has a waiting list. Should I hire my first employee or raise my prices?**

| | Board | Opus alone |
| --- | --- | --- |
| Usefulness | 8.0 | 7.5 |
| Accuracy | 7.0 | 8.0 |
| Risk spotting | 9.0 | 7.5 |
| Clarity | 6.5 | 8.5 |
| **Winner** | Tie | |

Judge, board shown first (A is the board): "Both give the same sound price-first plan, but B is clearer, adds the director caveat on Employment Allowance and the management burden of hiring, and flags its unverified figures, while A has slightly richer risk coverage but awkward analyst clutter and break-even thresholds it cannot support without knowing the owner's prices."

Judge, Opus shown first (A is Opus alone): "Both give the same sound advice to raise prices first, but B adds a concrete break-even (about 18 billed hours on a 25-hour contract), a cash-buffer test and more of the risks that matter (empty paid hours, council dog caps, right-to-work checks, day-one sick pay, client poaching); A is clearer and correctly notes the director exception to the Employment Allowance, which B leaves out."

<details>
<summary>Board answer (670 words)</summary>

#### Decision
Raise your prices now, and don't hire yet. Put the rise on new and waiting-list clients this week, and on existing clients from 1 January 2027. Decide on a part-time hire in February 2027. Only hire if the list, at the new price, could fill about three-quarters of the hours you would pay that person for.

#### Why
- **A waiting list is the clearest sign you charge too little.** It tells you demand beats supply at today's price. It does not tell you whether demand would cover a wage. A price rise answers the first question at no cost, and you can reverse it.
- **A hire is a fixed cost that is hard to undo.** At the £12.71 an hour minimum wage for ages 21 and over, a 25-hour contract costs about £16,500 a year in wages. Then add the 3% employer pension, insurance and payroll costs. Travel time between walks counts as paid working time.
- **Employer National Insurance is probably not a cost.** The £10,500 Employment Allowance should cover it for a first employee. Confirm you are eligible.
- **No member's profit forecast holds up.** The board has none of your real figures. The one 12-month estimate (about £13,000 extra) assumed the hire bills only about 8 of 20 paid hours, so treat it as a guess.
- **Waiting too long has a cost.** People on the list will not wait months. Testing until spring 2027 lets the list fade.

#### Main risks
- **Paying for empty hours.** This is the most likely way a hire fails. Rain, cancellations and school holidays still cost you wages. On a 25-hour contract, fewer than about 18 billed hours a week loses money.
- **Legal duties from day one.** Employer's liability insurance is compulsory, with fines of up to £2,500 a day without it. You also need PAYE registration, auto-enrolment, a right-to-work check and a written contract. Statutory sick pay is now due from day one. If you control a walker's hours and routes, they are probably an employee, whatever label you use.
- **Harder to dismiss someone.** The unfair dismissal qualifying period may drop to 6 months from 2027. This is not confirmed, so check it before you hire.
- **Your reputation and your clients.** An employee's lost dog damages your name. They also hold your clients' keys and could take clients with them if they leave.
- **Local dog limits.** Many councils cap the number of dogs per walker, often at 4 to 6. Group-walk income depends on your council's rule.

#### Honest criticism for the owner
You asked "hire or raise prices?" without knowing your own numbers. You need four: your hourly price, dogs per walk, your weekly hours and how long the list really is. Without them, neither option can be judged. Also, if you are well below the local rate (roughly £16 to £25 an hour, from rough sources), you have been leaving money on the table for a while.

#### Next steps
1. **By 10 November:** count the list and the hours it would fill each week. Check your council's dog cap and local rivals' prices.
2. **By 1 December:** quote new and waiting-list clients about 10 to 15% more. Check what notice your client terms require, then give existing clients at least 30 days' notice of a rise from 1 January.
3. **February 2027:** decide on the hire. Go ahead only if:
   - the list still fills about 18 or more billed hours a week
   - you hold about £4,400 in cash (3 months of wages)
   - insurance and payroll are set up before the start date.

#### Board notes
- I overruled the Skeptic's wait until spring 2027. The list will fade, so decide in February instead.
- I overruled the Advocate's one-month test. Clients leave at renewal, not straight away. The Advocate's paid priority tier is optional, untested and may annoy loyal clients.
- Still open: the dismissal rule change and your Employment Allowance eligibility both need checking.

</details>

<details>
<summary>Opus alone (606 words)</summary>

#### Decision
Raise your prices first. A waiting list usually means you are charging too little. Put up prices for new clients now, give existing clients 30 days' notice, and only hire if the list is still long after about 3 months at the new price. Raising prices costs nothing and you can undo it. Hiring is expensive and hard to reverse.

#### Main risks
**If you raise prices:**
- You may lose some existing clients. A 10 to 15% rise usually loses a few, not most. I can't tell you your local market, so test it on new clients first.
- Your rates may go above local rivals. Check 3 to 5 competitors before you set a number. As a rough guide, a group walk might cost £12 to £16 outside London and £16 to £22 in London. Please check your own area.

**If you hire:**
- **Cost.** The National Living Wage is £12.71 an hour for workers aged 21 and over (from April 2026; check gov.uk). At 25 hours a week that is about £16,500 a year before other costs. You also need to pay for travel time between walks, a 3% employer pension contribution, holiday pay and possibly mileage.
- **Legal duties.** You must have employer's liability insurance with at least £5 million of cover, or you can be fined up to £2,500 a day. You also need to register with HMRC for PAYE and set up a pension under auto-enrolment.
- **Employer National Insurance** is 15% on pay above £5,000 a year. The £10,500 Employment Allowance may cover it, but not if your only employee is a director of a limited company.
- **Reputation.** If an employee loses or injures a dog, it is your name that suffers. Trust is what you are selling.
- **Fake self-employment.** Calling a walker a "contractor" while you set their hours and routes can make them an employee in law anyway.

#### Honest criticism for the owner
- You are treating this as a choice between two things. It isn't. Pricing comes first, and what happens afterwards tells you whether hiring makes sense.
- A waiting list feels good, but it is income you are turning away. It is not proof the business can support a wage.
- I don't know your price, how long the list is, how many hours you work, or your profit per walk. Neither of us can make a confident hiring decision without those numbers. If you don't know your profit per walk, that is the real problem.
- Your first hire changes your job. You will spend less time walking dogs and more time managing a person, sorting rotas and covering sick days. Ask yourself honestly if you want that.

#### Next steps
1. **This week:** write down your current price, the number of people on your waiting list, and your weekly hours. Price 3 to 5 local competitors.
2. **By 1 December 2026:** charge new clients 10 to 15% more. Email existing clients a 30-day notice for a smaller rise, starting in January 2027.
3. **Review at the end of February 2027.** Hire only if all three of these are true: you still have 10 or more dogs waiting at the new price, your profit covers roughly £350 to £400 a week of total staff cost, and you want to manage someone. If you hire, start with a part-time trial and get employer's liability insurance before their first day.

I didn't look up live sources for this answer. The wage, National Insurance and fine figures come from my knowledge, so check them on gov.uk before you rely on them.

</details>

Full meeting: [statements and cross-examination](meetings/20261103-202955-3e94.md)

## Question 11

**I run a small online clothing shop. Should I start offering free returns?**

| | Board | Opus alone |
| --- | --- | --- |
| Usefulness | 9.0 | 8.0 |
| Accuracy | 8.0 | 8.0 |
| Risk spotting | 9.0 | 8.0 |
| Clarity | 7.0 | 9.0 |
| **Winner** | Board | |

Judge, board shown first (A is the board): "A wins narrowly: it gives a correct break-even calculation, keeps the trial clear of distorting holiday returns and sets explicit keep-or-stop thresholds, though B is clearer and adds the useful idea of fixing sizing first."

Judge, Opus shown first (A is Opus alone): "B adds a correct break-even calculation, concrete success criteria and test-design warnings such as delayed holiday returns and too few orders, which make it more actionable than A, though A reads more cleanly."

<details>
<summary>Board answer (678 words)</summary>

#### Decision
Do not switch on blanket free returns now, and do not make them a headline promise. First measure your real return rate, margin and label cost. Then trial free size exchanges (refunds stay paid) for 12 weeks from Monday 1 February 2027. Keep the exchanges only if margin per order holds and orders rise clearly.

#### Why
- **The law doesn't require free returns.** Under the Consumer Contracts Regulations 2013, a customer can charge back return postage to you only if you didn't tell them before purchase that they pay it. Free returns are a choice you'd be paying for.
- **The cost is bigger than the label.** You pay postage (roughly £2.24 to £5.22 plus VAT per label, undated reseller rates), handling time and the loss on stock you can't resell. Free returns also invite customers to order two sizes and send one back, so your return rate rises. Each extra return loses the margin on that sale.
- **You need a big sales lift to break even.** At a £40 order and about £1.80 of return cost per order, you need roughly 10% more orders at a 50% margin. At a 30% margin you need roughly 18%. No source the board found shows a lift that big for a small shop.
- **Big UK fashion retailers are moving the other way.** Between 35% and 79% of top UK fashion brands now charge for returns. Both figures come from vendors and their samples differ.
- **Exchanges get most of the benefit for less risk.** The main thing stopping people buying clothes online is worry about fit. A free size swap removes that worry without paying for people who just change their minds.

#### Main risks
- **Margin loss.** Your return rate rises faster than your sales, and you only see it after a quarter.
- **Hard to undo.** Withdrawing a public promise looks like a downgrade and draws bad reviews.
- **Misleading results.** Holiday returns arrive 2 to 4 weeks late, so a test that ends in January would make free returns look better than they are. A small shop may also not get enough orders to tell a real change from noise. Aim for at least a few hundred orders in each period.
- **Legal.** You must always refund the original standard delivery charge. If your terms don't clearly say the customer pays return postage, you may already owe it. Showing different return terms to different visitors could be a problem under the DMCC Act 2024. The board is unsure, so compare before and after instead.
- **Fraud.** Some customers will return worn items or swap in different ones.

#### Honest criticism for the owner
You're asking about a policy whose answer depends entirely on three numbers you didn't give: your return rate, your margin and your cost per return. If you don't know them offhand, that is the first problem to fix, whatever you decide. Also, don't count your own hours as free. Value them at least at the National Living Wage.

#### Next steps
1. **By 14 November:** pull 12 months of data: orders, average order value, gross margin, return rate and return reasons. Check that your terms clearly say who pays return postage.
2. **By 28 November:** get return label quotes from Royal Mail, Evri and DPD. Check the returns policies of your five closest rivals.
3. **1 February to 25 April 2027:** run free exchanges, or free returns over £50. Measure returns until 23 May. Continue only if orders rise at least 10%, the return rate stays within 3 points of today, and margin per order holds.

#### Board notes
- I overruled Advocate on making free returns a headline promise. It can't be withdrawn cleanly, and Advocate gave no numbers to support it.
- I overruled Scout's point that current returns aren't new cost. If customers pay for postage today, every free label becomes a new cost to you.
- I moved Operator's test out of the Black Friday and January period, because late returns would distort the results.

</details>

<details>
<summary>Opus alone (598 words)</summary>

#### Decision
Don't offer free returns on everything yet. Start with free exchanges, or free returns only on orders over a set amount, and run it as an 8-week test. You haven't given me your margins, order values or return rate, so I can't say whether full free returns would pay for itself. You need those numbers first.

#### Main risks
- **The cost is bigger than the postage label.** A worked example with assumed figures: average order £40, 25% return rate, £3.50 return label, £2 of your time to process each return. That comes to about £1.38 on every order you sell, or roughly 3.4% of revenue. Items that come back damaged or unsellable cost you more on top.
- **More people will return things.** Clothing return rates online are often quoted at 20% to 30%. Free returns usually push that up because people order several sizes and send most back. I can't tell you how much it would rise for your shop.
- **"Wardrobing."** Some people wear an item once and send it back. Small shops feel this more than big ones.
- **It's hard to undo.** The big UK chains went the other way. Zara (2022) and ASOS (2023) started charging for some returns because free returns hurt their profits. Customers notice when a shop takes a perk away.
- **The law already gives customers a lot.** Under the Consumer Contracts Regulations 2013, online buyers can cancel within 14 days of delivery. They then have another 14 days to send items back. You must refund the item and the standard delivery cost. You can make them pay return postage, but only if you told them clearly before they bought. So free returns is an extra on top of their legal rights, not a requirement.

#### Honest criticism for the owner
- You're asking about a policy without your own numbers. The answer depends almost entirely on your gross margin, average order value and current return rate. If you don't know those three numbers off the top of your head, sort that out first.
- You may be trying to fix the wrong problem. If customers hesitate to buy, the cause may be poor sizing info, unclear photos or no fabric details. Free returns doesn't fix any of those. A good size guide lowers returns. Free returns raises them.
- You probably can't win on returns against ASOS or Next. Small shops tend to win on product, service and trust. A quick, friendly exchange process may get you most of the benefit for less cost.
- Check that your current returns policy is actually stated clearly at checkout. If it isn't, you may already have to pay return costs you think customers are covering.

#### Next steps
1. **This week:** pull 6 to 12 months of data. Get your return rate, the top reasons for returns, average order value and margin per order. Work out what one return costs you all in.
2. **Within 2 weeks:** fix the biggest return reason. If it's sizing, add garment measurements in cm and "model is 5ft 8in, wears size 10" style notes.
3. **Then test for 8 weeks:** offer free exchanges, or free returns on orders over about £50 (set this a little above your average order value). Compare conversion rate, order value and return rate against the previous 8 weeks. Keep the change only if your extra profit is bigger than your extra return costs.

I haven't checked current Royal Mail or Evri return label prices. Treat £3.50 as a rough guess and look up the real rate.

</details>

Full meeting: [statements and cross-examination](meetings/20261103-203137-64a6.md)

## Question 12

**I'm a freelance designer. Should I raise my day rate from £300 to £400 for every client, including long-standing ones?**

| | Board | Opus alone |
| --- | --- | --- |
| Usefulness | 8.5 | 8.0 |
| Accuracy | 8.0 | 8.0 |
| Risk spotting | 8.5 | 8.5 |
| Clarity | 7.0 | 8.0 |
| **Winner** | Tie | |

Judge, board shown first (A is the board): "Both give a sound, staged plan with correct break-even and VAT maths. B edges ahead with sharper practical insights: the VAT cost for clients who can't reclaim it, the booked-capacity test, project fees and a lock-in offer. A is weighed down by meta analyst notes and minor wording slips."

Judge, Opus shown first (A is Opus alone): "B gives a clearer income-share threshold for exceptions, a worked break-even example, caveated market figures, and sharper contract and budget-cycle risks, though its analyst notes add some clutter and unexplained income figures."

<details>
<summary>Board answer (691 words)</summary>

#### Decision
Yes, move to £400. Charge it to all new clients from today. Move existing clients to £400 from 1 February 2027, with written notice sent by 20 November 2026. The one exception: any client worth more than 25% of your income gets £350 until 30 June 2027, then £400. Only do this once you have checked your contracts and your client concentration.

#### Why
- **The numbers favour the rise.** Going from £300 to £400 is a 33% increase. You earn the same gross income even if you lose 25% of your billed days. At 150 days a year (£45,000 now), you could lose 37 days and still not be worse off.
- **£400 is within the market range.** Published figures put your current £300 at or just below typical rates for graphic work. Senior graphic designers are listed at £280 to £400, and one contract median is £350. UX work pays well above £400. These are rough figures, mostly vacancy rates and blogs, and I don't know your specialism.
- **Loyalty is not a reason to undercharge.** It is a reason to give long notice and to protect your biggest relationships. It is not a reason to keep long-standing clients at £300.
- **Charging everyone £400 on one date is the weak version.** The most likely way this fails is that one large client walks, you have no work lined up to replace it, and you end up discounting to fill your diary. Protecting only your largest clients costs about £50 a day on a small share of your days, for five months.

#### Main risks
- **Contracts.** If a signed contract or agreed quote fixes your rate, notice alone does not change it. You need the client's agreement or the contract's own change terms.
- **Concentration.** One client worth 40% of your income leaving takes you past the 25% break-even on its own.
- **Gaps in your pipeline.** Lost days only cost you if you can't refill them. Nobody gave reliable figures on how long that takes.
- **Quiet cuts.** Clients may accept £400 but book fewer days or pass small jobs to someone cheaper. You won't see this for about a quarter.
- **Budgets.** Some clients set annual budgets, often for an April or January year. A rise they didn't plan for is easier to refuse. Check each one.
- **VAT.** The registration threshold is £90,000 of turnover over a rolling 12 months (unchanged since April 2024, as far as the board knows). At £400 a day you cross it at about 225 billed days. Check if you work more than 200 days a year.

#### Honest criticism for the owner
You asked about the rate before you know the three facts that decide it: your billed days, each client's share of your income, and how many months of savings you have. "Every client, the same day" is a blunt tool. The risk is not the rate itself. The risk is how much depends on one or two clients, and none of the board could see that.

#### Next steps
1. **By 6 November:** list every client with the days billed and their share of income over the last 12 months. Read each contract for fixed rates and notice terms.
2. **From today:** quote £400 to all new enquiries.
3. **By 20 November:** write to existing clients. Give one reason and one effective date (1 February 2027). Clients above 25% get the £350 step instead. Review on 1 May 2027: count lost clients and days booked against the same period last year.

#### Board notes
- I overruled the Advocate's 30 days' notice. It is too short for clients of two years or more.
- I overruled the Scout's two-step rise for every client, because it means two rate conversations with each one. I also used the Scout's correction of the Operator's early income estimates. Expect about £11,700 over the first three months, not £12,200.
- The Operator used two different cut-offs for "large client" (20% and 30%). I set it at 25% because that matches the break-even point. This is a judgement call, not evidence.

</details>

<details>
<summary>Opus alone (575 words)</summary>

#### Decision

Yes, move to £400, but do it in two steps rather than one. New clients should pay £400 from today. Long-standing clients should get written notice now and move to £400 from 1 February 2027. Your top one or two clients can be the exception: offer them £360 to £375 for 2027 if losing them would really hurt. A 33% jump for everyone overnight risks too much at once.

#### Main risks

- **Losing your biggest client.** If one client is over 30% of your income, a 33% rise could push them to look elsewhere. At £400, you can lose 25% of your billable days and still earn the same. Lose more than that and you are worse off.
- **Quiet churn.** Long-standing clients often won't argue. They just send less work. You may not see it for 3 to 6 months.
- **Breaking your own contracts.** Some of your agreements may fix rates or require notice. Check each one before you send anything.
- **VAT.** I believe the UK VAT registration threshold is still £90,000 of turnover in any rolling 12 months, but check gov.uk. At £400 a day, 225 billable days takes you past it. Registering adds 20% to bills for clients who can't reclaim VAT, such as small charities or sole traders. That is a hidden second rise for them.
- **What I don't know.** I don't know your discipline, your location, how fully booked you are, or how your clients are spread. All of these change the answer. I haven't checked current market rates. I'd guess £400 is mid to upper range for an experienced UK freelance designer outside London, but treat that as a guess.

#### Honest criticism for the owner

- **"Every client, same rate" is lazy pricing.** Your clients don't all get the same value from you. A client who pays on time, briefs well and sends steady work is worth more than £300 a day of hassle. A blanket rule ignores that.
- **You're asking the wrong question first.** The real test is whether you're turning work away or are booked more than 80% of the time. If yes, you're underpriced and £400 may still be low. If you have gaps, raising rates won't fill them.
- **Day rates cap your income.** If you mostly do defined pieces of work, such as a brand identity or a website, quoting a project fee is often worth more than any day rate. Clients compare day rates. They rarely compare project fees.
- **Loyalty is not a reason to discount forever.** Long-standing clients have probably been on £300 for years while your costs and skills went up. A fair rise with notice is normal business. Don't apologise for it.

#### Next steps

1. **This week:** List every client with their revenue over the last 12 months, the share of your income it represents, and any notice terms in their contract. That shows which clients you can't afford to lose.
2. **By 30 November 2026:** Email existing clients. Give them at least 8 weeks' notice of £400 from 1 February 2027. Give one sentence of reasons, such as experience or results delivered. Offer to lock in a block of days at the old rate if they book before the change.
3. **From now:** Quote £400 or a project fee to every new enquiry. Track how many say yes. If over 70% accept without pushback, test £450 in mid 2027.

</details>

Full meeting: [statements and cross-examination](meetings/20261103-203320-c2b5.md)

## Question 13

**Our family restaurant gets complaints about slow service on Saturdays. Should we cut the menu in half?**

| | Board | Opus alone |
| --- | --- | --- |
| Usefulness | 8.0 | 7.5 |
| Accuracy | 8.0 | 6.0 |
| Risk spotting | 9.0 | 6.5 |
| Clarity | 7.0 | 8.0 |
| **Winner** | Board | |

Judge, board shown first (A is the board): "Both diagnose before cutting, but A uses the correct current £12.71 wage, flags its weak evidence, and catches the allergen-record and December-distortion risks, while B relies on an outdated £12.21 rate despite its useful sales-data guidance."

Judge, Opus shown first (A is Opus alone): "B gives the same sound diagnose-first advice but adds stronger risks (allergen records, December distortion), a free staggered-booking fix and a clear pass mark, and uses the current £12.71 wage where A cites the outdated £12.21, though B has a typo ('one family analysts') and is a little longer."

<details>
<summary>Board answer (646 words)</summary>

#### Decision
Don't cut the menu in half. First, time every stage of three Saturday services and read what the complaints actually say. If the kitchen turns out to be the bottleneck, trial a shorter menu on Saturdays only, dropping just the slow, low-selling dishes, and keep the full menu Monday to Friday.

#### Why
- **The cause is unknown.** Slow Saturdays often start outside the kitchen: seating everyone at once, too few floor staff, drinks, or the bill. A smaller menu only fixes a kitchen bottleneck.
- **A full cut is out of proportion.** The problem is on one day, but halving would change all seven.
- **"Half" is a guess.** The right cut could be 3 dishes or 15. Only timings and till data can tell you which.
- **The evidence is thin.** The best example is Chili's, which reported ticket times 12% faster after a big menu cut. That is the company's own figure, with nothing to compare against, from a large chain. There is no independent research for a family restaurant.
- **A trial can be undone. A permanent cut is hard to undo.** Regulars who lose their favourite dish may not come back.

#### Main risks
- **Misdiagnosis.** You lose dishes and Saturdays stay slow. This is the most likely way it fails.
- **Losing regulars quietly.** People who stop coming rarely leave a review, so you won't see it.
- **Allergen records.** The Food Information Regulations 2014 require accurate allergen information for every dish. A second Saturday menu means a second record to keep correct, and more chance of staff mistakes.
- **Money.** Reprinting, updating booking sites and writing off stock should cost about £50 to £300, though nobody has itemised this. An extra Saturday hire at the £12.71 per hour National Living Wage, plus employer National Insurance and holiday pay, costs about £115 to £125 for an 8-hour shift.
- **Waiting too long.** Every slow Saturday adds more bad reviews, and those take a long time to recover.

#### Honest criticism for the owner
You jumped to a fix before checking the cause. You are treating "slow service" as "slow kitchen" without evidence. You also chose "half" because it is a round number, not because anything measured it. A family restaurant runs on its regulars, so a cut you can't easily reverse is the wrong first move.

#### Next steps
1. **Saturdays 7, 14 and 21 Nov: time every table.** Have one family member with a phone stopwatch record four times: seated, ordered, food out and bill paid. Ask the cooks which dishes are slowest or clog one station, such as the fryer or grill. Pull your top sellers from the till.
2. **Sat 28 Nov, if seating or the floor is the problem: stagger bookings.** Space arrivals 15 minutes apart. It costs £0 and changes no dishes. Make no menu changes in December, because Christmas parties will distort any results.
3. **Saturdays 9 to 30 Jan 2027, only if the kitchen is the bottleneck: run a 4-week trial.** Use a Saturday-only menu that drops the slow, low-selling dishes and keeps every top seller and regulars' favourites. Write down the pass mark before you start: time from order to food down at least 15%, and Saturday covers and spend per head not down.

#### Board notes
- I overruled the Advocate's fixed-price Saturday set. It raises prices on the day people already complain, and it lengthens each visit. It also changes several things at once, so you couldn't tell what worked.
- I overruled the Advocate's call to test in December. Christmas party bookings make the comparison unreliable, and peak trade is too valuable to put at risk.
- Open question: whether the 30 to 40% cut the Operator suggested, or the 20 to 30% the Scout suggested, is right. Your timing data should decide it, not either number.

</details>

<details>
<summary>Opus alone (572 words)</summary>

#### Decision
Don't cut the menu in half yet. First spend two Saturdays finding out where the delay actually happens. If the kitchen is the bottleneck, try a Saturday-only menu with about 30% fewer dishes for four weeks, and measure the result before making it permanent.

#### Main risks
- **Fixing the wrong problem.** Slow service often comes from too few front-of-house staff, a slow till, or tables not being turned quickly. It isn't always the number of dishes. If the kitchen isn't the bottleneck, halving the menu will cost you customers and leave service just as slow.
- **Losing regulars.** In a family restaurant, people often come back for one specific dish. Cut it and some of them won't return. You won't see that in complaints. You'll see it in fewer bookings.
- **Lower average spend.** Fewer choices can mean fewer starters and sides ordered. I can't estimate how much without your sales data.
- **Weekday knock-on.** Cutting the whole menu to fix one day's problem hurts the other six days.
- **Upside you might miss.** A tighter menu can cut food waste and prep time. That is a real benefit. You should only bank it if your data shows those dishes barely sell anyway.

#### Honest criticism for the owner
- You've jumped to a solution before diagnosing the problem. "Slow service" could mean slow to be seated, slow to order, slow food, or slow to get the bill. Each one has a different fix.
- "Cut it in half" is a round number, not a decision based on evidence. The right number of dishes to cut might be 5, or it might be 15. Your sales records will tell you.
- Saturday is probably your busiest day, so some waiting is normal. The real question may be whether you're short-staffed or overbooked on Saturdays, not whether the menu is too long.
- I don't know your menu size, covers, staffing or kitchen layout. So treat this as a framework, not a verdict.

#### Next steps
1. **Time the service on the next two Saturdays (7 and 14 November 2026).** For 20 tables, write down four times: when they're seated, when they order, when food arrives, and when they pay. In the UK, a main course arriving more than 20 to 25 minutes after ordering usually feels slow to customers. Whichever gap is longest is your problem.
2. **Pull 8 to 12 weeks of sales by dish from your till system.** Rank every dish by how often it's ordered and how much profit it makes. Also mark the dishes that take longest to cook or need a special station. The cut candidates are dishes that sell little, take a long time, or use ingredients nothing else on the menu uses. They are not simply the bottom half of the list.
3. **If the kitchen is the bottleneck, trial a Saturday menu with 25 to 35% fewer dishes for four weeks.** Keep your top sellers and anything regulars ask for by name. Track ticket times, complaints, average spend per head and covers against the previous four Saturdays. If the front of house is the bottleneck instead, try one extra server from 6pm to 9pm before you touch the menu. At the National Living Wage of £12.21 an hour, that's roughly £40 to £45 a night including employer costs. The rate may rise from April 2027, so check it before you budget.

</details>

Full meeting: [statements and cross-examination](meetings/20261103-203441-1379.md)

## Question 14

**Should I take a six-month unpaid career break to travel, using about £12,000 of my savings?**

| | Board | Opus alone |
| --- | --- | --- |
| Usefulness | 8.0 | 7.0 |
| Accuracy | 6.5 | 6.5 |
| Risk spotting | 9.0 | 7.0 |
| Clarity | 7.0 | 8.0 |
| **Winner** | Board | |

Judge, board shown first (A is the board): "A covers more of the risks that matter, including visa rules on remote work, landlord consent for subletting and continuous employment, though its £21–£40 daily figure is miscalculated and its deadlines are out of order; B is clearer and flags the missing facts but misses the legal risks and understates the cost of voluntary NI."

Judge, Opus shown first (A is Opus alone): "B covers more of the risks that matter (no legal right to unpaid leave, loss of continuous employment, subletting breaching a tenancy, illegal remote work on a tourist entry) and gives a clearer go/no-go structure, though its £21–£40 daily figure is miscalculated (closer to £15–£27) and its deadlines are listed out of order."

<details>
<summary>Board answer (702 words)</summary>

#### Decision
Go only if you get unpaid leave in writing with a guaranteed return date, or if you have savings beyond this £12,000. If you would have to resign and £12,000 is your whole safety net, don't go for six months. Take a trip of about three months instead, or wait until you have saved more.

#### Why
- **The return is the real risk, not the trip.** With an agreed return date, the downside is small and you can undo it. If you resign, you could come home with almost nothing left and spend months looking for work.
- **£12,000 is less than it looks.**
  - Over 182 days it is £66 a day.
  - Flights, insurance, vaccines and visas probably take £2,200 to £4,500 before you leave. These are estimates, not quotes.
  - Bills at home keep running. Rent of £800 a month comes to £4,800.
  - With both of those taken off, you have roughly £21 to £40 a day. That is only enough for budget travel in Southeast Asia or Latin America.
- **Your full cost is bigger than the cash you spend.** You also give up six months of salary, plus roughly £430 to £875 of employer pension contributions. Interest you lose on the savings is minor, under £300.

#### Main risks
1. **No job to come back to.** UK employees have no legal right to unpaid leave or a sabbatical. Your employer can say no. Resigning also resets your continuous employment, which affects redundancy pay and unfair dismissal protection.
2. **Coming home with no buffer.** If you spend all £12,000, one slow job search or one emergency at home leaves you overdrawn.
3. **Housing.** Subletting without your landlord's written consent can breach your tenancy. Paying rent on an empty home may eat 30% to 40% of your money.
4. **Working illegally.** Remote work while on a tourist entry usually breaks visa rules, even for a UK client. It can also raise tax residence questions. Working holiday visas are the legal route for Australia, New Zealand and Canada (usually up to age 35) and Japan (up to 30). Check that you qualify.
5. **Insurance gaps.** Policies often exclude pre-existing conditions and adventure sports. A hospital stay that isn't covered can cost five figures.
6. **National Insurance.** This is a small risk. If you earned above about £6,500 earlier in the tax year, you probably still get a qualifying year. Rules on paying voluntary contributions from abroad changed in April 2026. Check yours at gov.uk/check-national-insurance-record.

#### Honest criticism for the owner
You have framed this as "£12,000 of savings". The real questions are whether you have a job to return to and what you will have left when you land. Neither is answered yet. Also, "six months of travel" is not a budget. Without a route and a daily spending cap, trips commonly run 15% to 25% over.

#### Next steps
1. **By 30 Nov 2026:** ask HR for unpaid leave in writing. Ask for your role, salary, return date, and whether pension contributions continue. Do not resign before you have an answer.
2. **By 17 Nov 2026:** write down your monthly costs at home. Check whether your lease allows subletting or ending it early, then set a daily budget for your chosen countries with 20% added for overruns.
3. **By 15 Dec 2026:** make the go or no-go decision.
   - **With written leave:** go, and keep at least £3,000 back, more if your rent is high.
   - **Without it:** plan a trip of about three months, or keep saving.

#### Board notes
- I overruled the Skeptic's figures for pension loss (£900 to £1,500) and all-in cost (£25,000 to £35,000). The pension figure was a full year's worth, and the all-in total counted some costs twice.
- I overruled the Advocate on paying for the trip with remote work along the way. It is usually illegal on a tourist entry. The claim that a gap helps your career had no evidence behind it.
- Still open: how big your reserve should be. The Operator suggests £3,000 and the Skeptic six months of costs. Six months is safer if you resign. £3,000 is enough with guaranteed leave.

</details>

<details>
<summary>Opus alone (562 words)</summary>

#### Decision
Yes, take it, but only if two things are true. First, your employer agrees the break in writing with a guaranteed return date and role. Second, you still have at least 3 to 6 months of living costs saved after spending the £12,000. If either is false, delay it 6 to 12 months and fix that first. You haven't told me your total savings, debts, job security or housing costs, so this is a conditional yes, not a firm one.

#### Main risks
- **The real cost is more than £12,000.** Six months unpaid means you also lose six months of net salary. On a £35,000 salary that is roughly £13,000 after tax. You also lose employer pension contributions, often £500 to £1,500 over six months.
- **UK costs keep running.** Rent or mortgage, council tax, phone, subscriptions and storage don't stop. If they come to £1,000 a month, that's £6,000 of your £12,000 gone before you've travelled.
- **£12,000 may not cover where you want to go.** £2,000 a month for everything works in Southeast Asia or much of South America. It's tight in Western Europe, Australia, Japan or the US.
- **Coming back is risky.** "Unpaid leave" is not always a protected right in the UK. A role can be restructured while you're away. If you resign instead, finding a new job could take 2 to 4 months or longer, depending on your field.
- **National Insurance.** You may still get a qualifying year for your State Pension if you earn enough in the rest of the tax year. I'm not certain how your dates fall across tax years (6 April to 5 April). Check your record on GOV.UK. Filling a gap with voluntary contributions usually costs a few hundred pounds.
- **Insurance and health.** Normal annual travel policies often cap trips at 31 to 90 days. You need a long-stay or backpacker policy, likely £200 to £600 depending on age and destinations.

#### Honest criticism for the owner
- You're framing this as "£12,000 of savings". The honest figure is £12,000 plus lost salary plus lost pension, probably £25,000 or more in total. That can still be worth it, but decide on the real number.
- You haven't said what the break is for. Rest, burnout, a career change or a bucket list each point to different plans. If it's burnout, a shorter break or a job change might fix the actual problem more cheaply.
- If you've already decided and want permission, notice that. Then the useful question is how to do it safely, not whether.
- If your total savings are under about £20,000, spending £12,000 leaves you exposed to job loss, illness or a big bill when you get back.

#### Next steps
1. **This week:** Ask HR or your manager for a formal sabbatical or career break agreement. Get in writing your return date, your role, your pension position and whether your benefits continue.
2. **Within two weeks:** Write a monthly budget with two columns, UK fixed costs and travel costs, for each country. If the total goes over £12,000, cut destinations or let/sublet your home. Keep a separate untouched buffer of at least 3 months of expenses.
3. **Before booking:** Check your National Insurance record on GOV.UK. Then get quotes for long-stay travel insurance that covers every country and activity you're planning.

</details>

Full meeting: [statements and cross-examination](meetings/20261103-203609-f4f0.md)

## Question 15

**Should I buy an electric car now or wait two more years?**

| | Board | Opus alone |
| --- | --- | --- |
| Usefulness | 8.5 | 7.5 |
| Accuracy | 8.0 | 7.0 |
| Risk spotting | 9.0 | 7.5 |
| Clarity | 8.0 | 7.5 |
| **Winner** | Board | |

Judge, board shown first (A is the board): "A wins narrowly: it costs out the trade-off between depreciation and running-cost savings, and it covers insurance and lease risks. B adds sources and the charger grant, but its risk section mixes in speculation and items that aren't really risks."

Judge, Opus shown first (A is Opus alone): "B ties the timing to the condition of the current car, quantifies running-cost savings against depreciation with figures that check out, and covers more of the risks that matter (insurance, lease costs, battery warranty, grant funding), while A is accurate but less specific."

<details>
<summary>Board answer (626 words)</summary>

#### Decision
Don't time this around the EV market. Time it around your current car. If it is reliable, keep it and buy an EV when it actually needs replacing, whether that is in 2026 or 2029. If it needs replacing within about 12 months and you can charge at home, buy now. A one to three year old used EV usually gives the best value; a grant-eligible new car is the alternative.

#### Why
- **Waiting gains you little.** The 3p per mile road charge starts in April 2028 and applies to every EV, so waiting does not avoid it. The Electric Car Grant (up to £3,750 on new cars under about £37,000) is reported to run to March 2030. Used EV prices have already fallen a lot.
- **Running costs can save real money.** At 8,000 miles a year, petrol costs about £1,130. An EV charged on a home overnight tariff (about 8p per kWh) costs about £200. After the roughly £240 a year road charge from 2028, the net saving is about £700 a year. On a standard 25p tariff it is about £300.
- **Depreciation is larger than those savings.** A new EV can lose £5,000 to £7,000 in its first years. That is why swapping a working car early does not pay. It is also why used is usually the better buy.

#### Main risks
- **No home charging.** Public rapid charging costs 65p to 85p per kWh. At that price an EV costs more per mile than petrol. Without a driveway or a workable charger setup, don't buy.
- **Values are still falling.** Used EV prices were down about 10% year on year. Whoever owns the car takes the next drop. A lease is not free protection either: its price already includes expected depreciation, plus mileage caps and damage charges.
- **The grant could run out early.** "Runs to 2030" is not the same as "funded to 2030". The £650m pot covers about 173,000 cars. This only matters if you buy new.
- **Battery health on used cars.** Get a battery health report and check how much of the manufacturer's battery warranty is left. It is typically 8 years or 100,000 miles.
- **Insurance** is often higher for EVs. Get quotes before you commit.

#### Honest criticism for the owner
"Now or in two years" is the wrong question. You left out the four facts that decide it: your annual mileage, whether you can charge at home, the age and condition of your current car, and your budget. Each one can flip the answer. Waiting two years on purpose, while a car that needs replacing costs you in repairs, would be a mistake. So would replacing a sound car now.

#### Next steps
1. This week, write down four things: your annual mileage, whether you have off-street parking, your current car's age and likely repairs over the next 12 months, and your budget.
2. If you have off-street parking, get two charger installation quotes (about £800 to £1,200) and an overnight tariff quote.
3. If your car is due for replacement, check the official GOV.UK list of grant-eligible cars. Price two or three used EVs with a battery health report, and get insurance quotes for each.

#### Board notes
- I overruled the Advocate's claim that depreciation is "already priced in". Used prices are still falling.
- I overruled the Operator's "wait and buy used in late 2028" as a default. It avoids none of the policy changes, and it leaves out the old car's own repair costs and depreciation.
- Still open: whether the grant is funded to 2030, and the final road charge rate. Members were working partly from press reports and memory, so check both on GOV.UK.

</details>

<details>
<summary>Opus alone (568 words)</summary>

#### Decision
Buy now if two things are true: your current car needs replacing within about 2 years, and you can charge at home. If either is false, keep your current car and decide again in mid-2027. I don't know your mileage, budget or parking, so this answer is conditional. Waiting two years mostly costs you time and gains you little.

#### Main risks
- **Pay-per-mile tax.** From 1 April 2028 electric cars pay 3p per mile (eVED), rising with inflation from 2029. At 10,000 miles a year that is £300. Waiting does not avoid it, because it applies to every EV, whenever you bought it. Petrol fuel duty is roughly 5p to 6p per mile, so EVs should still be cheaper to run.
- **Grants.** The Electric Car Grant gives up to £3,750 off new EVs priced at or under £37,000. It has been extended to 2030, but the budget is fixed and models can be dropped from the list. I can't promise your chosen car will still qualify in 2028. The £500 home charger grant runs only until about March 2027 and is described as the final year.
- **Depreciation.** New EVs lose value fast. Better batteries in 2028 will hurt the resale value of a car bought now. Solid-state batteries are unlikely to be mainstream or affordable by 2028, though I'm not certain of that.
- **Public charging cost.** Without a home charger, rapid charging often costs 70p to 80p per kWh. That can make an EV cost as much to run per mile as petrol.

#### Honest criticism for the owner
- You are asking "now or later" without saying what problem the car solves. The real question is when your current car stops being worth keeping. Start there.
- "Wait for better tech" never ends. There will always be a better model in two years. Buying at the right time for your life matters more than buying at the peak of the technology.
- You may be leaving out used EVs. A 2 to 3 year old EV often costs 40% to 50% less than new. That one fact could matter more than any grant.
- You haven't told me your annual mileage. Low-mileage drivers (under about 6,000 miles a year) save little by switching, so keeping a paid-off car is often cheapest.

#### Next steps
1. **Run your numbers.** Write down your annual miles, whether you have off-street parking, and your budget. Compare EV running costs (home electricity on an EV tariff of about 7p to 8p per kWh, plus 3p per mile from 2028) against what you pay now for petrol.
2. **Check eligibility on GOV.UK.** See which cars currently qualify for the Electric Car Grant, and which band (£1,500 or £3,750). If you have a driveway, apply for the £500 charger grant before it closes in 2027.
3. **Price a used option alongside a new one.** Get a quote for one ECG-eligible new car and one 2 to 3 year old used EV, with a battery health report (state of health above 90%). Pick on total 4-year cost, not sticker price.

Sources:
- [MoneyWeek: Electric car grant extended until 2030](https://www.moneyweek.com/personal-finance/electric-car-grant-uk-government-scheme)
- [GOV.UK: charger grant press release](https://www.gov.uk/government/news/grant-boost-to-cover-almost-half-the-cost-of-installing-ev-chargers-for-households-and-businesses)
- [Westminster Brief: EV grants PQ](https://westminsterbrief.co.uk/archive/pq/125274)
- [What Car?: pay-per-mile tax set out](https://www.whatcar.com/news/pay-per-mile-tax-set-out-for-electric-car-drivers)
- [UK Tax Calculators: eVED explained](https://www.uktaxcalculators.co.uk/tax-news/2026/07/14/everything-you-need-to-know-about-electric-vehicle-excise-duty-eved/)
- [Electric Car Scheme: pay-per-mile update 2026](https://electriccarscheme.com/blog/pay-per-mile-road-tax-ev-update-2026)
- [Express & Star: EV pay-per-mile from 2028](https://www.expressandstar.com/lifestyle/cars/ev-drivers-set-to-face-pay-per-mile-scheme-from-2028-8797482)

</details>

Full meeting: [statements and cross-examination](meetings/20261103-203807-8288.md)
