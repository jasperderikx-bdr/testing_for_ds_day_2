import pandas as pd

from dishwashers.process import PREDICTIONS_PATH, main


# -- Exercise 7 --
# In previous exercises the model was trained on the dummy data, but for the next test this is a little more difficult.
# main() uses environment variables to read the data. You might think that you can mock these with monkeypatch.setenv().
# But if you follow all the lines of code, you'll find out that the os.environ.get() is called before the monkeypatch,
# so it won't work. The solution is: setting the pytest environment variables. (Note: for this reason pytest-env is
# part of the requirements.dev.txt.)
# Add the following code to the pyproject.toml under [tool.pytest.ini_options].
#
# env = [
#     "DISHWASHER_REGISTRATION_PATH=tests/test_data/dummy_dishwasher_registration.csv",
#     "PREDICTIONS_PATH=tests/pytest_basetemp/dummy_predictions.csv"
# ]
#
# How do you know that it worked?
def test_process_main(restrict_grid_search: None, mock_scraper: None) -> None:
    main()

    # To make sure that this test works with the dummy data, we check the number of output rows. On the original data
    # this number should be 35.
    assert 10 == pd.read_csv(PREDICTIONS_PATH).shape[0]

# -- Exercise 8 --
# If all exercises are completed, the code coverage is almost 100%. There is only 1 line left. In this specific case
# it's best to ignore it. Add the following code to the pyproject.toml under [tool.coverage.report].
#
# exclude_lines = [
#     "if __name__ == .__main__.:"
# ]