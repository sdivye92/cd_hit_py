import os
from platform import system
from cd_hit.error import *
from cd_hit.io import read_fasta
from .base import BASE

class CD_HIT_2D(BASE):

    def __init__(self, global_seq_identity=True, band_width=20, max_memory=400, word_length=5,
                 throw_away_sequences_length=10, tol=2, desc_length=20, length_difference_cutoff=0.0,
                 length_difference_cutoff_2=1.0, amino_acid_length_difference_cutoff=999999,
                 amino_acid_length_difference_cutoff_2=0, long_seq_alignment_coverage=0.0,
                 long_seq_alignment_coverage_control=99999999, short_seq_alignment_coverage=0.0,
                 short_seq_alignment_coverage_control=99999999, store_in_RAM=True,
                 print_alignment_overlap=False, nthreads=1, fast_mode=True):

        super().__init__(global_seq_identity=global_seq_identity,
                         band_width=band_width, max_memory=max_memory,
                         word_length=word_length,
                         throw_away_sequences_length=throw_away_sequences_length,
                         tol=tol,
                         desc_length=desc_length,
                         length_difference_cutoff=length_difference_cutoff,
                         amino_acid_length_difference_cutoff=amino_acid_length_difference_cutoff,
                         long_seq_alignment_coverage=long_seq_alignment_coverage,
                         short_seq_alignment_coverage_control=short_seq_alignment_coverage_control,
                         store_in_RAM=store_in_RAM,
                         print_alignment_overlap=print_alignment_overlap,
                         nthreads=nthreads,
                         fast_mode=fast_mode)

        self.length_difference_cutoff_2=length_difference_cutoff_2
        self.amino_acid_length_difference_cutoff_2=amino_acid_length_difference_cutoff_2

    def __get_command(self, cdhit_exe, fin1, fin2, fout, threshold):
        return "{0} -i {1} -i2 {2} -o {3} -c {4} -G {5} -b {6} -M {7} -n {8} -l {9} -t {10} -d {11} -s {12} -s2 {13} -S {14} -S2 {15} -aL {16} -AL {17} -aS {18} -AS {19} -B {20} -p {21} -T {22} -g {23}".format(cdhit_exe, fin1, fin2, fout,threshold, self.global_seq_identity, self.band_width, self.max_memory, self.word_length, self.throw_away_sequences_length, self.tol, self.desc_length, self.length_difference_cutoff, self.length_difference_cutoff_2, self.amino_acid_length_difference_cutoff, self.amino_acid_length_difference_cutoff_2, self.long_seq_alignment_coverage, self.long_seq_alignment_coverage_control, self.short_seq_alignment_coverage, self.short_seq_alignment_coverage_control, self.store_in_RAM, self.print_alignment_overlap, self.nthreads, self.fast_mode)
        
    def __call_cdhit(self, cdhit_exec, fin1, fin2, fout, threshold):
        import subprocess
        command = self.__get_command(cdhit_exec, fin1, fin2, fout, threshold)
        print(command)
        returncode = subprocess.Popen(command, shell=True).wait()
        if returncode != 0:
            raise CdhitCommandError("Error while execution of cd-hit")
        
    def from_file(self, inp_file1=None, inp_file2=None, out_file=None, threshold=0.9):
        cdhit_exec = self._get_cdhit_exec(['cd-hit-2d'])
        #if cdhit_exec:
        print(cdhit_exec)
        self.__call_cdhit(cdhit_exec, inp_file1, inp_file2, out_file, threshold)

    def from_list(self, seq_lst1=None, header_lst1=None, seq_lst2=None, header_lst2=None, threshold=0.9, output_fasta_file=None):
        cdhit_exec = self._get_cdhit_exec(['cd-hit-2d'])

        if seq_lst1 is None or header_lst1 is None:
            raise MissingArgumentError("Both sequence list and header list for db1 must be provided")
        if seq_lst2 is None or header_lst2 is None:
            raise MissingArgumentError("Both sequence list and header list for db2 must be provided")
        
        with self._temp_file() as inp1, self._temp_file() as inp2, self._temp_file() as out:
            self._print_to_file(seq_lst1, header_lst1, inp1)
            self._print_to_file(seq_lst2, header_lst2, inp2)

            self.__call_cdhit(cdhit_exec, inp1.name, inp2.name, out.name, threshold)

            df = read_fasta(out.name)
            
            if output_fasta_file:
                try:
                    from shutil import copyfile
                except ImportError:
                    from distutils.file_util import copy_file as copyfile

                copyfile(out.name, output_fasta_file)
                    
        return df["Header"].tolist(), df["Sequence"].tolist()
