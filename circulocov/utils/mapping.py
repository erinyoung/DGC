#!/usr/bin/env python

""" Mapping/Alignment of reads to assembly """

import logging
import subprocess
import pysam
import os

def mapping(reads, assembly, preset, threads, out, tmp):
    """ Minimap2 FTW """

    # naming sam file
    sam = tmp + preset + ".sam"
    bam = out + preset + ".bam"

    # convert reads to list
    reads = [reads] if isinstance(reads, str) else reads

    logging.info(f"Starting alignment for {reads}")
    command     = ["minimap2", "-ax", preset, "-t", str(threads), assembly] + reads + [">", sam]
    command_str = " ".join(command)
    process     = subprocess.Popen(command_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return_code = process.wait()

    # Check if the command executed successfully
    if return_code == 0:
        logging.debug("Command executed successfully.")
    else:
        logging.debug(f"Error: Command returned non-zero exit code {return_code}.")
    
    if os.path.exists(sam):
        logging.debug(f"Sorting and indexing {sam}")
        # note: originally I kept the sam files and pysam threw some indexing errors
        pysam.sort('-o', bam, '-@', str(threads), sam)
        pysam.index(bam)

        logging.info(f"Bam file {bam} created")
        return bam
    
    else:
        return False