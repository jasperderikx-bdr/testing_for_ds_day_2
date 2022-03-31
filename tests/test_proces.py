from dishwashers.process import main as proces_main


def test_process_main(restrict_grid_search: None, mock_scraper: None) -> None:
    proces_main()
