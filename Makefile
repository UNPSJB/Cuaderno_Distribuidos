

Material\ Auxiliar\ TP1.pdf: Material\ Auxiliar\ TP1.md
	pandoc -t beamer -s "$^" -o "$@"

