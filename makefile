source_docs=paper/*/*.md
SOURCE_DOCS := $(wildcard paper/*/*.md)

EXPORTED_DOCS=strange_years.pdf README

RM=rm
PANDOC=pandoc

OPTIONS=--from markdown+rebase_relative_paths+smart --standalone=true
FILTERS=--filter pandoc-crossref

PDF=-t pdf
README=-t gfm

strange_years.pdf : $(SOURCE_DOCS)
	$(PANDOC) $(source_docs) $(FILTERS) $(OPTIONS) $(PDF) -o $@ 

README : $(SOURCE_DOCS)
	$(PANDOC) $(source_docs) $(FILTERS) $(OPTIONS) $(README) -o $@
	
docs: $(EXPORTED_DOCS)

.DEFAULT_GOAL = docs
.PHONY: all clean

all : $(EXPORTED_DOCS)

clean:
	- $(RM) $(EXPORTED_DOCS)
	make README
