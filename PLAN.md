# Slidell Stitches — Storefront Site Plan

## Project Overview

**Client:** Stephanie Loupe
**Business:** Slidell Stitches — custom embroidery & monogramming shop in Slidell, Louisiana
**Etsy:** etsy.com/shop/slidellstitches (645 sales, 4.9★, 103 listings)
**Facebook:** facebook.com/p/Slidell-Stitches-61578203218841

**What we're building:** A branded storefront website that showcases her products and drives customers to Etsy for checkout. Custom orders handled via a contact form → email. She manages products herself through a CMS admin panel.

**What we're NOT building:** Shopping cart, checkout, payment processing, order management, user accounts.

---

## Architecture

### Stack
| Layer | Tool | Cost |
|-------|------|------|
| Static site generator | Astro | Free |
| Styling | Tailwind CSS v4 | Free |
| CMS | Decap CMS (formerly Netlify CMS) | Free |
| Hosting | Vercel (free tier) | Free |
| Forms | Formspree (free tier, 50 submissions/mo) | Free |
| Repo | GitHub | Free |
| Domain | TBD (staging on Vercel subdomain first) | ~$12/yr |
| **Total monthly** | | **$0** |

### How It Works
1. Products stored as Markdown files with frontmatter in `src/content/products/`
2. Astro builds static HTML pages from product data at build time
3. Stephanie logs into `site.com/admin` → Decap CMS gives her a form UI to add/edit/delete products
4. When she saves, Decap commits to GitHub → Vercel auto-rebuilds (< 60 seconds)
5. Every product page has a "Buy on Etsy" button linking to the Etsy listing
6. Custom order form submits via Formspree → info@slidell-stitches.com

### Project Structure
```
slidell-stitches/
├── public/
│   ├── admin/              # Decap CMS config
│   │   ├── index.html
│   │   └── config.yml
│   ├── images/
│   │   └── products/       # Product photos (scraped from Etsy)
│   └── logo.png
├── src/
│   ├── content/
│   │   ├── config.ts       # Astro content collection schema
│   │   └── products/       # Markdown files (1 per product)
│   │       ├── patriotic-american-wreath-sash.md
│   │       └── ...
│   ├── layouts/
│   │   └── Base.astro      # HTML shell, nav, footer
│   ├── components/
│   │   ├── Nav.astro
│   │   ├── Footer.astro
│   │   ├── ProductCard.astro
│   │   ├── ProductGrid.astro
│   │   ├── CategoryFilter.astro
│   │   ├── Hero.astro
│   │   ├── FeaturedProducts.astro
│   │   ├── CustomOrderForm.astro
│   │   └── TestimonialStrip.astro
│   ├── pages/
│   │   ├── index.astro         # Home
│   │   ├── shop/
│   │   │   ├── index.astro     # Shop All (all products)
│   │   │   └── [category].astro # Category landing pages (SSG)
│   │   ├── products/
│   │   │   └── [...slug].astro # Product detail pages
│   │   ├── custom-orders.astro # Custom order form
│   │   ├── about.astro         # Stephanie's story
│   │   ├── contact.astro       # Contact info
│   │   └── sitemap.xml.ts      # Dynamic sitemap
│   └── styles/
│       └── global.css
├── astro.config.mjs
├── tailwind.config.mjs
└── package.json
```

---

## Design System

### Style Direction: "Nature Distilled" meets Southern Charm
Warm, earthy, handmade feel. Linen textures, soft shadows, organic warmth. The site should feel like walking into a well-curated Southern boutique — not a tech startup, not an Etsy clone.

### Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--cream` | `#FAF7F2` | Page background — warm linen white |
| `--cream-dark` | `#F0EBE3` | Card backgrounds, alternate sections |
| `--sage` | `#7A8B6F` | Primary brand color — buttons, links, accents |
| `--sage-dark` | `#5C6B52` | Hover states, active elements |
| `--sage-light` | `#D4DDD0` | Borders, subtle backgrounds, tags |
| `--gold` | `#C9A96E` | Accent — prices, highlights, decorative elements |
| `--gold-light` | `#E8D5A8` | Subtle accent backgrounds |
| `--charcoal` | `#3D3D3D` | Primary text |
| `--charcoal-light` | `#6B6B6B` | Secondary text, descriptions |
| `--white` | `#FFFFFF` | Cards, overlays |
| `--blush` | `#E8D5C4` | Warm accent — section dividers, decorative |

### Typography

| Role | Font | Weight | Size |
|------|------|--------|------|
| Display/Hero | Playfair Display | 700 | 48–72px (clamp) |
| Script Accent | Great Vibes | 400 | 24–36px (sparingly — taglines, "handmade with love") |
| Headings | Playfair Display | 600 | 24–36px |
| Body | Lora | 400, 500 | 16–18px |
| UI/Buttons/Nav | Lora | 600 | 14–16px |
| Price | Lora | 700 | 18–20px |

**Google Fonts import:**
```
Playfair+Display:wght@600;700|Great+Vibes&family=Lora:wght@400;500;600;700
```

### Spacing Scale
```
4px / 8px / 12px / 16px / 24px / 32px / 48px / 64px / 96px
```

### Border Radius
- Cards: `12px`
- Buttons: `8px`
- Tags/badges: `9999px` (pill)
- Product images: `8px`

### Shadows
- Card: `0 2px 8px rgba(0,0,0,0.06)`
- Card hover: `0 8px 24px rgba(0,0,0,0.10)`
- Nav: `0 1px 3px rgba(0,0,0,0.05)`

### Texture & Effects
- Subtle linen/paper texture on `--cream` background (CSS noise pattern, not an image)
- Soft border-bottom on sections using `--sage-light`
- No harsh lines — use spacing and soft color shifts to separate content
- Product photos get a very subtle warm filter on hover (CSS `filter: saturate(1.05) brightness(1.02)`)

---

## SEO & Conversion Strategy

### Skills to Use During Execution
| Phase | Skill | Purpose |
|-------|-------|---------|
| Copywriting | `marketing:copywriting` | All page copy — homepage, about, category intros, CTAs |
| Page CRO | `marketing:page-cro` | Homepage + custom orders conversion optimization |
| Schema Markup | `marketing:schema-markup` | JSON-LD structured data on every page type |
| Content Strategy | `marketing:content-strategy` | Category page content, meta descriptions, keyword targeting |
| AI/GEO SEO | `marketing:ai-seo` | Make content citable by AI search (Google AI Overviews, ChatGPT) |
| SEO Audit | `seo-technical` | Technical SEO checklist before launch |
| Image SEO | `seo-images` | Alt text strategy, WebP, srcset, lazy loading |

### Target Keywords

**Primary (high intent, local):**
- "custom embroidery Slidell Louisiana"
- "custom embroidery near me" (Slidell/Northshore)
- "monogrammed gifts Louisiana"
- "personalized embroidery Slidell"

**Category-level (product intent):**
- "wreath sash" / "custom wreath sashes"
- "monogrammed wreath sash"
- "embroidered hats Louisiana"
- "personalized cocktail napkins"
- "monogrammed baby gifts"
- "custom baby quilt embroidered"
- "embroidered kitchen towels"
- "wedding bouquet wrap embroidered"

**Seasonal/occasion (traffic drivers):**
- "Mardi Gras wreath sash"
- "LSU wreath sash" / "Ole Miss wreath sash"
- "Christmas wreath sash"
- "Easter wreath sash"
- "game day embroidered hat"

### SEO Architecture

**Every category gets its own URL** — not just a filter on `/shop`. Each is a standalone landing page with:
- Unique H1 targeting the category keyword
- 2-3 sentence intro with natural keyword usage
- Unique meta title and description
- Product grid filtered to that category
- Internal links to related categories
- BreadcrumbList schema

**URL structure:**
```
/                           → Home
/shop                       → All products
/shop/wreath-sashes         → Category landing page
/shop/hats                  → Category landing page
/shop/cocktail-napkins      → Category landing page
/shop/towels                → Category landing page
/shop/baby                  → Category landing page
/shop/childrens-clothing    → Category landing page
/shop/bouquet-wraps         → Category landing page
/shop/pets                  → Category landing page
/products/[slug]            → Product detail
/custom-orders              → Custom order form
/about                      → About Stephanie
/contact                    → Contact
```

### Schema Markup Plan
| Page | Schema Type | Key Properties |
|------|------------|----------------|
| All pages | LocalBusiness | name, address (Slidell, LA), url, logo, sameAs (Etsy, Facebook) |
| All pages | BreadcrumbList | Navigation path |
| Home | Organization | name, logo, description, founder |
| Product detail | Product | name, image, price, priceCurrency, availability, brand, url, offers |
| Category pages | CollectionPage | name, description, hasPart (products) |
| About | AboutPage + Person | name, description, jobTitle, worksFor |
| Custom Orders | Service | name, description, provider, areaServed |

### Meta Title & Description Strategy
| Page | Title Pattern | Description Pattern |
|------|--------------|---------------------|
| Home | Slidell Stitches — Custom Embroidery & Monogramming | Handmade embroidered wreath sashes, hats, napkins & more from Slidell, Louisiana. 645+ happy customers. Shop or request a custom order. |
| Category | [Category] — Slidell Stitches | Shop handmade [category]. Personalized, embroidered by hand in Slidell, LA. [Unique selling point for category]. |
| Product | [Product Name] — Slidell Stitches | [Product description]. Handmade and embroidered by Slidell Stitches. Ships nationwide. |
| Custom Orders | Custom Embroidery Orders — Slidell Stitches | Request custom embroidered wreath sashes, hats, napkins, baby gifts & more. Handmade in Slidell, Louisiana. |
| About | About Stephanie Loupe — Slidell Stitches | Meet the maker behind Slidell Stitches. Handmade embroidery from Slidell, Louisiana. 2+ years, 645+ orders, 4.9★ on Etsy. |

### Conversion Strategy

**Primary conversion:** Click "Buy on Etsy" → purchase
**Secondary conversion:** Submit custom order form

**Homepage CRO principles:**
- Value prop visible within 1 second of landing (no scrolling on mobile)
- Social proof above the fold: "645+ orders | 4.9★ on Etsy"
- Two clear CTAs in hero: "Shop All" (primary) + "Request Custom Order" (secondary)
- Category cards immediately below hero → reduce decision fatigue
- Featured/bestseller products create urgency ("popular" badges)
- Custom order CTA section breaks up the browse flow — catches people who didn't find what they want
- Trust strip anchors the bottom: handmade, local, real person

**Custom Orders page CRO:**
- Headline addresses the desire, not the form: "Bring Your Idea to Life"
- Trust signals adjacent to form (not below it): Etsy rating, order count, turnaround time
- Form is short — only required fields visible, optional fields collapsed
- Past custom work gallery ABOVE the form (shows capability before asking for commitment)
- Clear "what happens next" after submit: "I'll review your request and get back to you within 24 hours with a quote"
- No price on the form — reduces friction (she quotes after)

**Product page CRO:**
- "Buy on Etsy" is the ONLY action — no competing CTAs
- Button is large, sticky on mobile (fixed bottom bar)
- "You might also like" section keeps browsers engaged
- Breadcrumb links back to category page (not just /shop)

---

## Page Layouts

### Home (`/`)
Copy written using `marketing:copywriting` skill. CRO layout using `marketing:page-cro` skill.
```
┌─────────────────────────────────────────┐
│  NAV: Logo (left) | Shop . Custom       │
│  Orders . About . Contact               │
│  [Shop on Etsy →] (subtle top-right)    │
├─────────────────────────────────────────┤
│  HERO (full-width lifestyle photo)      │
│  H1: "Handmade Embroidery for Every     │
│  Season" (Playfair Display)             │
│  Subhead: "Custom wreath sashes, hats,  │
│  napkins & more — stitched by hand in   │
│  Slidell, Louisiana" (Lora)             │
│  [Shop All →] [Request Custom Order]    │
│                                         │
│  Trust bar (inline, below CTAs):        │
│  "645+ Orders · 4.9★ on Etsy ·         │
│  Handmade in Slidell, LA"              │
├─────────────────────────────────────────┤
│  SECTION: "Shop by Category"            │
│  Grid of 8 category cards (4x2 desktop, │
│  2x4 mobile). Each card:               │
│  [category photo] + "Wreath Sashes →"   │
│  Links to /shop/wreath-sashes           │
├─────────────────────────────────────────┤
│  SECTION: "Customer Favorites"          │
│  4 featured product cards (bestsellers) │
│  [View All Products →]                  │
├─────────────────────────────────────────┤
│  CUSTOM ORDER CTA SECTION               │
│  Split layout: photo left, text right   │
│  "Have something special in mind?"      │
│  "I love bringing your ideas to life —  │
│  monograms, school logos, custom colors, │
│  you name it."                          │
│  [Request a Custom Order →]             │
├─────────────────────────────────────────┤
│  SECTION: "Why Slidell Stitches?"       │
│  3 columns:                             │
│  "Handmade with Care" | "Personalized   │
│  for You" | "Trusted by 645+ Customers" │
│  (short copy + icon per column)         │
├─────────────────────────────────────────┤
│  FOOTER                                 │
│  Logo | Nav links | Facebook | Etsy     │
│  hello@slidell-stitches.com             │
│  © 2026 Slidell Stitches                │
│  LocalBusiness schema in footer         │
└─────────────────────────────────────────┘
```

### Shop All (`/shop`)
```
┌─────────────────────────────────────────┐
│  NAV                                    │
├─────────────────────────────────────────┤
│  Breadcrumb: Home > Shop                │
│  H1: "Shop All Handmade Embroidery"     │
│  Subhead: "Browse everything or pick a  │
│  category below"                        │
│                                         │
│  FILTER BAR (horizontal, scrollable     │
│  on mobile — pill-shaped buttons):      │
│  All | Wreath Sashes | Hats | Napkins   │
│  | Towels | Baby | Children's | Bouquet │
│  Wraps | Pets                           │
│  (each filter links to /shop/[cat])     │
├─────────────────────────────────────────┤
│  PRODUCT GRID                           │
│  2 cols mobile / 3 cols tablet / 4 cols │
│  desktop. Each card:                    │
│  ┌──────────────┐                       │
│  │  [photo]     │                       │
│  │  Product Name│                       │
│  │  $38.00      │                       │
│  │  [View Details]                      │
│  └──────────────┘                       │
│  Client-side JS filtering AND each      │
│  category has its own server-rendered   │
│  URL for SEO                            │
├─────────────────────────────────────────┤
│  FOOTER                                 │
└─────────────────────────────────────────┘
```

### Category Page (`/shop/[category]`)
```
┌─────────────────────────────────────────┐
│  NAV                                    │
├─────────────────────────────────────────┤
│  Breadcrumb: Home > Shop > Wreath       │
│  Sashes                                 │
│  H1: "Handmade Wreath Sashes"           │
│  Intro: 2-3 sentences unique to this    │
│  category, naturally keyword-rich.      │
│  Written using marketing:copywriting.   │
│  e.g. "Dress up your front door for     │
│  every season with a hand-embroidered   │
│  wreath sash. From Mardi Gras to        │
│  Christmas, game day to everyday —      │
│  each one is stitched right here in     │
│  Slidell."                              │
├─────────────────────────────────────────┤
│  PRODUCT GRID (same as /shop but        │
│  filtered to this category only)        │
├─────────────────────────────────────────┤
│  "Browse Other Categories" — links to   │
│  other category pages (internal linking)│
├─────────────────────────────────────────┤
│  FOOTER                                 │
└─────────────────────────────────────────┘
```

### Product Detail (`/products/[slug]`)
```
┌─────────────────────────────────────────┐
│  NAV                                    │
├─────────────────────────────────────────┤
│  Breadcrumb: Home > Shop > Wreath       │
│  Sashes > Patriotic American Wreath Sash│
│                                         │
│  [PRODUCT PHOTO]    H1: Product Name    │
│  (large, left)      $38.00             │
│                     UNIQUE description  │
│                     (not copied from    │
│                     Etsy — rewritten    │
│                     using copywriting   │
│                     skill)              │
│                                         │
│                     Category: Wreath    │
│                     Sashes (linked)     │
│                                         │
│                     [Buy on Etsy →]     │
│                     (large sage button) │
│                                         │
│  MOBILE: sticky bottom bar with         │
│  "$38.00  [Buy on Etsy →]"             │
├─────────────────────────────────────────┤
│  "You might also like" — 4 related     │
│  products from same category            │
├─────────────────────────────────────────┤
│  Product schema (JSON-LD) in <head>     │
│  FOOTER                                 │
└─────────────────────────────────────────┘
```

### Custom Orders (`/custom-orders`)
CRO-optimized using `marketing:page-cro` skill.
```
┌─────────────────────────────────────────┐
│  NAV                                    │
├─────────────────────────────────────────┤
│  H1: "Bring Your Idea to Life"          │
│  Subhead: "Monograms, school logos,     │
│  custom colors — tell me what you're    │
│  dreaming up and I'll make it happen."  │
│                                         │
│  TRUST SIGNALS (inline, near headline): │
│  "645+ orders completed · 4.9★ rated ·  │
│  Most custom orders ship in 5-7 days"   │
├─────────────────────────────────────────┤
│  GALLERY: "Past Custom Work" (6-8      │
│  photos in a horizontal scroll/grid)    │
│  Shows capability BEFORE asking for     │
│  commitment                             │
├─────────────────────────────────────────┤
│  "How It Works" — 3 steps:              │
│  1. Tell me your idea (form below)      │
│  2. I'll send you a quote within 24hrs  │
│  3. I get stitching                     │
├─────────────────────────────────────────┤
│  FORM (Formspree → info@slidell-        │
│  stitches.com):                         │
│  VISIBLE:                               │
│  - Name *                               │
│  - Email *                              │
│  - What are you looking for? *          │
│    (dropdown: Wreath Sash, Hat,         │
│    Napkins, Towel, Baby Item, Apparel,  │
│    Other)                               │
│  - Personalization details *            │
│    (text/monogram, colors, fonts)       │
│  COLLAPSED ("+ Add more details"):      │
│  - Phone (optional)                     │
│  - Quantity                             │
│  - Needed by (date picker)             │
│  - Upload reference image (optional)   │
│  - Additional notes (textarea)          │
│  [Submit Request]                       │
│                                         │
│  POST-SUBMIT MESSAGE:                   │
│  "Got it! I'll review your request and  │
│  get back to you within 24 hours with   │
│  a quote. — Stephanie"                  │
├─────────────────────────────────────────┤
│  Service schema (JSON-LD) in <head>     │
│  FOOTER                                 │
└─────────────────────────────────────────┘
```

### About (`/about`)
```
┌─────────────────────────────────────────┐
│  NAV                                    │
├─────────────────────────────────────────┤
│  [PLACEHOLDER: stephanie-portrait.jpg]  │
│                                         │
│  H1: "Meet Stephanie"                   │
│                                         │
│  Bio copy (see About Page Bio section)  │
│  Written to naturally include keywords: │
│  embroidery, Slidell, Louisiana,        │
│  handmade, custom                       │
│                                         │
│  [PLACEHOLDER: stephanie-workspace.jpg] │
│                                         │
│  STATS STRIP:                           │
│  "2+ Years on Etsy" | "645+ Orders" |  │
│  "4.9★ Rating"                         │
│                                         │
│  CTA: "See my work → [Shop All]" or    │
│  "Have an idea? [Request Custom Order]" │
├─────────────────────────────────────────┤
│  Person + AboutPage schema in <head>    │
│  FOOTER                                 │
└─────────────────────────────────────────┘
```

### Contact (`/contact`)
```
┌─────────────────────────────────────────┐
│  NAV                                    │
├─────────────────────────────────────────┤
│  H1: "Get in Touch"                     │
│  "Questions, wholesale inquiries, or    │
│  just want to say hey — I'd love to     │
│  hear from you."                        │
│                                         │
│  Email: contact@slidell-stitches.com    │
│  Facebook: Slidell Stitches (linked)    │
│  Etsy: etsy.com/shop/slidellstitches    │
│  Location: Slidell, Louisiana           │
│                                         │
│  Simple contact form (Formspree →       │
│  contact@slidell-stitches.com):         │
│  Name, Email, Message                   │
│  [Send Message]                         │
├─────────────────────────────────────────┤
│  FOOTER                                 │
└─────────────────────────────────────────┘
```

---

## Content Collections (Astro)

### Product Schema
```typescript
// src/content/config.ts
import { defineCollection, z } from 'astro:content';

const categories = [
  'wreath-sashes',
  'hats',
  'cocktail-napkins',
  'towels',
  'baby',
  'childrens-clothing',
  'bouquet-wraps',
  'pets'
] as const;

const products = defineCollection({
  type: 'content',
  schema: z.object({
    name: z.string(),
    price: z.number(),
    image: z.string(),
    images: z.array(z.string()).optional(),
    image_alt: z.string(),           // SEO: descriptive alt text
    category: z.enum(categories),
    etsy_url: z.string().url(),
    featured: z.boolean().default(false),
    in_stock: z.boolean().default(true),
    description: z.string(),         // REQUIRED: unique copy, not from Etsy
    meta_description: z.string().optional(), // SEO: per-product meta desc
  }),
});

export const collections = { products };
```

### Example Product Markdown
```markdown
---
name: "Patriotic American Wreath Sash"
price: 38.00
image: "/images/products/patriotic-american-wreath-sash.jpg"
image_alt: "Red, white, and blue embroidered wreath sash with stars on a green wreath"
category: "wreath-sashes"
etsy_url: "https://www.etsy.com/listing/..."
featured: true
in_stock: true
description: "Bring a little Americana to your front door. This hand-embroidered wreath sash features classic red, white, and blue stripes with stitched stars — perfect for the Fourth of July, Memorial Day, or year-round patriotic charm."
meta_description: "Hand-embroidered patriotic wreath sash in red, white & blue. Handmade in Slidell, LA. Ships nationwide."
---
```

### Category Data
```typescript
// src/data/categories.ts
export const categories = {
  'wreath-sashes': {
    name: 'Wreath Sashes',
    slug: 'wreath-sashes',
    h1: 'Handmade Wreath Sashes',
    intro: 'Dress up your front door for every season with a hand-embroidered wreath sash. From Mardi Gras to Christmas, game day to everyday — each one is stitched right here in Slidell.',
    metaTitle: 'Handmade Wreath Sashes — Slidell Stitches',
    metaDescription: 'Shop hand-embroidered wreath sashes for every season. Mardi Gras, Christmas, game day, patriotic & more. Handmade in Slidell, Louisiana.',
    image: '/images/categories/wreath-sashes.jpg',
  },
  // ... (each category gets unique copy via marketing:copywriting)
};
```

---

## Decap CMS Configuration

```yaml
# public/admin/config.yml
backend:
  name: github
  repo: owner/slidell-stitches  # TBD
  branch: main

media_folder: public/images/products
public_folder: /images/products

collections:
  - name: products
    label: Products
    folder: src/content/products
    create: true
    slug: "{{slug}}"
    fields:
      - { label: "Name", name: "name", widget: "string" }
      - { label: "Price", name: "price", widget: "number", value_type: "float" }
      - { label: "Main Image", name: "image", widget: "image" }
      - label: "Category"
        name: "category"
        widget: "select"
        options:
          - { label: "Wreath Sashes", value: "wreath-sashes" }
          - { label: "Hats", value: "hats" }
          - { label: "Cocktail Napkins", value: "cocktail-napkins" }
          - { label: "Towels", value: "towels" }
          - { label: "Baby", value: "baby" }
          - { label: "Children's Clothing", value: "childrens-clothing" }
          - { label: "Bouquet Wraps", value: "bouquet-wraps" }
          - { label: "Pets", value: "pets" }
      - { label: "Etsy URL", name: "etsy_url", widget: "string" }
      - { label: "Featured", name: "featured", widget: "boolean", default: false }
      - { label: "In Stock", name: "in_stock", widget: "boolean", default: true }
      - { label: "Description", name: "description", widget: "text", required: false }
```

---

## Emails

| Purpose | Address |
|---------|---------|
| Custom order form | info@slidell-stitches.com |
| Contact page form | contact@slidell-stitches.com |
| General / footer | hello@slidell-stitches.com |

---

## About Page Bio

> I'm Stephanie, and Slidell Stitches is where my love for embroidery meets everything I care about — family, football Saturdays, faith, and making something beautiful by hand.
>
> It started the way most good things do — a project for a friend that turned into a project for her friend, and then another, and then I lost count. Before I knew it, my dining room table was covered in thread and fabric, and I wouldn't have it any other way.
>
> Every stitch that leaves my hands is personal. Whether it's a wreath sash for your front door, a monogrammed baby quilt for a new little one, or a set of cocktail napkins for your next get-together — I put the same care into it that I would if it were going on my own front porch.
>
> I'm based right here in Slidell, Louisiana, and I ship everywhere. If you've got an idea for something custom, I'd love to hear about it — that's honestly my favorite part of what I do.

### Photo Placeholders
- **Hero section:** `[PLACEHOLDER: stephanie-hero.jpg]` — Stephanie at her embroidery machine or workspace, natural light
- **About page portrait:** `[PLACEHOLDER: stephanie-portrait.jpg]` — Headshot or casual portrait, warm/friendly
- **About page workspace:** `[PLACEHOLDER: stephanie-workspace.jpg]` — Wide shot of her workspace/setup (optional)

---

## Etsy Scraper (Bootstrap Data)

Python script to scrape all 103 listings and output:
1. Product markdown files for `src/content/products/`
2. Downloaded product images to `public/images/products/`

**Approach:** Use `requests` + `BeautifulSoup` to scrape the public shop page (no API key needed). Pull: title, price, image URL, category (from Etsy sidebar), listing URL. Download images locally. Generate `.md` files with frontmatter.

**Fallback:** If Etsy blocks scraping, manual CSV import (Stephanie exports from Etsy → we convert).

---

## Execution Phases

### Phase 1: Scaffold & Design System
- Initialize Astro project with Tailwind
- Set up color tokens, typography, global styles
- Build base layout (Nav + Footer with LocalBusiness schema)
- Set up sitemap generation, robots.txt
- Deploy blank site to Vercel

### Phase 2: Scrape & Import Products
- Write Etsy scraper script
- Run scraper, download images
- Generate product markdown files with placeholder descriptions
- Verify all 103 products imported correctly
- Optimize images (WebP conversion, resize to max 1200px wide)

### Phase 3: Copywriting & Content (`marketing:copywriting`, `marketing:content-strategy`)
- Write homepage copy (H1, subhead, section headlines, CTAs)
- Write unique product descriptions for all 103 products (NOT copied from Etsy)
- Write category page intros (8 categories)
- Write custom orders page copy (headline, subhead, how-it-works, post-submit)
- Write meta titles and descriptions for all page types
- Write alt text for product images
- Review/finalize About page bio

### Phase 4: Build Pages (`marketing:page-cro`)
- Home page (hero, category cards, featured products, trust strip, CTA section)
- Shop All page (filterable product grid)
- Category landing pages (8 pages, SSG from category data)
- Product detail pages (dynamic routes, sticky mobile CTA)
- Custom Orders page (CRO-optimized form + gallery + how-it-works)
- About page
- Contact page

### Phase 5: SEO & Schema (`marketing:schema-markup`, `marketing:ai-seo`, `seo-images`)
- JSON-LD structured data on every page type (LocalBusiness, Product, CollectionPage, Service, Person, BreadcrumbList)
- Open Graph + Twitter Card meta tags
- Image optimization pass (alt text, WebP, srcset, lazy loading)
- Internal linking audit (categories ↔ products ↔ related)
- XML sitemap verification
- AI search readiness audit (content structure, citability)

### Phase 6: CMS Integration
- Configure Decap CMS (products + category content)
- Set up GitHub OAuth for admin login
- Test: add product, edit product, delete product
- Walk Stephanie through the admin

### Phase 7: QA & Launch Prep (`seo-technical`)
- Mobile responsiveness pass (375px, 768px, 1024px, 1440px)
- Lighthouse audit (Performance, Accessibility, SEO, Best Practices)
- Technical SEO checklist (crawlability, indexability, canonical tags)
- Favicon from logo
- 404 page
- Custom domain setup when ready
- Google Search Console submission

---

## Open Items (need from Stephanie)
- [ ] Hi-res photo of herself (portrait + at embroidery machine) — using placeholders until then
- [ ] A few lifestyle/action shots (wreath on a door, hat being worn, etc.) for hero — can use Etsy product photos as fallback
- [ ] Review the bio above and adjust anything that doesn't sound like her
- [ ] Photos of past custom work (for Custom Orders gallery)
- [ ] Confirmation of the 8 categories above
- [ ] Any products she does NOT want on the website
- [ ] Set up @slidell-stitches.com email addresses once domain is purchased
