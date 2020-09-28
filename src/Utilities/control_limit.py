# -*- coding: utf-8 -*-

"""Control all types of request limit imposed by social media API."""

import time


class ControlLimit:
    """Skipped."""

    def __init__(self):
        """Skipped."""
        self.start = time.time()
        self.end = None

    def control_pushshift_limit(
        self,
        total_number_of_request: int,
        max_per_min: int = 150,
    ) -> None:
        """Skipped."""
        self.end = time.time()
        max_per_second = max_per_min / 60
        interval = self.end - self.start
        number_of_request_per_second = total_number_of_request / interval
        if number_of_request_per_second > max_per_second:
            sleep_length = (
                int(
                    (number_of_request_per_second - max_per_second)
                    / max_per_second,
                )
                + 1
            )
            print(
                "request per second is too high "
                f"|| paused request for {sleep_length} second",
            )
            time.sleep(sleep_length)
        else:
            print(
                "request per second is acceptable || no need to pause request",
            )
