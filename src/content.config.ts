import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const products = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/products" }),
  schema: z.object({
    name: z.string(),
    price: z.number(),
    image: z.string(),
    image_alt: z.string(),
    category: z.enum([
      'wreath-sashes', 'hats', 'cocktail-napkins', 'towels',
      'baby', 'childrens-clothing', 'bouquet-wraps', 'pets'
    ]),
    etsy_url: z.string().url(),
    featured: z.boolean().default(false),
    in_stock: z.boolean().default(true),
    description: z.string(),
    meta_description: z.string().optional(),
  }),
});

export const collections = { products };
