from pytest_bdd import scenarios

# All step definitions are already defined in:
# - conftest.py (sleep steps, wait steps, fixtures)
# - test_activity_steps.py (activity steps)
# - test_readiness_steps.py (readiness steps)

# scenarios() at bottom after all imports
scenarios("../complete_flow.feature")
