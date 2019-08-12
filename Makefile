.SUFFIXES: .tex .ps .dia .pdf .svg

.dia.pdf:
	dia -e eps-builtin -n -e ${@:.pdf=.eps} $<
	ps2pdf -dEPSCrop ${@:.pdf=.eps} $@

.svg.pdf:
	inkscape --export-pdf=$@ $<

LATEX_FILES = auto_lbox.tex

DIAGRAMS = images/limitation_php.pdf \
		   images/autoremoval.pdf \
		   images/sampleparsetree.pdf \
		   images/lbox_parsetree.pdf

EXTRA_DISTRIB_FILES = auto_lbox.pdf Makefile

all: auto_lbox.pdf

bib.bib: softdevbib/softdev.bib
	softdevbib/bin/prebib softdevbib/softdev.bib > bib.bib

softdevbib-update: softdevbib
	cd softdevbib && git pull

softdevbib/softdev.bib: softdevbib

softdevbib:
	git clone https://github.com/softdevteam/softdevbib.git


# Package up the paper for arxiv.org.
# Note that acmart.cls is included in tex live 2016, but it is too old.
ARXIV_FILES= softdev.sty \
		bib.bib \
		auto_lbox.bbl \

ARXIV_BASE=arxiv
${ARXIV_BASE}: auto_lbox.pdf acmart
	mkdir $@
	rsync -Rav ${ARXIV_FILES} $@
	cp auto_lbox.tex $@/auto_lbox.tex
	cp acmart.cls $@
	cp acmart/acmart.dtx $@
	cp acmart/acmart.ins $@
	zip -r $@.zip ${ARXIV_BASE}

ACMART_VERSION=904956ed0f4545da4fbb7f2401318917a348ba75
acmart:
	git clone https://github.com/borisveytsman/acmart
	cd acmart && git checkout ${ACMART_VERSION}

clean-arxiv:
	rm -rf arxiv
	rm -rf arxiv.zip
	rm -rf acmart

clean: clean-arxiv
	rm -rf ${DIAGRAMS} ${DIAGRAMS:S/.pdf/.eps/}
	rm -rf auto_lbox.aux auto_lbox.bbl auto_lbox.blg \
		auto_lbox.dvi auto_lbox.log auto_lbox.ps auto_lbox.pdf \
		auto_lbox.toc auto_lbox.out auto_lbox.snm auto_lbox.nav \
		auto_lbox.vrb texput.log bib.bib

auto_lbox.pdf: ${LATEX_FILES} ${DIAGRAMS} bib.bib
	pdflatex auto_lbox.tex
	bibtex auto_lbox
	pdflatex auto_lbox.tex
	pdflatex auto_lbox.tex

artefact.pdf: artefact.tex
	pdflatex artefact.tex
	pdflatex artefact.tex
