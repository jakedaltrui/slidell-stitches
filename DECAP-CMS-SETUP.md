# Decap CMS Setup Guide — Slidell Stitches

This guide covers how to activate the Decap CMS admin panel at `/admin` so Stephanie can edit products through a web UI. The config files already exist at `public/admin/index.html` and `public/admin/config.yml` — this doc covers everything needed to turn them on.

---

## 1. Before First Use

The following must exist before the CMS will work:

- A GitHub repo (expected: `slidell-stitches/slidell-stitches`)
- The site code pushed to the `main` branch
- A Vercel project connected to that repo, auto-deploying on push
- A working production URL — either the custom domain (`slidell-stitches.com`) or the default Vercel subdomain (`slidell-stitches.vercel.app`)

If the domain in `public/admin/config.yml` doesn't match the live URL, update the `site_url` and `display_url` fields.

---

## 2. Set Up GitHub OAuth for Decap

Decap CMS commits changes directly to GitHub. That requires a GitHub OAuth App plus an OAuth proxy (a tiny service that exchanges the OAuth code for a token — GitHub doesn't allow browsers to do this directly).

### 2a. Create the GitHub OAuth App

1. Go to GitHub → **Settings** → **Developer Settings** → **OAuth Apps** → **New OAuth App**
2. Fill in:
   - **Application name:** `Slidell Stitches CMS`
   - **Homepage URL:** `https://slidell-stitches.com`
   - **Authorization callback URL:** `https://<your-oauth-proxy>.vercel.app/callback`
     (you'll get this URL in step 2b — come back and paste it)
3. Click **Register application**
4. On the next page, copy the **Client ID** and click **Generate a new client secret** — copy that too. Save both somewhere safe (the secret is only shown once).

### 2b. Deploy an OAuth Proxy on Vercel

Decap needs a small server to complete the OAuth flow. Two options:

**Option A (recommended) — self-host `netlify-cms-oauth-provider-node`:**

1. Fork `https://github.com/sterlingwes/netlify-cms-oauth-provider-node`
2. Create a new Vercel project pointed at your fork
3. In the Vercel project's **Environment Variables**, add:
   - `OAUTH_CLIENT_ID` = the GitHub Client ID from step 2a
   - `OAUTH_CLIENT_SECRET` = the GitHub Client Secret from step 2a
   - `ORIGIN` = `slidell-stitches.com` (no protocol)
4. Deploy. Vercel will assign a URL like `https://slidell-stitches-oauth.vercel.app`
5. Go back to your GitHub OAuth App settings and paste the callback URL: `https://slidell-stitches-oauth.vercel.app/callback`

**Option B — self-host `netlify-cms-github-oauth-provider` (PHP):** not recommended, Node version is simpler on Vercel.

### 2c. Update `public/admin/config.yml`

Add the `base_url` under `backend:` so Decap knows where the OAuth proxy lives:

```yaml
backend:
  name: github
  repo: slidell-stitches/slidell-stitches
  branch: main
  base_url: https://slidell-stitches-oauth.vercel.app
```

Commit and push. Vercel redeploys in ~60 seconds.

---

## 3. Update `config.yml` for the Real Repo

In `public/admin/config.yml`:

- Set `repo:` to the actual repo (e.g. `slidell-stitches/slidell-stitches`)
- Set `base_url:` under `backend:` to the OAuth proxy URL
- Confirm `site_url` and `display_url` point at the live domain

---

## 4. How Stephanie Uses the CMS

1. Go to `https://slidell-stitches.com/admin`
2. Click **Login with GitHub** → authorize the app (first time only)
3. The Products collection appears with all 103 products
4. Click any product to edit, or **New Product** to create one
5. Click **Publish** (or **Save** then **Publish** depending on workflow)
6. Changes commit to GitHub → Vercel auto-rebuilds → live in ~60 seconds

---

## 5. Adding a New Product

1. Click **New Product**
2. Fill in:
   - **Name** — e.g. "Pink Floral Wreath Sash"
   - **Price** — e.g. `24.99` (no dollar sign)
   - **Main Image** — upload a photo (aim for 1200px wide, under 500KB)
   - **Image Alt Text** — describe what's in the photo
   - **Category** — pick from the dropdown
   - **Etsy URL** — paste the full Etsy listing link
   - **Featured** — check to show on the homepage
   - **In Stock** — leave checked unless sold out
   - **Description** — 2-3 sentences
   - **Meta Description** — optional SEO blurb under 155 characters
3. Click **Publish**
4. Wait ~60 seconds and refresh the live site

---

## 6. Editing an Existing Product

1. Click the product from the list
2. Change whatever you need
3. Click **Publish**
4. Wait ~60 seconds for the site to rebuild

To take a product off the site quickly: uncheck **In Stock** and publish. To remove entirely: use the **Delete** button at the bottom of the edit screen.

---

## 7. Troubleshooting

**"Changes aren't showing up on the live site"**
→ Check the Vercel dashboard. If the latest deploy failed (red X), the build broke. The most common cause: a required field was left empty. Fix it in the CMS and publish again.

**"Can't log in / auth error"**
→ The GitHub OAuth app's callback URL doesn't match the OAuth proxy URL. Go to GitHub OAuth App settings and confirm it matches exactly (including `/callback`).

**"Image upload fails"**
→ The image is too large. Keep uploads under 2MB. Resize first at squoosh.app if needed.

**"Product isn't showing on the homepage"**
→ Check that **Featured** is turned on. The homepage Customer Favorites section only shows featured products.

**"I get a 404 at /admin"**
→ The Vercel deploy may not have finished, or `public/admin/` wasn't pushed. Verify `public/admin/index.html` and `public/admin/config.yml` are both in the repo on `main`.
