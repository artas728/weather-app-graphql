import pytest

pytest.main(["-v", "--cov=connectors", "tests/unittests/test_pytest_weather.py"])
pytest.main(["-v", "--cov=connectors", "tests/unittests/test_pytest_db.py"])
pytest.main(["-v", "--cov=connectors", "tests/unittests/test_pytest_graphql.py"])
pytest.main(["-v", "--cov=connectors", "tests/unittests/test_pytest_fastapi.py"])