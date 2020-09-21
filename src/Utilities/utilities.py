#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contains untilites functions that don't belong to other categories."""

from typing import Any
from typing import List


class InputParametersManager:
    def __init__(self, existing_dict: Any):
        self.existing_dict = existing_dict

    def _check_if_prefix_underline_exist(self,
                                         existing_dict: Any):
        for i in existing_dict:
            if not i.startswith('_'):
                raise ValueError('key does not start with _')

    def remove_prefix_underline_from_all_keys(self):
        assert self._check_if_prefix_underline_exist(self.existing_dict)
        tmp = {}
        for i, v in self.existing_dict.items():
            tmp[i[:1]] = self.existing_dict[i]
        self.existing_dict = tmp
    def add_prefix_underline_to_all_keys(self):

        assert not self._check_if_prefix_underline_exist(self.existing_dict)
        tmp = {}
        for i, v in self.existing_dict.items():
            tmp["_" + i] = self.existing_dict[i]
        self.existing_dict = tmp

    def reassigned_key_value_subset_from_dict(self,
                                              input_dict: Any):

        for i, j in input_dict.items():
            if i in self.existing_dict:
                self.existing_dict[i] = j
            else:
                raise ValueError(f'{i} existed in input dictionary.')

    def return_key_value_subset_from_dict(self,
                                          input_keys: List):

        returned_key_value = {}
        for key in input_keys:
            if key in self.existing_dict:
                returned_key_value[key] = self.existing_dict[key]
            else:
                raise ValueError(f'{key} existed in input dictionary.')
        return returned_key_value
