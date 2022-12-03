import pytest
import yaml


ANSWERS_PATH = "answers.yaml"


@pytest.fixture(scope="session")
def answers():
    with open(ANSWERS_PATH) as fp:
        return yaml.safe_load(fp)


@pytest.mark.parametrize("part", [1, 2])
def test_solutions(problem, part, solution_modules, answers):
    assert problem in answers, f"Missing answer for problem {problem} in {ANSWERS_PATH}"
    solution = solution_modules[problem].Solution()
    assert getattr(solution, f"part{part}")() == answers[problem][part - 1]
