#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import os
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    logger.info("PRE-CLEANING - Downloading input artifact ... ")
    artifact = run.use_artifact(args.input_artifact)
    df = pd.read_csv(artifact.file())


    logger.info("CLEANING DATA - Dropping outliers ... ")
    min_price = args.min_price
    max_price = args.max_price
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()
    
    logger.info("CLEANING DATA - Convert last_review to datetime ... ")
    df['last_review'] = pd.to_datetime(df['last_review'])

    logger.info("POST-CLEANING - Saving file ... ")
    filename = "clean_sample.csv"

    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()

    df.to_csv(filename, index=False)

    logger.info("POST-CLEANING - Preparing to upload the output artifact ... ")
    artifact = wandb.Artifact(
            name=args.output_artifact,
            type=args.output_type,
            description=args.output_description,
    )

    artifact.add_file(filename)

    logger.info("POST-CLEANING - Uploading the output artifact ... ")
    run.log_artifact(artifact)

    os.remove(filename)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Name of the input artifact to be cleaned",
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="Name of the output artifact to be uploaded after cleaning",
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help="Type of the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="Description of the output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="Minimum price",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="Maximum price",
        required=True
    )


    args = parser.parse_args()

    go(args)
