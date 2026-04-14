# Rollback Runbook

## Trigger Conditions
- Elevated API 5xx error rate for 5+ minutes
- Relayer writes entering persistent `dead_letter` state
- Authentication outage or token validation failures

## Rollback Steps
1. Route traffic to previous stable backend image tag.
2. Revert frontend to previous static bundle.
3. If DB migration introduced breaking changes, execute matching alembic downgrade.
4. Disable relayer writes by clearing `RELAYER_PRIVATE_KEY` and restarting backend.
5. Re-run smoke checks: `/health`, `/api/v1/auth/login`, `/api/v1/risk/{address}`.

## Post-Rollback
- Capture incident timeline and impacted requests.
- Export failed rows from `chain_jobs` and `ai_audits`.
- Open hotfix PR and rerun full CI matrix before redeploy.
