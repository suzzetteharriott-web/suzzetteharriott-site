# suzzetteharriott.com

Static website for Dr. Suzzette A. Harriott, PhD (Therapeutic Conflictology and RESET).

- `public/` is the website. Hosting serves this folder as-is (no build step).
- `tools/build.py` regenerates the HTML pages in `public/` from one place, so the header, footer and page text stay consistent. Edit it, then run `python3 tools/build.py`.
- `public/_redirects` sends old Wix addresses (college consulting, special education, logins) to cescarib.com.
- No accounts, no database, no cookies. The contact form opens the visitor's own email app.
