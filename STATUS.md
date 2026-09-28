# NewsHub: status (2026-09-28, 09:40)

## Resume this Claude session

```bash
cd ~
claude --resume eb16802d-77b0-4f7b-bb68-6f9eecc43d91
```

Run it from your home folder (`~`). That's where the session started.

## Goal

News website in English and Turkmen:

```
n8n: every 3h → read RSS feeds → skip known URLs → Ollama summary (EN) → Turkmen translation → POST to Django
Django: stores articles, website with EN/TK switch, admin panel, API
```

## Progress

| Phase | Status |
|---|---|
| 0. Setup: n8n, models, Turkmen test | 🟡 partly done |
| 1. Django site + API + admin | ✅ done, 13 tests pass, pushed to GitHub |
| 2. n8n workflow | ✅ working with `qwen3:1.7b`: 55 articles from 11 feeds, runs every 3 hours, no duplicates |
| 3. Website polish | ⏸ (basic site already works) |
| 4. Auto-start at boot (systemd) | ⏸ |
| 5. Extras (daily digest, Telegram) | ⏸ |

## Installed

| Item | Status |
|---|---|
| Django 6.1.1 + DRF + feedparser | ✅ in `~/projects/newshub/.venv` |
| n8n 2.40.7 | ✅ start with `~/projects/newshub/n8n/run-n8n.sh` → http://127.0.0.1:5678 |
| Ollama 0.34.4 | ✅ running, uses MX350 GPU (2 GB) |
| `qwen3:0.6b` | ✅ downloaded (weak, but usable for testing) |
| `qwen3:1.7b` | ✅ downloaded, used by the workflow (~5 s per article) |
| `gemma3:4b` | ⏳ downloading (for the Turkmen translation test) |
| NLLB-200 translator | ⏸ not started (PyTorch download too slow; plan: use CTranslate2 instead) |

## Blockers

1. **Slow, unstable internet.** Speeds jump between 0 and 300 KB/s, both direct and through NekoRay. A faster connection (hotspot or other Wi-Fi) would finish the model download.
2. **Ollama doesn't use the proxy.** Its service has no proxy setting, so downloads stall. Fix (needs your password):
   ```bash
   sudo mkdir -p /etc/systemd/system/ollama.service.d && printf '[Service]\nEnvironment="HTTPS_PROXY=http://127.0.0.1:2081"\nEnvironment="NO_PROXY=localhost,127.0.0.1"\n' | sudo tee /etc/systemd/system/ollama.service.d/proxy.conf && sudo systemctl daemon-reload && sudo systemctl restart ollama
   ```
3. After turning the PC back on, **restart the download**:
   ```bash
   ollama pull gemma3:4b
   ```

## Django project

- Folder: `~/projects/newshub`
- GitHub: https://github.com/Dayanch437/newshub (branch `main`)
- Run: `cd ~/projects/newshub && .venv/bin/python manage.py runserver 127.0.0.1:8000` → http://127.0.0.1:8000/
- Admin login: create one with `.venv/bin/python manage.py createsuperuser`
- n8n API token: stored in the local database (not on GitHub). Print it with `.venv/bin/python manage.py setup_newshub`
- API docs: see `README.md`
- 11 RSS sources and 10 categories are already set up (edit them in the admin panel)
- Please review the Turkmen UI text: `news/ui_text.py` and category names in `news/management/commands/setup_newshub.py`

## n8n

- Workflow file: `n8n/newshub-workflow.json` (import with `n8n/run-n8n.sh import:workflow --input=n8n/newshub-workflow.json`)
- Flow: get sources from Django → read RSS → newest 5 per feed → skip known URLs → Ollama summary + category + tags → save to Django
- Always start n8n with `n8n/run-n8n.sh`. It sets `NO_PROXY=127.0.0.1`; without it, calls to Django go through NekoRay and fail with 503.
- Open http://127.0.0.1:5678 and create your n8n owner account the first time.
- The model name is set in the "Only new" node (`MODEL = 'qwen3:1.7b'`). A JSON schema limits the category to the 10 allowed values, and a keyword check in "Build article" sets central-asia.

## Next steps

1. Finish the `gemma3:4b` download.
2. After a reboot, start Django and n8n again (or do step 4 so they start by themselves).
3. Test Turkmen translation quality: `gemma3:4b` vs NLLB. You pick the better one.
4. Set up auto-start for Django and n8n.
