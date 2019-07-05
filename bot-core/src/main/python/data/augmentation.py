import logging
import random
import re
from glob import glob as expand, iglob as iexpand
from itertools import product
from os import path
from typing import List

import numpy as np
import ruamel_yaml as yaml

import utils


class StoriesAugmentation:
    logger = logging.getLogger(__file__)

    def __init__(self, stories_path: str, config_file: str, output_file: str, seed: int = None) -> None:
        self.stories_path = stories_path
        self.output_file = output_file
        self.config_file = config_file
        self.config = self._load_configuration(config_file)
        if seed:
            random.seed(seed)

    def augment(self):
        utils.delete_file(self.output_file)
        stories = self.load_stories()
        with open(self.output_file, "w") as outfile:
            for name, options in self.config.items():
                augmented_stories = self._augment_one_rule(stories, name, options)
                if augmented_stories:
                    outfile.write("\n".join(augmented_stories))

    def load_stories(self):
        sub_folders = self._sub_folders()
        stories = {}
        for folder in sub_folders:
            files = expand(path.join(self.stories_path, folder, "*"))
            split_stories = [self.parse_story(f) for f in files]
            stories[folder] = [item for sublist in split_stories for item in sublist]
        return stories

    @classmethod
    def parse_story(cls, filename):
        with open(filename, 'rt') as file:
            content = file.read()
            content = utils.remove_empty_lines(content)
        stories = cls.split_stories(content)
        return [story for story in stories if story.strip() != ""]

    @classmethod
    def split_stories(cls, story: str) -> List[str]:
        return re.split(r'\n(?=##)', story, flags=re.MULTILINE)

    @classmethod
    def remove_title(cls, story: str) -> str:
        return "\n".join([line for line in story.splitlines() if not line.startswith('##')])

    def _sub_folders(self):
        return [p.split("/")[-1] for p in iexpand(path.join(self.stories_path, '*'))]

    def _augment_one_rule(self, stories, name, options):
        rule = options["rule"]
        amount = options.get("amount", None)
        num_to_generate = self._get_max_combinations(rule, stories, amount)
        all_stories_one_rule = self._make_all_stories_one_rule(stories, rule)
        augmented_stories = list()
        for index in range(num_to_generate):
            story = self._make_one_story(all_stories_one_rule, name, index)
            if story:
                augmented_stories.append(story)
        return augmented_stories

    def _make_one_story(self, all_stories_one_rule, name, index) -> str:
        if all_stories_one_rule:
            picked_stories = all_stories_one_rule.pop(random.randrange(0, len(all_stories_one_rule)))
            new_story = '\n'.join([self.remove_title(story) for story in picked_stories])
            return f"## generated_story_{name}_story{index}\n{new_story}\n"

    @staticmethod
    def _make_all_stories_one_rule(all_stories, rule):
        return list(product(*[all_stories[subfolder] for subfolder in rule]))

    @staticmethod
    def _load_configuration(path_to_config):
        product_config = dict()
        with open(path_to_config) as config_file:
            try:
                config = yaml.safe_load(config_file)
                for name, options in config.items():
                    product_rule = list(product(*options["rule"]))
                    for it, rule in enumerate(product_rule):
                        product_config[f"{name}_{it}"] = config[name].copy()
                        product_config[f"{name}_{it}"]["rule"] = rule
            except yaml.YAMLError as e:
                StoriesAugmentation.logger.error("Failed to load configuration")
                raise e
            return product_config

    @staticmethod
    def _get_total_combinations(rule, stories):
        return int(np.prod([len(stories[folder]) for folder in rule]))

    @classmethod
    def _get_max_combinations(cls, rule, stories, amount=None):
        if amount is None:
            return cls._get_total_combinations(rule, stories)
        elif type(amount) == int:
            return amount
        elif type(amount) == float:
            return round(cls._get_total_combinations(rule, stories) * amount)
        else:
            cls.logger.error(f"When 'amount' is specified, it must be int or float. Given {type(amount)}")
            raise ValueError("Amount is not int or float")

