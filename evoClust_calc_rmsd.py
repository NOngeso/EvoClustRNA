#!/usr/bin/env python3

"""
When RNA models are loaded, models ending with 'template.pdb' are ignore.

c1_tha_96cdea07- tha in mapping
"""
from __future__ import print_function

import argparse
import sys
import re
import pandas as pd
import matplotlib.pyplot as plt
import datetime

from RNAalignment import RNAalignment
from RNAmodel import RNAmodel

pd.set_option('display.max_colwidth', 100)
pd.set_option('display.width', 200)
plt.style.use('ggplot')
debug = False


def sort_nicely(l):
    """ Sort the given list in the way that humans expect.

    http://blog.codinghorror.com/sorting-for-humans-natural-sort-order/
    """
    def convert(text):
        return int(text) if text.isdigit() else text

    def alphanum_key(key):
        return [convert(c) for c in re.split('([0-9]+)', key)]
    l.sort(key=alphanum_key)
    return l


def parse_num_list(s):
    """ http://stackoverflow.com/questions/6512280/accept-a-range-of-numbers-in-the-form-of-0-5-using-pythons-argparse """
    m = re.match(r'(\d+)(?:-(\d+))?$', str(s))
    # ^ (or use .split('-'). anyway you like.)
    if not m:
        return s
    start = m.group(1)
    end = m.group(2) or start
    return list(range(int(start, 10), int(end, 10) + 1))

# def pair:
#    def __init__(self, f1, f2):
#        self.f1
#        self.f2
#    def calc_distance():
#        pass


def get_parser():
    """Get parser of arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', "--rna_alignment_fn",
                        help="rna alignemnt with the extra guidance line, e.g. test_data/rp14sub.stk", required=True)
    parser.add_argument('-t', "--target", help="the native structure file", required=True)
    parser.add_argument('-o', "--output_fn", help="output csv file", default="evoclust_rmsd.csv")
    parser.add_argument('-n', "--target_name",
                        help="target name in the alignment, used to map target on the alignment, e.g. target, ade, rp14 etc.", required=True)
    parser.add_argument('-m', "--mapping_fn", help="map folders on the drive with sequence names in the alignment (<name in the alignment>:<folder name>), use | to \
    for multiple seqs, e.g. 'target:rp14_farna_eloop_nol2fixed_cst|AACY023581040:aacy23_cst', use | as a separator", required=True)
    parser.add_argument('files', nargs='+', help='files')
    parser.add_argument('-g', '--group_name',
                        help='name given group of structure, helps to analyze results', default='')
    parser.add_argument('--debug',
                        help='debug, print more prints', action='store_true')
    parser.add_argument('--dont_ignore_clusters',
                        help='dont ignore clustX or template.pdb', action='store_true')
    return parser


def calc_evo_rmsd(targetfn, target_name_alignment, files, mapping, rna_alignment_fn, group_name='', output_fn='', debug=False):
    ra = RNAalignment(rna_alignment_fn)
    print('target:', targetfn)
    target_residues = ra.get_range(target_name_alignment)
    target = RNAmodel(targetfn, target_residues, save=False, output_dir=None)

    # parse mapping, a new way
    rnastruc = []
    for r in open(opts.mapping_fn).read().strip().split('\n'):
        if not r.startswith('#'):
            rnastruc.append(r.strip())

    print(' # of rnastruc :', len(rnastruc))
    print(' rnastruc:', rnastruc)
    print(' WARNING: if any of your PDB file is missing, check mapping!')
    models = []

    for f in files:
        # OK, this `for` is very non-optimal.
        # Before taking for f in files outside this loop, it was how it should be.
        # "for f in files" was moved up because, in this way, the proper order of files is fixed.
        # Before the files in here were processed according to the mapping file.
        # Right now they will be processed as they are inputted to the program, so c1_ , c2, c3 etc.
        for rs in rnastruc:
            try:
                rs_name_alignment, rs_name_dir = rs.split(':')  # target:rp14_farna_eloop_nol2fixed_cst
            except ValueError:
                # if -m 'tpp|tpp_pdb|CP000050.1/ ..
                # rnastruc: ['tpp', 'tpp_pdb', 'CP000050.1/1019813-1019911:tc5_pdb', 'AE017180.1/640928-641029:tae_pdb', 'BX248356.1/234808-234920:tb2_pdb']
                # Traceback (most recent call last):
                # File "/home/magnus/work/src/evoClustRNA/evoClustRNA.py", line 100, in <module>
                # raise Exception("There is an error in your mapping, check all : and | carefully")
                # Exception: There is an error in your mapping, check all : and | carefully
                raise Exception("There is an error in your mapping, check all : and | carefully")

            # print ' ', rs_name_alignment,'<->', rs_name_dir # AACY023581040 <-> aacy23_cst
            #print(f)
            if rs_name_dir in f:  # rp14_farna_eloop_nol2fixed_cst*pdb
                if debug: print('\_', rs_name_dir, f)
                # models.extend(get_rna_models_from_dir(input_dir + os.sep + rs_name_dir, ra.get_range(rs_name_alignment), False, False)[:])
                # print(ra.get_range(rs_name_alignment))
                models.append(RNAmodel(f, ra.get_range(rs_name_alignment), False, False))

    data = {'target': [], 'model': [], 'rmsd': [], 'group_name': []}
    for model in models:
        # print r1.fn, r2.fn, r1.get_rmsd_to(r2)#, 'tmp.pdb')
        rmsd = round(target.get_rmsd_to(model), 2)  # , 'tmp.pdb')
        # print target, model, rmsd, group_name
        data['target'].append(target)
        data['model'].append(model)
        data['rmsd'].append(rmsd)
        data['group_name'].append(group_name)
    df = pd.DataFrame(data, columns=('target', 'model', 'rmsd', 'group_name'))
    if output_fn:
        df.to_csv(output_fn)
    try:
        df.sort_values(by='rmsd').plot(y='rmsd', use_index=False)
    except TypeError:
        print('Check if the representives have tags, e.g. c1_thf_pk_...')
    plt.savefig(output_fn.replace('.csv', '.png'))
    return df


# main
def test():
    mapping = 'target:rp14_farna_eloop_nol2fixed_cst|AACY023581040:aacy23_cst|AJ630128:aj63_cst'
    x = calc_evo_rmsd("test_data/rp14/rp14_5ddp_bound_clean_ligand.pdb", 'target',
                      ['test_data/rp14/rp14_farna_eloop_nol2fixed_cst/rp14_farna_eloop_nol2fixed_cst.out.1.pdb'],
                      mapping, rna_alignment_fn="test_data/rp14/rp14sub.stk")
    print(x)
    sys.exit(0)


if __name__ == '__main__':
    # if True: test()
    parser = get_parser()
    opts = parser.parse_args()
    print(datetime.datetime.now().ctime())
    print(opts)
    df = calc_evo_rmsd(opts.target, opts.target_name, opts.files, opts.mapping_fn,
                       opts.rna_alignment_fn, opts.group_name, opts.output_fn, opts.debug)  # , opts.dont_ignore_clusters)

    print(df)
