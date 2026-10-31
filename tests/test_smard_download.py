from smard_download import save_week


def test_save_week_twice_gives_one_file(tmp_path):
    """Saving the same week twice must give 1 file, not 2 (idempotent)."""
    week_data = {"series": [[1792969200000, 23.88]]}

    save_week(week_data, 4169, 1792969200000, folder=tmp_path)
    save_week(week_data, 4169, 1792969200000, folder=tmp_path)

    files = list(tmp_path.iterdir())
    assert len(files) == 1
