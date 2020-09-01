import pytest
import pandas as pd
from cd_hit import read_fasta

from cd_hit import CD_HIT, CD_HIT_2D

def test_cd_hit_from_file(tmpdir):
    with open("test/filtered_cdhit.fasta", "r") as f:
        expected_out = f.read()

    out_file = tmpdir.join("output.fasta")
    cdh = CD_HIT()
    cdh.from_file("test/test_seq.fasta", out_file, threshold=0.7)

    assert out_file.read() == expected_out

def test_cd_hit_from_list(tmpdir):
    with open("test/filtered_cdhit.fasta", "r") as f:
        expected_out_content = f.read()

    out_file = tmpdir.join("output.fasta")
    
    inp = pd.read_csv("test/test_seq.csv")
    expected_out = read_fasta("test/filtered_cdhit.fasta")
    cdh = CD_HIT()
    head, seq = cdh.from_list(inp.Sequence.to_list(), inp.Header.to_list(), threshold=0.7, output_fasta_file=out_file)

    assert len(seq) == len(expected_out.Sequence.to_list())
    assert len(head) == len(expected_out.Header.to_list())
    assert seq == expected_out.Sequence.to_list()
    assert head == expected_out.Header.to_list()
    assert out_file.read().strip('\n') == expected_out_content

def test_cd_hit_2d_from_file(tmpdir):
    with open("test/filtered_cdhit2d.fasta", "r") as f:
        expected_out = f.read()

    out_file = tmpdir.join("output.fasta")
    cdh2d = CD_HIT_2D()
    cdh2d.from_file("test/test_seq.fasta", "test/test_seq2.fasta", out_file, threshold=0.7)

    assert out_file.read() == expected_out

def test_cd_hit_2d_from_list(tmpdir):
    with open("test/filtered_cdhit2d.fasta", "r") as f:
        expected_out_content = f.read()

    out_file = tmpdir.join("output.fasta")
    
    inp1 = pd.read_csv("test/test_seq.csv")
    inp2 = pd.read_csv("test/test_seq2.csv")
    expected_out = read_fasta("test/filtered_cdhit2d.fasta")
    cdh2d = CD_HIT_2D()
    head, seq = cdh2d.from_list(inp1.Sequence.to_list(), inp1.Header.to_list(),inp2.Sequence.to_list(), inp2.Header.to_list(), threshold=0.7, output_fasta_file=out_file)

    assert len(seq) == len(expected_out.Sequence.to_list())
    assert len(head) == len(expected_out.Header.to_list())
    assert seq == expected_out.Sequence.to_list()
    assert head == expected_out.Header.to_list()
    assert out_file.read().strip('\n') == expected_out_content
