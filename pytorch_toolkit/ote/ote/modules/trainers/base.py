"""
 Copyright (c) 2020 Intel Corporation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import logging
import os
import sys
from abc import ABCMeta, abstractmethod

import torch
import yaml
from mmcv.utils import Config

from ote.utils import run_with_termination


class BaseTrainer(metaclass=ABCMeta):
    def __init__(self):
        pass

    def __call__(self, config, gpu_num, out, update_config, tensorboard_dir):
        logging.basicConfig(level=logging.INFO)
        logging.info(f'Commandline:\n{" ".join(sys.argv)}')

        cfg = Config.fromfile(config)

        update_config = ' '.join([f'{k}={v}' for k, v in update_config.items()])
        update_config = f' --update_config {update_config}' if update_config else ''

        update_config = self._add_extra_args(cfg, config, update_config)

        logging.info('Training started ...')
        training_info = self._train_internal(config, gpu_num, update_config, tensorboard_dir)
        logging.info('... training completed.')

        with open(out, 'a+') as dst_file:
            yaml.dump(training_info, dst_file)

    def _train_internal(self, config, gpu_num, update_config, tensorboard_dir):
        tools_dir = self._get_tools_dir()
        tensorboard_dir = f' --tensorboard-dir {tensorboard_dir}' if tensorboard_dir is not None else ''

        training_info = {'training_gpu_num': 0}
        if os.getenv('MASTER_ADDR') is not None and os.getenv('MASTER_PORT') is not None:
            # Distributed training is handled by Kubeflow’s PyTorchJob at a higher level.
            logging.info('Distributed training started ...')
            run_with_termination(f'python {tools_dir}/train.py'
                                 f' --launcher=pytorch'
                                 f' {config}'
                                 f'{tensorboard_dir}'
                                 f'{update_config}'.split(' '))
            logging.info('... distributed training completed.')
        elif torch.cuda.is_available():
            logging.info('Training on GPUs started ...')
            available_gpu_num = torch.cuda.device_count()
            if available_gpu_num < gpu_num:
                logging.warning(f'available_gpu_num < args.gpu_num: {available_gpu_num} < {gpu_num}')
                logging.warning(f'decreased number of gpu to: {available_gpu_num}')
                gpu_num = available_gpu_num
                sys.stdout.flush()
            run_with_termination(f'{tools_dir}/dist_train.sh'
                                 f' {config}'
                                 f' {gpu_num}'
                                 f'{tensorboard_dir}'
                                 f'{update_config}'.split(' '))
            training_info['training_gpu_num'] = gpu_num
            logging.info('... training on GPUs completed.')
        else:
            logging.info('Training on CPU started ...')
            run_with_termination(f'python {tools_dir}/train.py'
                                 f' {config}'
                                 f'{tensorboard_dir}'
                                 f'{update_config}'.split(' '))
            logging.info('... training on CPU completed.')

        return training_info

    def _add_extra_args(self, cfg, config_path, update_config):
        return update_config

    @abstractmethod
    def _get_tools_dir(self):
        pass