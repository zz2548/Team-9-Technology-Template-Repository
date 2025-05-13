from typing import Literal, TypedDict, cast


class DiffCoverageResult(TypedDict):
    file: str
    line: int
    before: Literal["covered", "not_covered", "not_found"]
    after: Literal["covered", "not_covered", "not_found"]


def analyze_diff_coverage(
    diff_lines: dict[str, set[int]],
    base_coverage: dict[str, set[int]],
    head_coverage: dict[str, set[int]],
) -> list[DiffCoverageResult]:
    results: list[DiffCoverageResult] = []

    for file, lines in diff_lines.items():
        base_lines = base_coverage.get(file, set())
        head_lines = head_coverage.get(file, set())

        for line in lines:
            before = "covered" if line in base_lines else "not_covered"
            after = "covered" if line in head_lines else "not_covered"

            results.append({
                "file": file,
                "line": line,
                "before": cast(Literal["covered", "not_covered", "not_found"], before),
                "after": cast(Literal["covered", "not_covered", "not_found"], after),
            })

    return results
