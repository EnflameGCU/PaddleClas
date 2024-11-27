# Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import sys
import yaml

# XXX: avoid triggering error on DCU machines
import tarfile

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__dir__, '../')))

from ppcls.utils import config, convert_to_dict
from ppcls.engine.engine import Engine

if __name__ == "__main__":
    args = config.parse_args()
    config = config.get_config(args.config, overrides=args.override, show=False)
    config.profiler_options = args.profiler_options
    uniform_output_enabled = config["Global"].get("uniform_output_enabled",
                                                  False)
    if uniform_output_enabled:
        if os.path.exists(
                os.path.join(config["Global"]["output_dir"],
                             "train_result.json")):
            try:
                os.remove(
                    os.path.join(config["Global"]["output_dir"],
                                 "train_result.json"))
            except:
                pass
        config_dict = convert_to_dict(config)
        with open(
                os.path.join(config["Global"]["output_dir"], "config.yaml"),
                "w") as f:
            yaml.dump(config_dict, f)
    engine = Engine(config, mode="train")
    engine.train()
