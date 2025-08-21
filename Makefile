.PHONY: format lint type-check check all

# Formattage du code
format:
	black .
	isort .

# Flake 8
lint:
	flake8 .

# Vérification des typages
type-check:
	mypy .

# Tout exécuter
check: format lint type-check