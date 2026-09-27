# NewsHub

News website in English and Turkmen. n8n collects and summarizes news, then sends it here through the API.

## Run

```bash
cd ~/projects/newshub
.venv/bin/python manage.py runserver 127.0.0.1:8000
```

- Site: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/ (create a login with `.venv/bin/python manage.py createsuperuser`)

First-time setup (safe to rerun, prints the n8n token):

```bash
.venv/bin/python manage.py migrate
.venv/bin/python manage.py setup_newshub
```

## API

All requests need the header `Authorization: Token <token>`.

| Method | URL | Purpose |
|---|---|---|
| GET | `/api/sources/` | Active RSS feeds (manage them in admin) |
| POST | `/api/articles/check/` | `{"urls": [...]}` → `{"new": [...]}`, the URLs not stored yet |
| POST | `/api/articles/` | Create an article. Returns 201, or 200 with `"duplicate": true` if the URL exists |
| PATCH | `/api/articles/<id>/` | Update an article, e.g. add `title_tk` / `summary_tk` later |

Article fields: `url` (required, unique), `title` (required), `source` (id), `category` (slug; unknown → `other`),
`title_tk`, `content`, `summary_en`, `summary_tk`, `tags` (list, max 8), `image_url`, `published_at` (ISO 8601).

Category slugs: `world`, `politics`, `business`, `technology`, `science`, `health`, `sports`, `culture`, `central-asia`, `other`.

## Tests

```bash
.venv/bin/python manage.py test news
```
