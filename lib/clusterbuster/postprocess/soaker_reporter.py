#!/usr/bin/env python3

# Copyright 2022 Robert Krawitz/Red Hat
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import sys
import textwrap
from copy import deepcopy
from lib.clusterbuster.postprocess.ClusterBusterReporter import ClusterBusterReporter

class soaker_reporter(ClusterBusterReporter):
    def __init__(self, jdata: dict, report_format: str):
        ClusterBusterReporter.__init__(self, jdata, report_format)
        self.initialize_accumulators(['work_iterations'])
        self.set_header_components(['namespace', 'pod', 'container', 'process_id'])

    def generate_summary(self, results: dict):
        # I'd like to do this, but if the nodes are out of sync time-wise, this will not
        # function correctly.
        ClusterBusterReporter.generate_summary(self, results)
        results['Interations'] = self._summary['work_iterations']
        results['Interations/sec'] = round(self._summary['work_iterations'] / self._summary['data_run_span'])
        results['Interations/CPU sec'] = round(self._summary['work_iterations'] / self._summary['cpu_time'])

    def generate_row(self, results: dict, row: dict):
        ClusterBusterReporter.generate_row(self, results, row)
        result = {}
        result['Elapsed Time'] = round(row['data_elapsed_time'], 3)
        result['iterations'] = row['work_iterations']
        result['iterations/sec'] = round(row['work_iterations'] / row['data_elapsed_time'])
        result['iterations/CPU sec'] = round(row['work_iterations'] / row['cpu_time'])
        results[row['namespace']][row['pod']][row['container']][row['process_id']] = result
