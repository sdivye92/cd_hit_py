import os
from platform import system
from .._error import *
from .._io import read_fasta
from .base import BASE
    
class CD_HIT(BASE):
    def __init__(self, global_seq_identity= True, band_width= 20, max_memory= 400, word_length= 5,
                 throw_away_sequences_length= 10, tol= 2, desc_length= 20, length_difference_cutoff= 0.0,
                 amino_acid_length_difference_cutoff= 999999, long_seq_alignment_coverage= 0.0,
                 long_seq_alignment_coverage_control= 99999999, short_seq_alignment_coverage= 0.0,
                 short_seq_alignment_coverage_control= 99999999, store_in_RAM= True,
                 print_alignment_overlap= False, nthreads= 1, fast_mode= True):

        super().__init__(global_seq_identity= True, band_width= 20, max_memory= 400, word_length= 5,
                 throw_away_sequences_length= 10, tol= 2, desc_length= 20, length_difference_cutoff= 0.0,
                 amino_acid_length_difference_cutoff= 999999, long_seq_alignment_coverage= 0.0,
                 long_seq_alignment_coverage_control= 99999999, short_seq_alignment_coverage= 0.0,
                 short_seq_alignment_coverage_control= 99999999, store_in_RAM= True,
                 print_alignment_overlap= False, nthreads= 1, fast_mode= True)

    def __get_command(self, cdhit_exe, fin, fout, threshold):
        return "{0} -i {1} -o {2} -c {3} -G {4} -b {5} -M {6} -n {7} -l {8} -t {9} -d {10} -s {11} -S {12} -aL {13} -AL {14} -aS {15} -AS {16} -B {17} -p {18} -T {19} -g {20}".format(cdhit_exe, fin, fout,
                    threshold, self.global_seq_identity, self.band_width, self.max_memory, self.word_length, self.throw_away_sequences_length, self.tol, self.desc_length, self.length_difference_cutoff, self.amino_acid_length_difference_cutoff, self.long_seq_alignment_coverage, self.long_seq_alignment_coverage_control, self.short_seq_alignment_coverage, self.short_seq_alignment_coverage_control, self.store_in_RAM, self.print_alignment_overlap, self.nthreads, self.fast_mode)
    
    def __call_cdhit(self, cdhit_exec, fin, fout, threshold):
        import subprocess
        command = self.__get_command(cdhit_exec, fin, fout, threshold)
        
        returncode = subprocess.Popen(command, shell=True).wait()
        if returncode != 0:
            raise CdhitCommandError("Error while execution of cd-hit")
        
    def from_file(self, inp_file=None, out_file=None, threshold=0.9):
        cdhit_exec = self._get_cdhit_exec(['cd-hit', 'cdhit'])
        #if cdhit_exec:
        print(cdhit_exec)
        self.__call_cdhit(cdhit_exec, inp_file, out_file, threshold)
        

    def from_list(self, seq_lst=None, header_lst=None, threshold=0.9, output_fasta_file=None):
        cdhit_exec = self._get_cdhit_exec(['cd-hit', 'cdhit'])

        if seq_lst is None or header_lst is None:
            raise MissingArgumentError("Both sequence list and header list must be provided")
        
        with self._temp_file() as inp, self._temp_file() as out:
            self._print_to_file(seq_lst, header_lst, inp)

            self.__call_cdhit(cdhit_exec, inp.name, out.name, threshold)

            df = read_fasta(out.name)
            
            if output_fasta_file:
                try:
                    from shutil import copyfile
                except ImportError:
                    from distutils.file_util import copy_file as copyfile

                copyfile(out.name, output_fasta_file)
                    
        return df["Header"].tolist(), df["Sequence"].tolist()
