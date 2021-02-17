# @pytest.mark.unit
# def test_main(input1, input2):
#     def _check_main_arg_condition(_max_after,
#                                   _before_date,
#                                   _after_date):
#         pass
#     _check_main_arg_condition(max_after, before_date, after_date)
import pytest
from click.testing import CliRunner

from src.Sources.Preparations.Data.social_media_crawler import \
    main
from src.Sources.Preparations.Data.social_media_crawler import \
    run_all_conditions



@pytest.mark.test_social_media_crawler
def test_social_media_crawler_input_arguments():
    # NOTE: This is a happy path testing serve no purpose but to show that
    #  testing  click is possible.
    runner = CliRunner()
    result = runner.invoke(main,
                           [
                               "all",  # this is value of argument `tag`
                               "--select_all_conditions",
                               "--max_after",
                               "15",
                               "--crawler_type",
                               "reddit",
                               "--dry_run"
                           ]
                           )
    assert result.exit_code == 0
    assert result.output == (
        f"We have passed in the following input args\n"
        f"\tselect_all_conditions = True\n"
        f"\ttags = ('all',)\n"
        f"\tmax_after = 15\n"
        f"\tcrawler_type = reddit\n"
        f"\tbefore_date = None\n"
        f"\tafter_date = None\n"
    )

