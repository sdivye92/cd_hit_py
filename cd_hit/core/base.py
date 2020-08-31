import os
from platform import system

class BASE:
    def __init__(self, global_seq_identity= True, band_width= 20, max_memory= 400, word_length= 5,
                 throw_away_sequences_length= 10, tol= 2, desc_length= 20, length_difference_cutoff= 0.0,
                 amino_acid_length_difference_cutoff= 999999, long_seq_alignment_coverage= 0.0,
                 long_seq_alignment_coverage_control= 99999999, short_seq_alignment_coverage= 0.0,
                 short_seq_alignment_coverage_control= 99999999, store_in_RAM= True, print_alignment_overlap= False, nthreads= 1, fast_mode= True):

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

    def temp_file(self):
        import tempfile
        tempfile = tempfile.NamedTemporaryFile
        kwargs = {'delete': True, 'mode': 'r+'}
        return tempfile(**kwargs)

    def check_exec_installation(self, cmds):
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

    def get_os_name(self):
        os_name = system()
        if os_name == 'Windows':
            raise OSError("cd-hit binaries are not available for {0}".format(os_name))
        elif os_name == 'Linux':
            return 'linux'
        elif os_name == 'Darwin':
            return 'osx'

    def get_cdhit_exec(self):
        cdhit_exec = self.check_exec_installation(['cd-hit', 'cdhit'])
        if cdhit_exec:
            return cdhit_exec
        else:
            current_path = os.path.dirname(__file__)
            proj_path = '/'.join(current_path.split('/')[:-1])
            os_name = self.get_os_name()
            bin_path = proj_path+'/bin/'+os_name+'/bin'
            return bin_path+"/cd-hit"
    
