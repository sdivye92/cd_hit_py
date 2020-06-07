import os
from cd_hit.error import *
from cd_hit.io import read_fasta
    
class CD_HIT:
    def __init__(self, threshold= 0.9, global_seq_identity= True, band_width= 20, max_memory= 400, word_length= 5,
                 throw_away_sequences_length= 10, tol= 2, desc_length= 20, length_difference_cutoff= 0.0,
                 amino_acid_length_difference_cutoff= 999999, long_seq_alignment_coverage= 0.0,
                 long_seq_alignment_coverage_control= 99999999, short_seq_alignment_coverage= 0.0,
                 short_seq_alignment_coverage_control= 99999999, store_in_RAM= True, print_alignment_overlap= False, nthreads= 1, fast_mode= True):

        self.threshold= threshold
        self.global_seq_identity= 1 if global_seq_identity else 0
        self.band_width= band_width
        self.max_memory= max_memory
        self.word_length= word_length
        self.throw_away_sequences_length= throw_away_sequences_length
        self.tol= tol
        self.desc_length= desc_length
        self.length_difference_cutoff= length_difference_cutoff
        self.amino_acid_length_difference_cutoff= amino_acid_length_difference_cutoff
        self.long_seq_alignment_coverage= long_seq_alignment_coverage
        self.long_seq_alignment_coverage_control= long_seq_alignment_coverage_control
        self.short_seq_alignment_coverage= short_seq_alignment_coverage
        self.short_seq_alignment_coverage_control= short_seq_alignment_coverage_control
        self.store_in_RAM= 1 if store_in_RAM else 0
        self.print_alignment_overlap= 1 if print_alignment_overlap else 0
        self.nthreads= nthreads
        self.fast_mode= fast_mode

    def __temp_file(self):
        import tempfile
        tempfile = tempfile.NamedTemporaryFile
        kwargs = {'delete': True, 'mode': 'r+'}
        return tempfile(**kwargs)

    def __get_command(self, cdhit_exe, fin, fout, threshold):
        return "{0} -i {1} -o {2} -c {3} -G {4} -b {5} -M {6} -n {7} -l {8} -t {9} -d {10} -s {11} -S {12} -aL {13} -AL {14} -aS {15} -AS {16} -B {17} -p {18} -T {19} -g {20}".format(cdhit_exe, fin, fout,
                    threshold, self.global_seq_identity, self.band_width, self.max_memory, self.word_length, self.throw_away_sequences_length, self.tol, self.desc_length, self.length_difference_cutoff, self.amino_acid_length_difference_cutoff, self.long_seq_alignment_coverage, self.long_seq_alignment_coverage_control, self.short_seq_alignment_coverage, self.short_seq_alignment_coverage_control, self.store_in_RAM, self.print_alignment_overlap, self.nthreads, self.fast_mode)
    
    def __call_cdhit(self, cdhit_exec, fin, fout, threshold):
        import subprocess
        command = self.__get_command(cdhit_exec, fin, fout, threshold)
        
        returncode = subprocess.Popen(command, shell=True).wait()
        if returncode != 0:
            raise CdhitCommandError("Error while execution of cd-hit")

    def __check_exec_installation(self, cmds):
        """Given a command returns its path, or None.
        Given a list of commands returns the first recoverable path, or None.
        """
        try:
            from shutil import which as which  # python3 only
        except ImportError:
            from distutils.spawn import find_executable as which
            
        if isinstance(cmds, str):
            return which(cmds)
        else:
            for cmd in cmds:
                path = which(cmd)
                if path is not None:
                    return path
            return path

    def __get_cdhit_exec(self):
        cdhit_exec = self.__check_exec_installation(['cd-hit', 'cdhit'])
        if cdhit_exec:
            return cdhit_exec
        else:
            current_path = os.path.dirname(__file__)
            bin_path = current_path+'/bin'
            return bin_path+"/cd-hit"
        
    def __print_to_file(self, seq_lst, header_lst, inp):
        if not (isinstance(seq_lst, list) and isinstance(header_lst, list)):
            raise ValueError("Sequence and header must be of type list")
        
        if len(seq_lst) != len(header_lst):
            raise LengthMissmatchError("Sequence and header lists must have same length")
        
        for hdr, seq in zip(header_lst, seq_lst):
            hdr_seq = ">{0}\n{1}".format(hdr, seq)
            print(hdr_seq, file=inp)

        inp.flush()
        
    def from_file(self, inp_file=None, out_file=None, threshold=0.9):
        cdhit_exec = self.__get_cdhit_exec()
        #if cdhit_exec:
        self.__call_cdhit(cdhit_exec, inp_file, out_file, threshold)
        

    def from_list(self, seq_lst=None, header_lst=None, threshold=0.9, output_fasta_file=None):
        cdhit_exec = self.__get_cdhit_exec()

        if seq_lst is None or header_lst is None:
            raise MissingArgumentError("Both sequence list and header list must be provided")
        
        with self.__temp_file() as inp, self.__temp_file() as out:
            self.__print_to_file(seq_lst, header_lst, inp)

            self.__call_cdhit(cdhit_exec, inp.name, out.name, threshold)

            df = read_fasta(out.name)
            
            if output_fasta_file:
                try:
                    from shutil import copyfile
                except ImportError:
                    from distutils.file_util import copy_file as copyfile

                copyfile(out.name, output_fasta_file)
                    
                
            

        return df["Header"].tolist(), df["Sequence"].tolist()
