docs: assertions_doc modules_doc

assertions_doc: ../module_utils/bf_assertion_util.py
	python assertions2rst.py

modules_doc: ../library/*.py ansible2rst.py rst.j2
	python ansible2rst.py
