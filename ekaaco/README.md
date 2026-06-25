# Ekaa, The Event Collective

A wedding first marketing site for Ekaa, a Mumbai wedding planner. One job: get an
engaged couple to start a conversation on WhatsApp. Mobile first, fast, editorial.

Built with FastAPI and Jinja2. All visible copy lives in `app/content.yaml`, so words
can be changed without touching code.

## Run it locally

```bash
cd ekaaco
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open http://127.0.0.1:8000

## Project layout

```
ekaaco/
  app/
    main.py            FastAPI app and routes
    content.yaml       all editable site copy (edit this to change words)
    templates/         base.html, index.html, book.html, contact.html
    static/
      css/style.css    the whole design, hand written and lightweight
      img/             logo and any brand images
      gallery/         drop wedding photos here
  data/                enquiries land in enquiries.jsonl (created on first submit)
  requirements.txt
```

## Routes

- `/`         the single page scrolling site (hero, services, founder, work, process, instagram, enquiry)
- `/contact`  a focused contact page
- `/book`     standalone enquiry form (the home page form posts here too)
- `/privacy`  privacy policy (copy lives in `app/main.py`)
- `/terms`    terms (copy lives in `app/main.py`)
- `/health`   simple health check

## Images

Section and gallery photos live in `app/static/img/` and `app/static/gallery/`.
They were exported from the photo brief with the Glowwed Films watermark cropped
out and optimised for the web. The logo is `app/static/img/ekaa-logo.png` (clean
transparent background) with `ekaa-logo-light.png` for the dark footer.

The stylesheet is cache busted automatically: the `<link>` carries a `?v=` stamp
from the CSS file mtime, so a fresh copy loads whenever you edit the styles.

## Editing content

Open `app/content.yaml`. Change any text. Copy reloads on the next page load, no
restart needed.

Hard brand rule: no hyphens and no em dashes anywhere in copy. Rephrase instead.

### Adding wedding photos

1. Drop image files into `app/static/gallery/`.
2. List them under `gallery.images` in `content.yaml`:

   ```yaml
   gallery:
     images:
       - file: "wedding-01.jpg"
         alt: "Mandap under soft evening light"
   ```

The grid renders automatically. With no images, a tasteful placeholder pointing to
Instagram shows instead.

### Adding testimonials

Add entries under `testimonials.quotes` in `content.yaml`. The section stays hidden
until at least one exists.

## Enquiries

Form submissions are appended to `data/enquiries.jsonl`, one JSON object per line.
To forward enquiries to email (`ekaaandco@gmail.com`) or a form service, extend the
`book_submit` handler in `app/main.py`. This is the one piece left deliberately
simple so it can be wired to whatever tool is preferred.

## Brand

- Colours: Ivory `#F5F0E8`, Charcoal `#2C2C2C`, Terracotta `#C17A5A`
- Type: Cormorant Garamond (headings), DM Sans (body)
- Instagram: @ekaa_theeventcollective
- WhatsApp and phone: +91 99305 09101
- Email: ekaaandco@gmail.com
- Domain: ekaa.in

## Deploy

It is a small Python app. Any host that runs `uvicorn` works (Render, Railway,
Fly, a small VPS). Point `ekaa.in` at it. Set the SEO domain in `content.yaml`
under `seo.domain` so Open Graph image URLs are absolute.
