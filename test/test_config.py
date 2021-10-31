import pytest
import make_trays

@pytest.fixture()
def no_args(monkeypatch):
    monkeypatch.setattr("sys.argv", ["pytest", "-d"])

def test_no_args(no_args):
    with pytest.raises(SystemExit) as e:
        maker = make_trays.MakeTrays()
    assert e.value.code == 'You need to specify an output folder (-o <folder>) so I know where to put everything.'


@pytest.fixture()
def enough_args_to_avoid_early_exit(monkeypatch):
    monkeypatch.setattr("sys.argv", ["pytest", "-d", "-o", "testfolder", "--dimensions", "4x2x1"])

def test_some_defaults(enough_args_to_avoid_early_exit):
    maker = make_trays.MakeTrays()
    assert maker.config['unit_name'] == "in"
    assert maker.config['scale_units'] == 25.4
    maker.make()
    assert "testfolder/4-in-L/2-in-W/1-in-H/tray_4x2x1.3mf" in maker.result['models']
    assert len(maker.result['models']) == 1


@pytest.fixture()
def cli_cm(monkeypatch):
    monkeypatch.setattr(
        "sys.argv", ["pytest", "-d", "-o", "testfolder", "--dimensions", "1x1x1", "-u", "cm"])

def test_cli_cm(cli_cm):
    maker = make_trays.MakeTrays()
    assert maker.config['unit_name'] == "cm"
    assert maker.config['scale_units'] == 10.0

@pytest.fixture()
def only_output_args(monkeypatch):
    monkeypatch.setattr("sys.argv", ["pytest", "-d", "-o", "testfolder"])

def test_only_output_args(only_output_args):
    with pytest.raises(SystemExit) as e:
        maker = make_trays.MakeTrays()
        maker.make()
    assert str(e.value.code).startswith("This probably wasn't what you were expecting")


@pytest.fixture()
def non_existent_config(monkeypatch):
    monkeypatch.setattr("sys.argv", ["pytest", "-d", "-c", "test/no-config.json"])


def test_non_existent_config(non_existent_config):
    with pytest.raises(SystemExit) as e:
        maker = make_trays.MakeTrays()
        maker.make()
    assert str(e.value.code).startswith(
        "Specified config file does not exist:")


