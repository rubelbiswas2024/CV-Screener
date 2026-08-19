from app.generation.candidate_specifications import CandidateSpecificationCatalog


def test_all_returns_at_least_one_spec():
    specs = CandidateSpecificationCatalog.all()
    assert len(specs) > 0


def test_all_returns_a_copy_not_the_internal_list():
    specs = CandidateSpecificationCatalog.all()
    specs.append("not a real spec")

    assert "not a real spec" not in CandidateSpecificationCatalog.all()
