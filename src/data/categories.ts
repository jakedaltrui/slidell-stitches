export const categories = {
  "wreath-sashes": {
    name: "Wreath Sashes",
    slug: "wreath-sashes",
    h1: "Handmade Wreath Sashes",
    intro:
      "Dress up your front door for every season with a hand-embroidered wreath sash. From Mardi Gras to Christmas, game day to everyday — each one is stitched right here in Slidell.",
    metaTitle: "Handmade Wreath Sashes — Slidell Stitches",
    metaDescription:
      "Shop hand-embroidered wreath sashes for every season. Mardi Gras, Christmas, game day, patriotic & more. Handmade in Slidell, Louisiana.",
    image: "/images/categories/wreath-sashes.jpg",
  },
  hats: {
    name: "Hats",
    slug: "hats",
    h1: "Embroidered Hats",
    intro:
      "Trucker caps, baseball hats, and ponytail styles — all embroidered by hand. Rep your city, your school, or your own custom design.",
    metaTitle: "Embroidered Hats — Slidell Stitches",
    metaDescription:
      "Custom embroidered hats handmade in Slidell, Louisiana. Trucker caps, baseball hats & ponytail styles with your design.",
    image: "/images/categories/hats.jpg",
  },
  "cocktail-napkins": {
    name: "Cocktail Napkins",
    slug: "cocktail-napkins",
    h1: "Embroidered Cocktail Napkins",
    intro:
      "Linen cocktail napkins with hand-embroidered designs that make any gathering feel a little more special. Perfect for hostess gifts or your own bar cart.",
    metaTitle: "Embroidered Cocktail Napkins — Slidell Stitches",
    metaDescription:
      "Hand-embroidered linen cocktail napkins. Perfect hostess gifts. Custom monograms & designs available. Handmade in Slidell, LA.",
    image: "/images/categories/cocktail-napkins.jpg",
  },
  towels: {
    name: "Towels",
    slug: "towels",
    h1: "Embroidered Kitchen Towels",
    intro:
      "Hand-embroidered kitchen towels that are almost too pretty to use. Personalized with names, monograms, or custom designs.",
    metaTitle: "Embroidered Kitchen Towels — Slidell Stitches",
    metaDescription:
      "Personalized kitchen towels with hand embroidery. Monograms, names & custom designs. Handmade in Slidell, Louisiana.",
    image: "/images/categories/towels.jpg",
  },
  baby: {
    name: "Baby",
    slug: "baby",
    h1: "Personalized Baby Gifts",
    intro:
      "Heirloom-quality baby quilts, swaddles, and backpacks embroidered with love. The kind of gift that gets kept forever.",
    metaTitle: "Personalized Baby Gifts — Slidell Stitches",
    metaDescription:
      "Handmade personalized baby quilts, swaddles & backpacks. Embroidered baby gifts that become keepsakes. Made in Slidell, LA.",
    image: "/images/categories/baby.jpg",
  },
  "childrens-clothing": {
    name: "Children's Clothing",
    slug: "childrens-clothing",
    h1: "Embroidered Children's Clothing",
    intro:
      "Custom embroidered clothing for the little ones. From seersucker to everyday wear, each piece is stitched with their name or a design they'll love.",
    metaTitle: "Embroidered Children's Clothing — Slidell Stitches",
    metaDescription:
      "Custom embroidered children's clothing. Personalized with names & designs. Handmade in Slidell, Louisiana.",
    image: "/images/categories/childrens-clothing.jpg",
  },
  "bouquet-wraps": {
    name: "Bouquet Wraps",
    slug: "bouquet-wraps",
    h1: "Embroidered Bouquet Wraps",
    intro:
      "A hand-embroidered bouquet wrap turns your wedding flowers into a keepsake. Personalized with initials, dates, or a memorial message.",
    metaTitle: "Embroidered Bouquet Wraps — Slidell Stitches",
    metaDescription:
      "Hand-embroidered wedding bouquet wraps. Personalized with initials, dates & memorial messages. Handmade in Slidell, LA.",
    image: "/images/categories/bouquet-wraps.jpg",
  },
  pets: {
    name: "Pets",
    slug: "pets",
    h1: "Embroidered Pet Accessories",
    intro:
      "Because your pet deserves the monogram treatment too. Custom embroidered bandanas, collars, and more.",
    metaTitle: "Embroidered Pet Accessories — Slidell Stitches",
    metaDescription:
      "Custom embroidered pet accessories. Personalized bandanas, collars & more for your furry family. Handmade in Slidell, LA.",
    image: "/images/categories/pets.jpg",
  },
} as const;

export type CategorySlug = keyof typeof categories;
export const categoryList = Object.values(categories);
export const categorySlugs = Object.keys(categories) as CategorySlug[];
