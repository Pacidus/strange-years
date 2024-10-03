SOURCE_DOCS := $(wildcard paper/*/*.md)
# SOURCE_DOCS := paper/*/*.md

EXPORTED_DOCS=strange_years.pdf README.md

RM=rm

PANDOC=pandoc

OPTIONS=--from markdown+rebase_relative_paths+smart --standalone=true
FILTERS=--filter pandoc-crossref

PDF=-t pdf
README=-t gfm



strange_years.pdf : $(SOURCE_DOCS)
	$(PANDOC) $(FILTERS) $(OPTIONS) $(PDF) $< -o $@ 

README.md : $(SOURCE_DOCS)
	$(PANDOC) $(FILTERS) $(OPTIONS) $(PDF) $< -o $@
	

.PHONY: all clean

all : $(EXPORTED_DOCS)

clean:
	- $(RM) $(EXPORTED_DOCS)
	make README.md
