import pytest
import pandas as pd

from cd_hit import read_fasta
from cd_hit import write_fasta
from cd_hit._error import LengthMissmatchError

def test_read_fasta():
    inp = read_fasta("test/test_seq.fasta")
    expected_inp = pd.read_csv("test/test_seq.csv")

    assert inp.shape == expected_inp.shape
    assert all(inp.Sequence == expected_inp.Sequence)
    assert all(inp.Header == expected_inp.Header)

def test_write_fasta(tmpdir):
    seq = pd.DataFrame(
        [
            ['seq0', 'MYQVWEEFSRAVEKLYLTDPMKVRVVLKYRHCDGNLCIKVTDNSVCLQYKTDQAQDVK'],
            ['seq1', 'EEFSRAVEKLYLTDPMKVRVVLKYRHCDGNLCIKVTDNSVVSYEMRLFGVQKDNFALEHSLL']
        ], columns = ['Header', 'Sequence']
    )

    expected_out = '>seq0\nMYQVWEEFSRAVEKLYLTDPMKVRVVLKYRHCDGNLCIKVTDNSVCLQYKTDQAQDVK\n>seq1\nEEFSRAVEKLYLTDPMKVRVVLKYRHCDGNLCIKVTDNSVVSYEMRLFGVQKDNFALEHSLL\n'
    
    out_file = tmpdir.join('output.fasta')
    write_fasta(out_file.strpath, seq.Sequence.to_list(), seq.Header.to_list())

    assert out_file.read() == expected_out

@pytest.mark.xfail(raises=LengthMissmatchError)
def test_line_mismatch_error(tmpdir):
    seq = ['MYQVWEEFSRAVEKLYLTDPMKVRVVLKYRHCDGNLCIKVTDNSVCLQYKTDQAQDVK',
    'EEFSRAVEKLYLTDPMKVRVVLKYRHCDGNLCIKVTDNSVVSYEMRLFGVQKDNFALEHSLL']
    header = ['seq0']

    out_file = tmpdir.join('output.fasta')
    write_fasta(out_file.strpath, seq, header)
