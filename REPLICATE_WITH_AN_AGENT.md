# Replicate with an AI agent

Copy the prompt below into Hermes, Claude Code, Codex or another coding agent that can run a terminal and, ideally,
drive a browser. The agent prepares everything it is allowed to. **You** do the parts that need your identity:
registering with the survey archives, accepting their terms, and logging in to Hugging Face. No agent should accept a
licence or type a password for you.

What you can replicate today without a GPU: Paper A's committed tables and headline, and the Paper B manuscript's
number audit (every number in the PDF checked against the locked numbers table). Re-scoring or retraining adapters
needs a GPU and the model weights. Paper B's private Hugging Face artifacts are not public yet.

---

```text
You are setting up the SCA2_PofW research repository (EconLLM Lab) so that I can replicate the results in its
papers. Work step by step. Report what you ran and what it printed, and never invent output. Stop and ask me
whenever a step needs my account, a licence acceptance or a password. Do not accept terms, solve CAPTCHAs or
enter credentials yourself.

1. Clone the repository: git clone https://github.com/EconLLM-Lab/SCA2_PofW && cd SCA2_PofW
   Read README.md, DATA.md and replication/README.md before doing anything else.

2. Environment: use uv (https://docs.astral.sh/uv/) and no global pip installs. Create the project environment
   with `uv venv .venv --python 3.12`, then install the table-regeneration requirements with
   `uv pip install --python .venv/bin/python -r replication/requirements-tables.txt`.
   Run Python as `env -u PYTHONPATH .venv/bin/python ...`.

3. Data: DATA.md lists every third-party file, its official download page and the exact path where the code
   expects it. For each source:
   a. Open its download page (with your browser or computer-use tool, if you have one) and show me the page.
   b. Wait while I register, accept the terms and start the download myself.
   c. Once I confirm that the file is in my Downloads folder, move it to the path in DATA.md and print its size
      and sha256.
   The GPS country-level file alone is enough for Paper A's headline. Add WVS Wave 7 for the 42-country human map
   and Paper B. Never upload, commit or paste the contents of these files anywhere.

4. Our artifacts: if I want the adapter weights, ask me to run `hf auth login` and accept the gate at
   https://huggingface.co/Bonorinoa/SCA2-phase2-adapters. Then download at commit
   03c43dfd27c9535283feb78ffa727da3bfa1b966. The table replication below does not need the weights.

5. Replicate Paper A without a GPU:
   - Tier A: follow replication/README.md and check the committed artifacts against replication/HASHES.md.
   - Tier B: run `env -u PYTHONPATH .venv/bin/python analysis/phase2/reproduce_tables.py`. Confirm the trust
     adapter–GPS Spearman correlation of 0.74 [0.44, 0.88] on 16 countries by 23 items.

6. Paper B's manuscript audit: on branch paper/paper-b-draft, run
   `env -u PYTHONPATH .venv/bin/python misc/paper_b/tools/audit_numbers.py --out /tmp/NUMBER_AUDIT.txt` and report its RESULT line. It checks
   every number in the manuscript against planning/sprint_2026-10-11/paper-b-tier1/NUMBERS_TABLE.csv.

7. Finish with a table with one row per step: the command, its exit code, the key printed number and whether it
   matched. List anything that needed my action and anything that failed, with the error message.
```

---

If a step fails, the agent should report the exact error rather than work around it. A workaround can quietly change
what is being replicated.
