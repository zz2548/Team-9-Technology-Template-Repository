from src.main import main

def test_main_execution(capfd):
    main()
    out, err = capfd.readouterr()
    assert out.strip() == "3"
