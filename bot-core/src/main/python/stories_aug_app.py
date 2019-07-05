import argparse

from data.augmentation import StoriesAugmentation


def create_argument_parser():
    """Parse all the command line arguments for the training script."""
    parser = argparse.ArgumentParser(description='Augment rasa stories', add_help=True)

    parser.add_argument(
        '-s', '--stories',
        type=str,
        default="./base_stories",
        help="The path to the directory with all stories "
             "to use as base to the augmentation process.")

    parser.add_argument(
        '-r', '--rules',
        type=str,
        help="The full path to the rules file.")
    parser.add_argument(
        '-o', '--output',
        type=str,
        default="augmented_stories.md",
        help="The full path to the output file.")
    parser.add_argument(
        '--seed',
        type=int,
        default=None,
        help="A seed to control random number generation.")
    return parser


if __name__ == "__main__":
    arg_parser = create_argument_parser()
    args = arg_parser.parse_args()
    sa = StoriesAugmentation(args.stories, args.rules, args.output, args.seed)
    sa.augment()
