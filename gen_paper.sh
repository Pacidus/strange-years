pandoc --filter pandoc-crossref  --lua-filter ./fig.lua -t gfm strange_years.md -o README.md
pandoc --filter pandoc-crossref -t pdf strange_years.md -o strange_years.pdf
