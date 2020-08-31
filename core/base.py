import os
from platform import system

class BASE:
    def __init__(self):
        pass

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
    
