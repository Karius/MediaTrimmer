pyinst=d:\Apps\pyinstaller\pyinstaller.py

dist/Trimmer.exe: *.py
	python $(pyinst) --onefile Trimmer.py


.PHONY : clean
clean:
	-del *.pyc *.log *.spec
	-rd /s /q build
