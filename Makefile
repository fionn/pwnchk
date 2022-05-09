DIR = pwnchk
SRC = $(DIR)/

.PHONY: install_user
install_user: $(SRC)
	@pip install --user --no-deps .

.PHONY: install_system
install_system: $(SRC)
	@pip install --no-deps .

build: $(SRC)
	@python -m build

tags: $(SRC)
	@ctags --languages=python --python-kinds=-i $(SRC)

.PHONY: lint
lint:
	@pylint -f colorized $(SRC) $(TEST)

.PHONY: typecheck
typecheck:
	@mypy $(SRC) $(TEST)

.PHONY: clean
clean:
	@$(RM) -r .mypy_cache
	@$(RM) -r __pycache__
	@$(RM) -r dist
	@$(RM) tags
