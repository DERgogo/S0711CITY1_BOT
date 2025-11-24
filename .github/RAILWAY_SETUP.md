Railway deployment setup
=======================

Required GitHub repository secrets (set these in Settings → Secrets):

- `RAILWAY_TOKEN` — Railway deploy token (read/deploy permissions)
- `PROJECT_ID` — Railway project id
- `ENVIRONMENT_STAGING` — Railway environment id for staging
- `ENVIRONMENT_PROD` — Railway environment id for production
- `DEPLOY_HEALTHCHECK_URL` — Optional: public URL for smoke tests (e.g. `https://yourapp.example/ping`)

Implemented strategies
----------------------

- Strategy A: promote same commit from staging → production (implemented in `railway-deploy.yml`).
- Strategy B: copy environment variables from staging → production (script: `.github/scripts/railway_copy_envs.sh`).
	- The script attempts to use the Railway CLI (`railway variables list` / `railway variables set`). CLI flags vary by version; adjust the script for your CLI if needed.
- Strategy C: canary deployment helper and workflow (script: `.github/scripts/railway_canary.sh`, workflow: `railway-canary.yml`).
	- This performs a canary deploy to a separate environment and runs smoke tests; true traffic-splitting is not performed automatically — Railway's platform traffic control may require provider-specific configuration.

Security & Permissions
----------------------

• `RAILWAY_TOKEN` must have permissions to deploy and to read/write environment variables. For env-copying the token needs variable read + set rights.

Notes
-----
• These scripts attempt to be backwards-compatible with multiple Railway CLI versions by trying JSON output and falling back to text parsing. If the Railway CLI in your environment differs, edit the scripts in `.github/scripts/` to match the installed CLI.


Optional inputs to the workflow (when manually triggering):

- `strategy`: `A` (promote same commit), `B` (copy envs - not implemented), `C` (canary - not implemented)
- `release_id`: optional release id to rollback to (used by rollback helper)

Notes
-----

• The workflow `0711-Railway-Deploy` deploys automatically to staging on `push` to `main` and can be run manually.
• Strategy A (promote same commit) is implemented: deploy to staging → smoke test → deploy same commit to production.
• Strategies B and C are placeholders — they require provider-specific API calls and safer validation before being enabled.

Rollback
--------

• The rollback script attempts `railway releases:rollback <id>` if you provide a `release_id`. If not available, please use the Railway console to rollback.

Release tracking
----------------

• The workflows now capture the most recent release ID after deploys and expose them as Action outputs (`staging_release_id`, `prod_release_id`, `canary_release_id`).
• Artifacts `release-artifacts-<run_id>` are uploaded containing `*_release_id.txt` for traceability.

Live testing
-----------

• After setting the required secrets, trigger the workflows via GitHub Actions → `railway-canary.yml` (Run workflow) or push to `main` to trigger `railway-deploy.yml`.
• The workflows will attempt to use the Railway CLI. If your runner does not have the CLI, the scripts install it at runtime.

