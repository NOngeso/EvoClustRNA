#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-c is needed if you want to run it for only one case
"""

from __future__ import print_function
import os
import argparse
import shutil
import glob

#FARNA_ARCHIVE = '/Users/magnus/work/rosetta-archive/'
ROSETTA_ARCHIVE = "/home/magnus/work/rosetta-archive/"
SIMRNA_ARCHIVE = "/home/magnus/work/simrnaweb-archive/"
TRASH = False # trash everything in ade/evox/<mode>

def get_parser():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-g', '--get-models', help="has to go with --farna <100> or --simrna <100> or both", action="store_true")
    parser.add_argument('-e', '--evoclust', action="store_true", help="run EvoClustRNA with auto, get models before")
    parser.add_argument('-p', '--process', action="store_true", help="run evoClust_get_models.py ")
    parser.add_argument('--target-only', action="store_true", help="collect only models for the reference (target) structure")
    parser.add_argument('--top100', action="store_true", help="make links of models and keep them in here @todo")
    parser.add_argument('--top200', action="store_true", help="make links of models and keep them in here @todo")
    parser.add_argument('--input', default="../../")
    parser.add_argument('--local-map', action="store_true", help="use some local mapping")
    parser.add_argument('-l', '--inf-all', help="", action="store_true")
    parser.add_argument('-c', '--calc-stats', help="", action="store_true")
    parser.add_argument('--cleanall', help="clean folder mode, keep only structures! Be careful!", action="store_true")
    parser.add_argument('--autoclust', help="do autoclustering after -e (.matrix generation with evoClustRNA.py)", action="store_true")
    parser.add_argument('-a', '--rmsd-all-structs', help="must be combined with -p",
                        action="store_true")
    parser.add_argument('-f', '--farna', help="collect Farna models needed for the analysis")
    parser.add_argument('-s', '--simrna', help="collect SimRNA models needed for the anlysis")
    parser.add_argument('-m', '--motif-save', help="", action="store_true")
    parser.add_argument('-t', '--add-solution', help="", action="store_true")
    parser.add_argument('--autoclusthalf', help="cluster in the half mode [overwrites the results and trash other clustering results .matrix "
                        "to remove files of previous analysis use --clean", action="store_true")
    parser.add_argument("-v", "--verbose",
                        action="store_true", help="be verbose")
    parser.add_argument('case')
    return parser


def exe(cmd, dryrun=False):
    print(cmd)
    if not dryrun: os.system(cmd)

def get_farna(hs, n, case):
    """
    Collects the data based on these lists:
    hs = ['a04pk', 'a99pk', 'adepk', 'b28pk', 'u51pk']
    n = topX, e.g. top10
    """
    root = os.getcwd()
    for h in hs.keys():
        job_id = hs[h]
        # cmd = "scp malibu:/home/magnus/rna-evo-malibu/ade/" + h + "/" + h + "_top" + n + "/* structures/"
        # /home/magnus/rna-evo-malibu/ade/a04pk
        try: os.mkdir(ROSETTA_ARCHIVE + case)
        except OSError: pass

        # ok, download trajectories files
        # this is off at the moment :)
        ## local_out_fn = ROSETTA_ARCHIVE + case + "/" + h + "_min.out"
        ## if not os.path.isfile(local_out_fn):
        ##     cmd = "scp malibu:/home/magnus/rna-evo-malibu/" + case + "/" + h + "/" + h + "_min.out " + \
        ##       local_out_fn
        ##     exe(cmd)
        ## else:
        ##     print('Exists ' + local_out_fn + ' [ok]')

        for i in range(1, int(n) + 1):
            # /Users/magnus/work/rosetta-archive/trna/trna_min.out.99.pdb
            pdb_fn_in = hs[h] + '_min.out.' + str(i) + '.pdb'
            pdb_fn_out = h + '_min.out.' + str(i) + '.pdb'
            lnfn = 'ln -s ' + ROSETTA_ARCHIVE + case + '/' + pdb_fn_in + ' ' + \
                            'structures/' + pdb_fn_out
            print(lnfn)
            exe(lnfn)

        # extract!
        dryrun = False
        # is this the code to get models for rp14?
        # off at the moment
        #if False:
        #    exe('mkdir %s_top%i' % (h, int(n)), dryrun)
        #    exe('extract_lowscore_decoys.py ' + local_out_fn + ' %i' % (int(n)), dryrun)
        #    exe('mv -v *min.out.*.pdb %s_top%i' % (h, int(n)), dryrun)
        #    exe('mv -v *min.out.*.pdb structures', dryrun)


def get_simrna(hs, n):
    """n=10
    trash structures
    mkdir structures

    mkdir ade_pk
    cd ade_pk
    rna_simrnaweb_download_job.py -c ade_pk-35b2a2c1 -n $n

    """
    root = os.getcwd()
    for h in hs.keys():
        job_id = hs[h]  # '{'ade_pk-35b2a2c1'
        print(job_id)
        # ~/work/simrnaweb-archive/_e614e4a0-0898-45f2-9964-52db07279965_ALL/
        #    e614e4a0-0898-45f2-9964-52db07279965_ALL-000001_AA.pdb
        for i in range(1, int(n) + 1):
            lnfn = 'ln -s ' + SIMRNA_ARCHIVE + '_' + job_id + '_ALL_top1000/' + \
              job_id + '_ALL_top1000-' + str(i).zfill(6) + '_AA.pdb ' + \
              'structures/' + h + '_' + job_id + '_ALL-' + str(i).zfill(6)+ '_AA.pdb'
            print(lnfn)
            exe(lnfn)

        # old test
        # exe("rna_simrnaweb_download_job.py --web-models -c " + job_id + " -n " + n)
        ## exe("cd _" + job_id + "_ALL_top" + n + "/ && rename 's/%s/%s_%s/' * " % (hs[h], h, hs[h]))
        ## exe("cp -v _" + job_id + "_ALL_top" + n + "/* ../structures")
        # os.chdir(root)
        #sys.exit()

# main
if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    print(args)

    # rna_simrnaweb_download_job.py -n 1000 -c ade_pk-35b2a2c1
    # mv _XXX -> structures
    if args.farna or args.simrna:
        if TRASH:
            os.system('trash *')
        try:
            os.mkdir('structures')
        except OSError:
            shutil.rmtree('structures')
            os.mkdir('structures')

    if args.top100:
        os.system('ln -s /Users/magnus/work-src/evoClustRNA/benchmark/rnas_half/' + args.case + '/evox/top100/ structures')
    if args.top200:
        os.system('ln -s /Users/magnus/work-src/evoClustRNA/benchmark/rnas_half/' + args.case + '/evox/top200/ structures')

    if args.farna:
        # this is for rosetta
        # this is not ideal, but it works ;-)
        if args.case == 'ade' and args.target_only:
            hs = {'tar' : 'adepk'}
        elif args.case == 'ade':
            hs = {'a04' : 'a04pk',
                  'a99' : 'a99pk',
                  'tar' : 'adepk',
                  'b28' : 'b28pk',
                  'u51' : 'u51pk'}  # options for this I can have!

        if args.case == 'tpp' and args.target_only:
            hs = {'tar': 'tpp'}
        elif args.case == 'tpp':
            hs = {'tae' : 'tae',
                  'tal' : 'tal',
                  'tb2' : 'tb2',
                  'tc5' : 'tc5',
                  'tar' : 'tpp'}

        if args.case == 'gmp' and args.target_only:
            hs = {'tar' : 'gmp'}
        elif args.case == 'gmp':
            hs = {'gap' : 'gapP',
                  'gba' : 'gbaP',
                  'gbx' : 'gbx',
                  'tar' : 'gmp',
                  'gxx' : 'gxx'}

        if args.case == 'thf' and args.target_only:
            hs = {'tar' : 'thf'}
        elif args.case == 'thf':
            hs = {'tar' : 'thf',
                  'hak' : 'hak',
                  'haq' : 'haqpk',
                  'hcp' : 'hcppk',
                  'tha' : 'tha'}

        if args.case == 'trna' and args.target_only:
            hs = {'tar' : 'trna'}
        elif args.case == 'trna':
            hs = {'tab' : 'tab',
                  'taf' : 'taf',
                  'tm2' : 'tm2',
                  'tm5' : 'tm5',
                  'tar' : 'trna'}

        if args.case == 'rp17' and args.target_only:
            hs = {'tar': 'rp17'}
        elif args.case == 'rp17':
            hs = {'tar' : 'rp17',
                'hcf' : 'rp17hcf',
                'pis' : 'rp17pistol',
                's21' : 'rp17s221',
                's23' : 'rp17s223'}

        ## if args.case == 'rp06' and args.target_only:
        ##     hs = ['rp06']
        ## elif args.case == 'rp06':
        ##     hs = 'rp06 rp06af193 rp06bx571'.split()

        if args.case == 'rp13' and args.target_only:
            hs = {'tar' : 'rp13'}
        elif args.case == 'rp13':
            hs = {'tar' : 'rp13',
                  'zcp' : 'rp13cp0016',
                  'zc3' : 'rp13nc3295',
                  'znc' : 'rp13nc9445',
                  'zza' : 'rp13nzaaox'}
            # tutaj ten kod mozesz sobie uzyc jakbym kiedys chcial pracowac na modelach
            # pochodzacych z modelowania z więzami
            # hs = 'rp13cp0016cst nc3295cst rp13nc9445cst nzaaoxcst rp13prs_cst'.split()
            #hs = []
            #hs = ''.split() # '

        if args.case == 'rp14' and args.target_only:
            hs = {'tar' : 'rp14'}
        elif args.case == 'rp14':
            hs = {'tar' : 'rp14',
                  'aj6' : 'rp14_aj63',
                  'cy2' : 'rp14_aacy23'}

        get_farna(hs, args.farna, args.case)

    if args.simrna:

        if args.case == 'ade' and args.target_only:
            hs = {'tar': 'ade_pk-35b2a2c1'}
        elif args.case == 'ade':
            hs = {'tar': 'ade_pk-35b2a2c1',
                  'a04': '9c6339e0-591c-498d-9745-1a828f9ee81d',
                  'a99': '2e496700-b989-4044-883d-d34257b022ab',
                  'u51': 'e614e4a0-0898-45f2-9964-52db07279965',
                  'b28': '7bc1d432-eac8-47cf-a42e-aa3c89efc721'}

        if args.case == 'tpp' and args.target_only:
            hs = {'tar': '16662ebf-cf31-42d1-98a3-2aae31f28087'}
        elif args.case == 'tpp':
            hs = {'tar': '16662ebf-cf31-42d1-98a3-2aae31f28087',
                  'tc5': 'aed2c40b-bb70-44a7-846d-b133359fc6bd',
                  'tb2': '0abbb76e-9cda-482f-abb2-94557e91acd8',
                  'tae': '6bff10d7-d4ec-43ce-8f79-8f538fa1ae65',
                  'tal': 'd2609d4d-bd6f-49fd-acbe-0ab278e0166b'}

        if args.case == 'trna' and args.target_only:
            hs = {'tar': 'a9bc516d-e3da-489d-93ef-5eb20e3f13c3'}
        elif args.case == 'trna':
            hs = {'tar': 'a9bc516d-e3da-489d-93ef-5eb20e3f13c3',
                  'taf': '822df074-320e-4166-9fd1-8fbcf085908a',
                  'tm5': '613bcfcf-f513-4945-9cf4-6df7db04545e',
                  'tab': 'cf61bea5-88c4-4e82-8042-dc04ce5cadcf',
                  'tm2': '8ca21d4d-7ceb-4736-9619-7c1814c75637'}

        if args.case == 'gmp' and  args.target_only:
            hs = {'tar': 'faa97ed7'}
        elif args.case == 'gmp':
            hs = {'tar': 'faa97ed7',
                  'gapP' : 'd9d225c5',
                  'gbx' : '00de79c8',
                  'gbaP' : 'd2b57aef',
                  'gxx' : '6bd26658' }

        if args.case == 'thf' and  args.target_only:
            hs = {'tar' : '7f0f8826'}
        elif args.case == 'thf':
            hs = {'tar' : '7f0f8826',
                  'tha' : '5f8916a8',
                  'hak' : 'cb6e7e4d',
                  'haq' : '497811c4',
                  'hcp' : 'hcp-pk-374cbbb1'}

        if args.case == 'rp17' and  args.target_only:
            hs = {'tar' : '948f56bb-ea7a-4619-9945-2fbfd6902c24'}
        elif args.case == 'rp17':
            hs = {'tar' : '27b5093d',
                  'hcf' : '6d8062dd',
                  's23' : '36828e10',
                  's21' : '742b47e6',
                  'pis' : '336e0098'}

        if args.case == 'rp13' and  args.target_only:
            hs = {'tar' : '20569fa1'}
        elif args.case == 'rp13':
            hs = {
                  'tar' : '20569fa1',
                  'zcp' : '6537608a',
                  'znc' :  'a1ea6711', #
                  'zza' : 'rp13nzaaox-6e435e41',
                  'zc3'  : 'rp13nc3295-aff20914'}

        if args.case == 'rp14' and  args.target_only:
            hs = {'tar' : 'rp14+m+pk2-946da607'}
        elif args.case == 'rp14':
            hs = {
                'tar' : 'rp14+m+pk2-946da607',
                'aj6' : 'r14aj63pk-2f5f0e3d',
                'cy2' : 'r14aacy23+m+pk2-84f4be23'}

        ## if args.case == 'rp06' and  args.target_only:
        ##     hs = {'rp06' : '9d39f986'}
        ## elif args.case == 'rp06':
        ##     hs = {'rp06' : '9d39f986',
        ##           'bx571' : '01621888',
        ##           'cp771' : 'cf8f8bb2',
        ##           'af193' : '545c05f8',
        ##           'am40'  : '9c6345c3'}

        get_simrna(hs, args.simrna)

    # -t', '--add-solution'
    if args.add_solution:
        exe('cp -v ' + args.input + '/*ref.pdb structures/solution.pdb')

    if args.cleanall:
        exe("trash reps")
        exe("trash reps_ns") # hmm... for farnatop1

        exe("trash reps_motifs")
        exe("trash reps_motifs_ns")

        exe("trash *mapping*.out")

        exe("trash inf.csv")

        exe("trash rmsd_motif.csv")
        exe("trash rmsds.csv")
        exe("trash rmsd_motif.png")

        exe("trash *png")
        exe("trash *csv")

        exe("trash *matrix")

    mapping = args.input + "/*mapping*ref.txt"
    if args.local_map:
        mapping = "*mapping*ref.txt"

    # -e', '--evoclust'
    if args.evoclust:
        # exe("evoClustRNA.py -a ../../ade_plus_ade_cleanup.sto -i structures -m ../../mapping_pk.txt -f")  # ade
        options = ''
        if args.motif_save:
            options += ' -s '

        # there should be only one sto, so I think I can remove this ref.sto, if there is more than
        # one this should cause some error
        #exe("evoClustRNA.py -a ../../" + args.case + "*ref.sto -i structures -s -m ../../*mapping*ref.txt -f " + options)  # tpp<bleble>.sto
        exe("evoClustRNA.py -a " + args.input + "/*ref.sto -i structures -m " + mapping + " -f " + options)  # tpp<bleble>.sto

    if args.autoclust:
         exe("evoClust_autoclustix.py *mapping*X.matrix")


    if args.autoclusthalf:
        exe("evoClust_autoclustix.py --half  *mapping*X.matrix")

    # now case has different modes, so I have to clean up case to only first part
    # rp17_X_X -> rp17
    case = args.case.split('_')[0]

    # '-a', '--rmsd-all-structs'
    if args.rmsd_all_structs:
         exe("evoClust_calc_rmsd.py -a " + args.input + "/*ref.sto -t " + args.input + "*ref.pdb -o rmsd_all_strucs.csv -n " + case + " -m " + mapping + "  structures/*.pdb")

    if args.inf_all:
        exe("rna_calc_inf.py -f -t " + args.input + "/*ref.pdb structures/tar*.pdb -o inf_all.csv -m 0")

    # -p, --process
    if args.process:
        # -u --skip_structures
        exe("evoClust_get_models.py -i structures/ *.out -u")
        exe("evoClust_get_models.py -i structures/ *.out -n tar -u")

    # -c, --calc-stats
    if args.calc_stats:
        exe("rna_pdb_toolsx.py --rpr --inplace reps/*.pdb")
        exe("evoClust_calc_rmsd.py -a " + args.input  + "/*ref.sto -t " + args.input  + "/*ref.pdb -n " + case + " -m " + mapping + " -o rmsd_motif.csv reps/*.pdb")
        #exe("evoClust_calc_rmsd.py -a " + args.input  + "/*ref.sto -t " + args.input  + "/*ref.pdb -n " + case + " -m " + mapping + " -o rmsd_motif_ns.csv reps_ns/*.pdb")
        ## exe("evoClust_calc_rmsd.py -a " + args.input  + "/*ref.sto -t " + args.input  + "/*ref.pdb -n " + case + " -m " + mapping + " -o rmsd_motif_top100.csv top100/*.pdb")
        ## exe("evoClust_calc_rmsd.py -a " + args.input  + "/*ref.sto -t " + args.input  + "/*ref.pdb -n " + case + " -m " + mapping + " -o rmsd_motif_top200.csv structures/*.pdb")
        ## exe("evoClust_calc_rmsd.py -a " + args.input  + "/*ref.sto -t " + args.input  + "/*ref.pdb -n " + case + " -m " + mapping + " -o rmsd_motif_top200.csv structures/*.pdb")
        ## exe("evoClust_calc_rmsd.py -a " + args.input  + "/*ref.sto -t " + args.input  + "/*ref.pdb -o rmsd_all_strucs.csv -n " + case + " -m " + mapping + "  structures/*.pdb")

        # pre-process structures to be compatible with the native
        if glob.glob('reps_ns/*.pdb'):
            if case == 'rp13': exe("cd reps_ns && rna_pdb_toolsx.py --delete 'A:46-56' --inplace *")
            if case == 'rp14': exe("cd reps_ns && rna_pdb_toolsx.py --delete 'A:35-44' --inplace *") # 32 U-G
            if case == 'rp17': exe("cd reps_ns && rna_pdb_toolsx.py --delete 'A:48-51' --inplace *")
            if case == 'ade': exe("cd reps_ns && rna_pdb_toolsx.py --delete 'A:72' --inplace *")
            if case == 'tpp': exe("cd reps_ns && rna_pdb_toolsx.py --delete 'A:80' --inplace *")
            if case == 'gmp': exe("cd reps_ns && rna_pdb_toolsx.py --delete 'A:76+77' --inplace *")

        # if reps_ns are not empty
        if glob.glob('reps_ns/*.pdb'):
            exe("rna_pdb_toolsx.py --inplace --rpr reps_ns/*.pdb")
            if case == 'trna':
                exe("rna_calc_rmsd.py -t " + args.input + "/*ref.pdb --model_ignore_selection A/34/O2  --target_ignore_selection A/34/O2 reps_ns/*.pdb")
            elif case == 'rp14':  # ignore U/G 32
                exe("rna_calc_rmsd.py -t ../../*ref.pdb  "
                    "--target_selection A:1-31+33-61  "
                    "--model_selection A:1-31+33-61   "
                    "reps_ns/*.pdb")
            elif case == 'rp17':
                exe("rna_calc_rmsd.py   -t ../../*ref.pdb  "
                    " --target_selection A:1-48+52-63  "
                    "--model_selection A:1-48+52-63  "
                    "--model_ignore_selection A/57/O2\\' "
                    "reps_ns/*.pdb")
            else:
                exe("rna_calc_rmsd.py -t " + args.input + "/*ref.pdb reps_ns/*.pdb")

            exe("rna_calc_inf.py -f -t " + args.input + "/*ref.pdb reps_ns/*.pdb")


    print('evox [ok]')
