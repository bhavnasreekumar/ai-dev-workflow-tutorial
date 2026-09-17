# AI-Assisted Development Workflow Tutorial

This tutorial teaches you a professional development workflow by having you build and deploy a real project: an e-commerce sales dashboard.

You'll work through it in two parts:

| Part | What you do | Time |
|------|-------------|------|
| [Part 1: Setup](pre-work-setup.md) | Set up accounts, install tools, get your repo ready | 55–80 min |
| [Part 2: Build & Deploy](workshop-build-deploy.md) | Plan with [Superpowers](https://github.com/obra/superpowers) (a skills add-on for Claude Code), track work in `TASKS.md`, build with Claude Code, deploy live | ~3 hours |

**Your course sets the deadline and the submission channel.** Several courses use this tutorial, and it carries no due date of its own. Section 7 of Part 2 tells you what to have ready when you finish. Where to send it, by when, and how much of the tutorial is assigned all come from your course.

## Why this matters

Most working developers now build with a coding agent. In a March 2026 survey of 906 engineers by The Pragmatic Engineer, 95 percent used AI tools every week, and Claude Code was the most used. The field has settled on a name for doing this well: agentic engineering. Andrej Karpathy coined "vibe coding" for the casual version. He describes the professional one as writing a clear spec, supervising the agent's plan, reading its changes, and keeping a way to check the result. That list is this tutorial.

Claude Code, the tool you'll use throughout, is Anthropic's coding agent. Unlike a chatbot that suggests code for you to paste, it works in your terminal: it reads your project, edits files, runs commands, and debugs with you.

You're not here to become a software engineer. You're here to learn how to build things when your work calls for it: a dashboard, an automated workflow, a rough prototype. Those skills carry over whether you go into analytics, consulting, or product management.

AI is an amplifier, not a shortcut. For someone with judgment, it multiplies what they can do. For someone without it, it produces confident output with no one home to check it. The evidence is specific. In a January 2026 study, Anthropic gave 52 junior developers a new library to learn, half of them with AI help. The AI group scored 50 percent on a comprehension quiz against 67 percent for the others, and saved no time doing it. The students who kept up were the ones who asked the AI to explain, questioned its choices, and did their own debugging. The ones who fell behind handed everything over.

This tutorial is built for the first group, and every step asks you to read what the agent did, decide something, or explain it back. The workflow rewards curiosity and initiative: asking why, reading the diff, pushing back on a plan, changing your mind on the record. Bring those, and a coding agent multiplies what you can do.

Where those numbers come from: https://newsletter.pragmaticengineer.com/p/ai-tooling-2026 and https://www.anthropic.com/research/AI-assistance-coding-skills

## What you'll build

A Streamlit dashboard with KPI (key performance indicator) scorecards, a sales trend chart, and breakdowns by category and region. Streamlit is an open-source Python framework for building web apps from plain Python scripts.

```
┌─────────────────────────────────────────────────────────────┐
│                E-Commerce Sales Dashboard                    │
├────────────────────────────┬────────────────────────────────┤
│       Total Sales          │       Total Orders             │
│       $1,234,567           │       8,432                    │
├────────────────────────────┴────────────────────────────────┤
│                   Sales Trend (Line Chart)                   │
│    $                                                         │
│    │      ╱╲        ╱╲                                       │
│    │     ╱  ╲      ╱  ╲      ╱                              │
│    │    ╱    ╲    ╱    ╲    ╱                               │
│    │   ╱      ╲  ╱      ╲  ╱                                │
│    │  ╱        ╲╱        ╲╱                                 │
│    └──────────────────────────────────────────── time       │
├────────────────────────────┬────────────────────────────────┤
│    Sales by Category       │    Sales by Region             │
│    (Bar Chart)             │    (Bar Chart)                 │
└────────────────────────────┴────────────────────────────────┘
```

See the finished version: https://sales-dashboard-greg-lontok.streamlit.app/

The dashboard itself is straightforward. The point is the workflow you use to build it.

## The workflow

Every technology company uses a variation of this workflow. You'll experience the entire cycle:

```
┌─────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌────────┐
│   PRD   │ -> │   TASKS.md   │ -> │ brainstorming│ -> │writing-plans │ -> │  Code  │
│(written)│    │ (milestones) │    │ (design doc) │    │ (impl plan)  │    │(Claude)│
└─────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └────────┘
                                                                              │
┌─────────┐    ┌───────────┐    ┌─────────┐    ┌───────────────────────────────┐
│  Live!  │ <- │  Deploy   │ <- │  Push   │ <- │ executing-plans (TDD + commit)│
│(public) │    │(Streamlit)│    │(GitHub) │    │ on a feature branch           │
└─────────┘    └───────────┘    └─────────┘    └───────────────────────────────┘
```

1. **PRD** (Product Requirements Document): Start with a written specification of what to build
2. **TASKS.md**: Draft your milestones (the deliverables, with IDs like TASK-1) from the PRD into a Markdown board in your repo
3. **brainstorming**: A Superpowers skill that asks clarifying questions and produces a design document
4. **writing-plans**: A Superpowers skill that turns the design into a bite-sized implementation plan covering your milestones
5. **executing-plans**: A Superpowers skill that builds the feature with Claude Code, implementing each task (test-first where the plan flags it)
6. **Commit**: Save your changes with a meaningful message linked to the milestone ID
7. **Push**: Upload your code to GitHub
8. **Review and merge**: Read what the agent wrote, run Claude Code's `/code-review` on the branch, decide what to fix, then merge
9. **Deploy**: Make your dashboard publicly accessible

## Key concepts

**Traceability.** Every piece of code traces back to a requirement. When you commit, you include the milestone ID (like TASK-1) in the message, and because `TASKS.md` is versioned in the repo, `git log` shows the whole chain from requirement to code to deployed feature.

**Skill-driven development.** Instead of jumping straight to code, you let Claude's Superpowers skills run a structured process: brainstorming explores what to build, writing-plans turns that into a bite-sized plan, then executing-plans implements task by task, using TDD on the tasks the plan flags for it (test-driven development: write a failing test first, then the code to pass it). This prevents the most common failure mode: building the wrong thing fast.

**AI as a partner.** Claude Code isn't just a code generator. You set the direction and make the judgment calls; it supplies the speed and technical know-how, and explains its reasoning so you learn as you go. You also review what it wrote before it ships, because you own what you ship.

## What you need

- Basic Python knowledge (if you've used pandas or written a few scripts, you're fine)
- A computer running macOS or Windows
- No prior experience with Git or AI coding tools
- A Claude Pro subscription, or a ChatGPT subscription if you already have one. The tutorial is written for Claude Code. If you already pay for ChatGPT, which includes OpenAI's Codex, follow the [Codex companion](codex-companion.md) at the marked points instead of buying a second subscription. The workflow is the same on both.

## Where to start

Open [pre-work-setup.md](pre-work-setup.md) and work through it first, then continue to Part 2.

## Project materials

| Resource | Description |
|----------|-------------|
| [E-Commerce PRD](prd/ecommerce-analytics.md) | The product requirements document you'll build from |
| [Sales data](data/sales-data.csv) | Sample dataset for the dashboard |
| [Codex companion](codex-companion.md) | For students on a ChatGPT subscription: what to do differently with OpenAI's Codex at each marked point |
| [Capstone tools](capstone-tools.md) | Appendix: Granola (meeting notes into Claude Code) and Wispr Flow (dictation), for the capstone, not this tutorial |

## License

This tutorial is provided for educational purposes.

## Run the sales dashboard

You need Python 3.11 or newer. From this project's directory, run:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
python -m pytest -q -W error
```

On Windows, replace the activation command with `venv\Scripts\activate`.
Open the local URL printed by Streamlit. Press Ctrl+C in the terminal to stop the server.

**ShopSmart Sales Dashboard** shows Total Sales and Total Orders, a monthly
sales trend, and category and region charts side by side. Hover over chart
points or bars to see exact dollar amounts. The supplied snapshot contains
482 transactions and $116,500.21 in sales from January 3–December 31, 2024.

The app reads `data/sales-data.csv` relative to `app.py`. Required columns are
`date`, `order_id`, `product`, `category`, `region`, `quantity`, `unit_price`,
and `total_amount`. Dates must use `YYYY-MM-DD`; quantity must be a finite
whole number, and prices and amounts must be finite numbers. Required cells
cannot be blank. IDs remain text, and extra columns are ignored.

Missing, empty, malformed, or invalid CSV input displays a clear error and
stops the app before any metrics or charts appear. Invalid rows are never
silently dropped. Sales use the recorded `total_amount`; orders count
transaction rows, including repeated IDs. Monthly totals keep years separate
and fill intervening months without sales with zero. Breakdown bars are sorted
by descending sales, with alphabetical ties.

This is a static data snapshot with no automatic refresh or date filters.
The tests cover validation and calculations, including the supplied CSV.
See the [verification record](docs/verification/sales-dashboard.md) for measured
results and outstanding browser and performance checks.

Task 1 environment: Python 3.14.7, Streamlit 1.64.0, Pandas 3.0.5,
Plotly 6.9.0, and pytest 9.1.1. These four package versions are pinned in
`requirements.txt`; `python -m pip check` reported no broken requirements.

## Review and deploy the sales dashboard

Deployment is the user-executed final step. Before deploying, finish M6's
outstanding browser and painted-frame performance checks in the
[verification record](docs/verification/sales-dashboard.md). Review the branch
changes with `git diff main...HEAD`, then follow the tutorial's
[review, merge, and push workflow](workshop-build-deploy.md). The deployment
handoff does not mean those checks or your review have been completed.

For code review, `sales_data.py` validates the CSV and computes the summaries;
`app.py` handles layout, chart formatting, and error messages. The tests check
the data rules and known sample results independently of the UI.

After merging and pushing the reviewed changes, confirm GitHub's `main` branch
contains `app.py`, `sales_data.py`, `requirements.txt`, and `data/sales-data.csv`,
and record the reviewed commit. The dependency file and CSV must be committed;
the local `venv/` is not deployed. Remote `main` has not yet been verified to
contain this implementation.

Use the [official Streamlit deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy):

1. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) with access
   to your GitHub repository, choose **Create app**, and choose your existing app.
2. Select repository `bhavnasreekumar/ai-dev-workflow-tutorial`, branch `main`,
   and entry point `app.py`.
3. In **Advanced settings**, choose Python **3.14**, matching the locally tested
   Python 3.14.7 major/minor version. If 3.14 is unavailable, test the pinned
   dependencies and app locally on an offered supported version before using it.
4. Deploy and inspect the build/runtime logs. Confirm dependency installation
   succeeds and the app reads the committed CSV.
5. Open the public URL in a private/logged-out browser window. Verify
   `$116,500.21`, `482` orders, twelve monthly points, five categories, four
   regions, descending bars, and working dollar/cents tooltips. Resolve errors
   before considering deployment complete.
6. Record the public URL, deployed Git commit, selected Python runtime, and
   hosted startup observations under M7 in [TASKS.md](TASKS.md). Keep hosted
   timings separate from local measurements. Then check M7's completed criteria
   and commit/push that board update through the tutorial workflow.
