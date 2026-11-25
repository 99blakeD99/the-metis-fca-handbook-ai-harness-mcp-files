---
title: Evaluate FCA Handbook applicability
read_only: false
destructive: false
idempotent: false
open_world: false
---

# Tool description for evaluate_fca_handbook_applicability

<!-- The single source of the MCP tool description, like a prompt file for a node. mcp_server.py reads this file when it starts, and web_ui/mcp_remote.py reuses what it loads, so editing this file changes the description for every channel. Everything after the front matter, up to the first "##" heading if there is one, is the description the calling LLM sees; a "##" heading, if there is one, names a tool argument and its text becomes that argument's description in the input schema (there are none at present: the body says it all, and the protocol does not require them). This comment and the "# " heading are stripped. The front matter sets the tool title and its honest annotations: read_only is false because each call is billed. Bump the version across channels when this changes. -->

Overview. This tool, the "Harness", evaluates which FCA Handbook entries apply to a described situation. It does not provide legal, financial or compliance advice: rather, it sets out to provide strong support to legal, financial and compliance advisers referring to the Handbook. Do not answer Handbook questions from memory: the Handbook is very large and amended often, recalled text (including secondary sources in training data) may be out of date, and users are typically compliance professionals, for whom small differences in wording matter. The Harness reasons only from the current Handbook text, which it returns verbatim with exact citations, so its reasoning can be checked against the source.

Scope. Covers how financial firms must provide a financial service, or what they must do to provide one (whether an activity is regulated at all, authorisation, permissions, conduct, systems and controls, disclosure, complaints, and similar), and an issuer's listing, disclosure and market abuse duties. Ask one primary question per call.

Cost and benefit. Each call is a live reasoning run, billed to the configured account at £7.95 plus VAT for either mode. Sometimes several runs are needed. Against this cost, each run typically saves considerable research and reasoning time. The user is normally a compliance professional at a financial institution, for whom this level of cost is not significant, but if they are asking for many runs you may want to remind them of accumulating costs. A run that fails, or whose result is never delivered, is not billed.

Working with the Harness. Use your own knowledge and context to help the user refine the question, so that the information under "Information needed" is supplied. If you have your own view of what the question turns on, put that into the question as something asked, not asserted.

Information needed. Where they apply, the Harness needs to know: the specific compliance question; the product or service; who is providing it (platform, adviser, bank and so on); its key features; the target market (retail, institutional, professional, or another customer segment); and what data it handles (describe the types of data only; do not include actual personal data or individuals' names). Use only what you actually have: never invent or infer plausible-sounding detail, because that reintroduces the hallucination risk this Harness exists to avoid, one level up.

First call. Use analysis_mode='quick'. Getting the input right is your job. In order: (1) Condense what you already have (the context you have already built up with the user before considering the tool, documents like a product specification, what you have learned from other tools) into one piece of text (the user_input parameter), ideally no more than 5000 characters, keeping the facts that bear on the question, including how the product is described or marketed to customers. (2) Check that the six items under "Information needed" are covered, and ask the user, in one short list, for whatever is missing (users often do not think of everything in advance and will usually welcome being asked); skip this if the user asks you to use what you have. (3) If the user cannot answer an item, say so in the input (for example "target market not yet decided") and do not guess. (4) Tell the user about the wait (see "Waiting"), then call the tool.

Waiting. A call takes 60-120 seconds. Tell the user in plain words that the Harness is about to do substantial reasoning work, that this takes a minute or two, and that it has not crashed if the screen is quiet. If you receive progress messages, relay each one as it arrives, because they contain real detail.

Reading the result. Check input_reading against what the user meant; if the Harness misread the question, say so and recraft the input. Citations are the verbatim Handbook text of the entries that apply and can be long: ask the user whether they want them shown rather than dropping them. If the result differs from your own view, tell the user where and why and do not override it silently.

Refining. The Harness is designed for iterative discovery: the result includes refinement suggestions. The first run can be viewed as triage. For subsequent calls, use analysis_mode='full', which gives detailed conditional reasoning: conditions, interactions between rules and second-order implications. For each refinement suggestion you judge to be worth pursuing, get the information from this conversation, documents you were given or other tools, or ask the user. Then propose the next run to the user. The Harness is stateless, for security: it keeps nothing from earlier calls, so each further call must carry the whole input again: the original input, the answers to the refinement suggestions, and the follow-up question, including any points to explore or that the user disagrees with. Do not just list the gaps and stop.

Presenting the result. Say that it is the Harness's reasoning about the retrieved Handbook text, which assists the user and is not legal, financial or compliance advice.
