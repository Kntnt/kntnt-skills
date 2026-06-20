# Caveman compression

Maximum meaning per token: strip every wasted word, lose zero meaning. This is the shared definition of "caveman" for the `/caveman` skill and `agents-md`; each skill applies it its own way. Three lists, plus one rule above all.

## CUT — noise, remove it

- Grammatical filler the language permits (English: articles `a` / `an` / `the`) where the sense survives without it.
- Filler words — *just*, *really*, *basically*, *actually*, *simply*, *of course* — and each language's equivalents.
- Hedging — *it might be worth*, *you could consider*, *I think*, *maybe*, *in general*.
- Pleasantries and weak connectors — *sure*, *certainly*, *happy to*, *however*, *furthermore*, *moreover*, *note that*.
- Preamble, restating the request, and closing recaps.
- Redundancy — *in order to* → *to*; collapse two sentences that say one thing into one; a pattern shown three times → shown once.

## KEEP — meaning, never drop it

Every fact, number, date, name, unit, monetary amount and term of art — and every meaning-bearing word: negations (*not*, *no*, *never*), quantifiers (*only*, *all*, *except*, *unless*), conditionals (*if*, *before*, *after*, *when*). Drop one of these and the facts change. Fragments and lists are fine; plain words beat fancy ones.

## VERBATIM — exact, never alter or abbreviate

Reproduce exactly, uncompressed: code (inline and fenced), commands, flags, file paths, config, identifiers, function and hook names, env vars, version numbers, URLs, error strings, quotes, math and formulas, tables, data, and Markdown / YAML structure (headings, list shape, frontmatter). Anything that must read exactly as written stays exactly as written.

## Scope and language

- Compress *wording*, not *content*. Never delete a fact to save tokens — that is curation, a different job, out of scope here.
- Preserve genre and register. When the text is a set form — an email, an essay, a legal clause, code, an article handed to you — keep that form's register; compress its prose, never convert its genre.
- Stay in the text's language. Apply each rule to that language's equivalents; never force one language's grammar onto another.

## The rule above all rules

Correctness beats brevity. If shortening would make a fact ambiguous, wrong, or genre-broken, keep the words.
