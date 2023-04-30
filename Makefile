doc:
	pandoc -f man -t markdown man/man1/piknik.1 > README.md
	echo -e "\n\n# ABOUT THIS DOCUMENT\n\nThis document was generated using \`pandoc -f man -t markdown ...\`" >> README.md
