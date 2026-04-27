# Flow A Interview Q&A

## Why is Flow A needed?

It prevents unvalidated detection content from becoming deployable. Detection-as-code needs the same engineering discipline as application code.

## Why store changed files separately?

A CI summary says pass/fail, but changed-file inventory proves what was tested and why the branch was considered relevant.

## Why did metadata-only changes trigger CI?

Metadata controls mappings, ownership, OWASP category, ATLAS techniques, and expected rule IDs. Broken metadata can create wrong triage context even if Wazuh XML is unchanged.

## How does Flow A connect to Flow B?

Flow A applies `detection-ci-pass` when validation succeeds. Flow B checks this label as part of the deployment gate.
